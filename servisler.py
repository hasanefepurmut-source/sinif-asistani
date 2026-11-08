"""Sayfaların ortak kullandığı Streamlit yardımcıları.

API anahtarı ve depo adı şu sırayla aranır:
  1. st.secrets / ortam değişkeni (yayındaki uygulama için)
  2. Panelden girilen değer: sadece sunucunun BELLEĞİNDE tutulur, hiçbir dosyaya
     yazılmaz; uygulama kapanınca unutulur.

Yönetici şifresi:
  1. YONETICI_SIFRESI ayarı (st.secrets / ortam değişkeni) varsa o kullanılır.
  2. Yoksa, kendi bilgisayarında panelden belirlenen şifre yonetici_sifresi.json
     dosyasında geri çözülemez bir özet (PBKDF2) olarak saklanır.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
import time

import streamlit as st

import ortak
from ortak import Asistan, BelgeDeposu, ayar, model_adi

SIFRE_DOSYASI = ortak.PROJE_KLASORU / "yonetici_sifresi.json"
SIFRE_EN_AZ = 6
YANLIS_DENEME_SINIRI = 5
KILIT_SURESI_SN = 60
_PBKDF2_TEKRAR = 200_000


@st.cache_resource(show_spinner=False)
def bellek() -> dict:
    """Uygulama açık kaldığı sürece tüm ziyaretçiler için ortak bellek."""
    return {}


@st.cache_resource(show_spinner=False)
def _istemci(anahtar: str):
    return ortak.istemci_olustur(anahtar)


def yerel_mi() -> bool:
    """Uygulama baslat.bat ile, kendi bilgisayarında çalışıyorsa True.

    İki koşul birden aranır: baslat.bat'ın koyduğu işaret VE adresin localhost olması.
    Yayındaki (Streamlit Cloud) uygulamada bu işaret yoktur.
    """
    if os.environ.get("SINIF_ASISTANI_YEREL") != "1":
        return False
    try:
        host = st.context.headers.get("Host") or ""
    except Exception:  # noqa: BLE001
        return False
    if host.startswith("["):          # IPv6, örn. [::1]:8501
        host = host[1:].split("]")[0]
    else:                             # örn. localhost:8501
        host = host.split(":")[0]
    return host in ("localhost", "127.0.0.1", "::1")


# ------------------------------------------------------------ Anahtar/depo ---
def anahtar() -> str | None:
    return ayar("GEMINI_API_KEY") or bellek().get("anahtar")


def anahtar_kaynagi() -> str | None:
    if ayar("GEMINI_API_KEY"):
        return "ayarlar"
    if bellek().get("anahtar"):
        return "bellek"
    return None


def istemci_al():
    a = anahtar()
    return _istemci(a) if a else None


def depo_adi() -> str | None:
    return ortak.depo_adi() or bellek().get("depo")


def servisleri_al():
    """(asistan, depo, sorun) döndürür. sorun: None, 'sorun_anahtar' veya 'sorun_depo'
    (dil.py'deki metin anahtarları)."""
    istemci = istemci_al()
    if istemci is None:
        return None, None, "sorun_anahtar"
    depo = depo_adi()
    if not depo:
        return None, None, "sorun_depo"
    return Asistan(istemci, depo, model_adi()), BelgeDeposu(istemci, depo), None


# ------------------------------------------------------------------ Şifre ---
def sifre_modu() -> str | None:
    """'ayarlar' (Secrets/ortam), 'dosya' (panelden belirlenmiş) veya None (yok)."""
    if ayar("YONETICI_SIFRESI"):
        return "ayarlar"
    if SIFRE_DOSYASI.exists():
        return "dosya"
    return None


def _ozet(sifre: str, tuz: bytes, tekrar: int = _PBKDF2_TEKRAR) -> str:
    return hashlib.pbkdf2_hmac("sha256", sifre.encode("utf-8"), tuz, tekrar).hex()


def sifre_belirle(yeni: str) -> None:
    tuz = secrets.token_bytes(16)
    veri = {"yontem": "pbkdf2_sha256", "tekrar": _PBKDF2_TEKRAR,
            "tuz": tuz.hex(), "ozet": _ozet(yeni, tuz)}
    SIFRE_DOSYASI.write_text(json.dumps(veri), encoding="utf-8")


def sifre_dogru_mu(girilen: str) -> bool:
    mod = sifre_modu()
    if mod == "ayarlar":
        gercek = ayar("YONETICI_SIFRESI") or ""
        # Türkçe karakterlerde hata vermesin diye bayt olarak karşılaştırılır.
        return hmac.compare_digest(girilen.encode("utf-8"), gercek.encode("utf-8"))
    if mod == "dosya":
        try:
            veri = json.loads(SIFRE_DOSYASI.read_text(encoding="utf-8"))
            beklenen = veri["ozet"]
            hesap = _ozet(girilen, bytes.fromhex(veri["tuz"]), int(veri["tekrar"]))
        except (OSError, ValueError, KeyError):
            return False
        return hmac.compare_digest(hesap, beklenen)
    return False


def kilit_kalan_sn() -> int:
    """Çok fazla yanlış denemeden sonra kalan bekleme süresi (saniye)."""
    return max(0, int(bellek().get("kilit_bitis", 0) - time.time()))


def yanlis_deneme_kaydet() -> None:
    b = bellek()
    b["yanlis"] = b.get("yanlis", 0) + 1
    if b["yanlis"] >= YANLIS_DENEME_SINIRI:
        b["kilit_bitis"] = time.time() + KILIT_SURESI_SN
        b["yanlis"] = 0


def denemeleri_sifirla() -> None:
    bellek().pop("yanlis", None)
    bellek().pop("kilit_bitis", None)
