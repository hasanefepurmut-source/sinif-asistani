"""Sınıf asistanının ortak parçaları.

Bu dosyayı hem app.py (Streamlit arayüzü) hem de bilgi_yukle.py (toplu yükleme)
kullanır. İçinde üç şey var:
  1. Ayarları okuma (önce st.secrets, yoksa ortam değişkeni)
  2. BelgeDeposu: Gemini File Search deposuna belge yükleme / listeleme / silme
  3. Asistan: soruyu Gemini'ye sorup cevabı ve kaynakları döndürme
"""
from __future__ import annotations

import hashlib
import io
import os
import time
from dataclasses import dataclass, field
from pathlib import Path

PROJE_KLASORU = Path(__file__).resolve().parent
DEPO_ADI_DOSYASI = PROJE_KLASORU / "depo_adi.txt"
BILGILER_DOSYASI = PROJE_KLASORU / "bilgiler.txt"
BELGELER_KLASORU = PROJE_KLASORU / "belgeler"

# Model adı buradan veya GEMINI_MODEL ayarından değiştirilebilir.
# (gemini-2.5-flash Kasım 2026'da yeni kullanıcılara kapatıldı; Google 3.8'i öneriyor.)
VARSAYILAN_MODEL = "gemini-3.8-flash"

# Sohbette modele gönderilecek en fazla geçmiş mesaj sayısı.
GECMIS_MESAJ_SAYISI = 10

# Desteklenen diller: "tr" (Türkçe), "en" (English)
DILLER = ("tr", "en")

MESAJLAR = {
    "tr": {
        "bulunamadi": "Bu konuda bilgi bulamadım, sınıf temsilcisine danışabilirsin.",
        "kota": ("Şu an çok fazla soru geldi ve günlük/dakikalık soru hakkımız doldu. "
                 "Lütfen biraz sonra tekrar dene."),
        "yogunluk": ("Google'ın yapay zeka sunucuları şu an çok yoğun. "
                     "Lütfen birkaç dakika sonra tekrar dene."),
        "genel": ("Bir hata oluştu, cevap alınamadı. Biraz sonra tekrar dene; "
                  "sorun sürerse sınıf temsilcisine haber ver."),
    },
    "en": {
        "bulunamadi": ("I couldn't find information about this. "
                       "You can ask your class representative."),
        "kota": ("Too many questions right now and our question limit is used up. "
                 "Please try again a bit later."),
        "yogunluk": ("Google's AI servers are very busy right now. "
                     "Please try again in a few minutes."),
        "genel": ("Something went wrong and no answer could be generated. Please try again "
                  "later; if it continues, let your class representative know."),
    },
}
# Eski adlar (Türkçe varsayılan)
BULUNAMADI_MESAJI = MESAJLAR["tr"]["bulunamadi"]
KOTA_MESAJI = MESAJLAR["tr"]["kota"]
YOGUNLUK_MESAJI = MESAJLAR["tr"]["yogunluk"]
GENEL_HATA_MESAJI = MESAJLAR["tr"]["genel"]

# Modelin "bulamadım" dediğini anlamak için aranan ifadeler (iki dilde)
BULUNAMADI_ISARETLERI = ("bilgi bulamadım", "couldn't find information",
                         "could not find information")


def mesaj(anahtar: str, dil: str = "tr") -> str:
    return MESAJLAR.get(dil, MESAJLAR["tr"])[anahtar]


def sistem_talimati(dil: str = "tr") -> str:
    if dil == "en":
        return f"""You are the helpful assistant of a university class. You answer students'
school-related questions (exam dates, attendance rules, course registration, etc.).

STRICT RULES:
1. Use ONLY information found in the documents via the file search tool. NEVER use your
   own general knowledge, guesses or information from the internet.
2. If the answer is not clearly in the documents, do not guess; write only this sentence:
   "{MESAJLAR['en']['bulunamadi']}"
3. The documents may be in Turkish. Translate their meaning faithfully into English, but
   give dates, times, room codes, grade percentages and attendance limits EXACTLY as
   written; never change, round or calculate a new date.
4. If documents contradict each other, mention both and suggest asking the class
   representative.
5. Always answer in English, short, clear and friendly.
"""
    return f"""Sen bir üniversite sınıfının yardımcı asistanısın. Öğrencilerin okulla ilgili
sorularını (sınav tarihleri, devamsızlık kuralları, ders kaydı vb.) cevaplıyorsun.

KESİN KURALLAR:
1. YALNIZCA dosya arama aracıyla bulduğun belgelerdeki bilgileri kullan. Kendi genel
   bilgini, tahminini veya internetteki bilgileri ASLA kullanma.
2. Sorunun cevabı belgelerde açıkça yoksa, tahmin yürütme ve yalnızca şu cümleyi yaz:
   "{MESAJLAR['tr']['bulunamadi']}"
3. Tarih, saat, derslik, not oranı, devamsızlık sınırı gibi bilgileri belgede yazdığı
   gibi aynen ver; asla değiştirme, yuvarlama veya hesaplayarak yeni bir tarih üretme.
4. Belgeler arasında çelişki görürsen ikisini de belirt ve sınıf temsilcisine
   danışmasını öner.
5. Her zaman Türkçe, kısa, net ve samimi cevap ver.
"""

MIME_TURLERI = {
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".txt": "text/plain",
}
DESTEKLENEN_UZANTILAR = tuple(MIME_TURLERI)


# ---------------------------------------------------------------- Ayarlar ---
def ayar(ad: str, varsayilan: str | None = None) -> str | None:
    """Ayarı önce Streamlit secrets'tan, sonra ortam değişkeninden okur."""
    try:
        import streamlit as st

        if ad in st.secrets:
            deger = str(st.secrets[ad]).strip()
            if deger:
                return deger
    except Exception:
        # secrets.toml yoksa Streamlit hata fırlatır; bu normal, ortam değişkenine geç.
        pass
    deger = os.environ.get(ad, "").strip()
    return deger or varsayilan


def model_adi() -> str:
    return ayar("GEMINI_MODEL", VARSAYILAN_MODEL)


def depo_adi() -> str | None:
    """DEPO_ADI ayarı; yoksa bilgi_yukle.py'nin yazdığı depo_adi.txt dosyası."""
    ad = ayar("DEPO_ADI")
    if ad:
        return ad
    if DEPO_ADI_DOSYASI.exists():
        return DEPO_ADI_DOSYASI.read_text(encoding="utf-8").strip() or None
    return None


def istemci_olustur(anahtar: str | None = None):
    """Gemini istemcisini oluşturur. Anahtar verilmezse ayarlardan okur; yoksa None."""
    anahtar = anahtar or ayar("GEMINI_API_KEY")
    if not anahtar:
        return None
    from google import genai

    return genai.Client(api_key=anahtar)


# ------------------------------------------------------------ Hata türleri ---
def kota_hatasi_mi(hata: Exception) -> bool:
    """429 / RESOURCE_EXHAUSTED (kota doldu) hatası mı?"""
    kod = getattr(hata, "code", None)
    durum = str(getattr(hata, "status", "") or "")
    return kod == 429 or "RESOURCE_EXHAUSTED" in durum or "RESOURCE_EXHAUSTED" in str(hata)


def mime_turu(dosya_adi: str) -> str | None:
    return MIME_TURLERI.get(Path(dosya_adi).suffix.lower())


def ozet_hash(veri: bytes) -> str:
    return hashlib.sha256(veri).hexdigest()


# ------------------------------------------------------------------- Depo ---
@dataclass
class KayitliBelge:
    ad: str            # API'deki tam ad (silmek için gerekir)
    gorunen_ad: str    # Dosya adı veya başlık (kaynak olarak bu görünür)
    boyut: int = 0
    tarih: str = ""
    durum: str = ""
    hash: str = ""


class BelgeDeposu:
    """Gemini File Search deposu üzerinde yükleme/listeleme/silme işlemleri."""

    def __init__(self, istemci, depo: str):
        self.istemci = istemci
        self.depo = depo

    # -- listeleme
    def listele(self) -> list[KayitliBelge]:
        belgeler = []
        for b in self.istemci.file_search_stores.documents.list(parent=self.depo):
            h = ""
            for m in b.custom_metadata or []:
                if m.key == "sha256":
                    h = m.string_value or ""
            belgeler.append(
                KayitliBelge(
                    ad=b.name,
                    gorunen_ad=b.display_name or b.name,
                    boyut=int(b.size_bytes or 0),
                    tarih=b.create_time.strftime("%d.%m.%Y %H:%M") if b.create_time else "",
                    durum=b.state.value if b.state else "",
                    hash=h,
                )
            )
        belgeler.sort(key=lambda x: x.gorunen_ad.lower())
        return belgeler

    # -- silme
    def sil(self, ad: str) -> None:
        self.istemci.file_search_stores.documents.delete(name=ad, config={"force": True})

    # -- yükleme (aynı adda belge varsa günceller)
    def yukle(self, veri: bytes, gorunen_ad: str, mime: str, bekleme_suresi: int = 300) -> None:
        """Belgeyi yükler. Aynı görünen adda eski belge varsa, yenisi başarıyla
        yüklendikten SONRA eskisini siler (yükleme başarısız olursa eski bilgi kaybolmaz)."""
        eskiler = [b.ad for b in self.listele() if b.gorunen_ad == gorunen_ad]

        islem = self.istemci.file_search_stores.upload_to_file_search_store(
            file=io.BytesIO(veri),
            file_search_store_name=self.depo,
            config={
                "display_name": gorunen_ad,
                "mime_type": mime,
                "custom_metadata": [{"key": "sha256", "string_value": ozet_hash(veri)}],
            },
        )
        baslangic = time.time()
        while not islem.done:
            if time.time() - baslangic > bekleme_suresi:
                raise TimeoutError(f"'{gorunen_ad}' işlenmesi çok uzun sürdü.")
            time.sleep(2)
            islem = self.istemci.operations.get(islem)
        if islem.error:
            raise RuntimeError(f"'{gorunen_ad}' yüklenemedi: {islem.error}")

        for ad in eskiler:
            self.sil(ad)

    def metin_kaydet(self, baslik: str, metin: str) -> None:
        """Elle yazılan metni .txt belgesi olarak kaydeder (başlık = belge adı)."""
        icerik = f"{baslik}\n\n{metin.strip()}\n"
        self.yukle(icerik.encode("utf-8"), baslik, "text/plain")


def depo_olustur(istemci, gorunen_ad: str = "sinif-asistani") -> str:
    depo = istemci.file_search_stores.create(config={"display_name": gorunen_ad})
    return depo.name


# ---------------------------------------------------------- Toplu yükleme ---
def yuklenecek_dosyalar(bilgiler: Path | None = None, klasor: Path | None = None):
    """(yüklenecek dosyalar, desteklenmeyen dosya adları) döndürür."""
    bilgiler = bilgiler or BILGILER_DOSYASI
    klasor = klasor or BELGELER_KLASORU
    dosyalar, atlananlar = [], []
    if bilgiler.exists():
        dosyalar.append(bilgiler)
    if klasor.is_dir():
        for yol in sorted(klasor.iterdir()):
            if not yol.is_file() or yol.name.startswith(".") or yol.name == "BENI_OKU.md":
                continue
            if yol.suffix.lower() in DESTEKLENEN_UZANTILAR:
                dosyalar.append(yol)
            else:
                atlananlar.append(yol.name)
    return dosyalar, atlananlar


def toplu_yukle(bd: BelgeDeposu, bilgiler: Path | None = None, klasor: Path | None = None):
    """bilgiler.txt ve belgeler/ klasörünü depoya yükler.

    Her dosya için (dosya_adi, durum, ayrinti) üretir. Durumlar:
    'yuklendi', 'guncellendi', 'degismedi', 'desteklenmiyor', 'hata', 'kota'.
    Depoda olup klasörde olmayan belgelere (panelden eklenenlere) dokunmaz.
    """
    dosyalar, atlananlar = yuklenecek_dosyalar(bilgiler, klasor)
    for ad in atlananlar:
        yield ad, "desteklenmiyor", ""
    mevcut = {b.gorunen_ad: b for b in bd.listele()}
    for yol in dosyalar:
        veri = yol.read_bytes()
        eski = mevcut.get(yol.name)
        if eski and eski.hash == ozet_hash(veri):
            yield yol.name, "degismedi", ""
            continue
        try:
            bd.yukle(veri, yol.name, mime_turu(yol.name) or "text/plain")
            yield yol.name, ("guncellendi" if eski else "yuklendi"), ""
        except Exception as hata:  # noqa: BLE001
            if kota_hatasi_mi(hata):
                yield yol.name, "kota", ""
                return
            yield yol.name, "hata", str(hata)


# ---------------------------------------------------------------- Asistan ---
@dataclass
class Cevap:
    metin: str
    kaynaklar: list[str] = field(default_factory=list)
    hata: bool = False
    ayrinti: str = ""  # teknik hata ayrıntısı (sorun çözmek için)


def kaynaklari_cikar(yanit) -> list[str]:
    """Cevabın dayandığı belge adlarını (tekrarsız, sırayla) çıkarır."""
    kaynaklar: list[str] = []
    try:
        meta = yanit.candidates[0].grounding_metadata
        parcalar = (meta.grounding_chunks if meta else None) or []
    except (AttributeError, IndexError, TypeError):
        return kaynaklar
    for parca in parcalar:
        rc = getattr(parca, "retrieved_context", None)
        baslik = getattr(rc, "title", None) if rc else None
        if baslik and baslik not in kaynaklar:
            kaynaklar.append(baslik)
    return kaynaklar


# Ayarlanan model bulunamazsa sırayla denenecek modeller (sonra hesaptaki
# flash modelleri otomatik aranır).
YEDEK_MODELLER: list[str] = []
# Yoğunluk (503) hatasında aynı model kaç kez denensin, aralarında kaç saniye beklensin.
YOGUNLUK_DENEME_SAYISI = 2
YOGUNLUK_BEKLEME_SN = 2
# Bir kez çalıştığı görülen model hatırlanır (her soruda tekrar aranmasın).
_CALISAN_MODEL: dict[str, str] = {}

HATA_KAYDI_DOSYASI = PROJE_KLASORU / "hata_kaydi.txt"


def hata_kaydet(metin: str) -> None:
    """Hatayı hata_kaydi.txt'ye ekler (son 200 satır tutulur). Anahtar yazılmaz."""
    try:
        from datetime import datetime

        satirlar = []
        if HATA_KAYDI_DOSYASI.exists():
            satirlar = HATA_KAYDI_DOSYASI.read_text(encoding="utf-8").splitlines()[-200:]
        satirlar.append(f"[{datetime.now():%d.%m.%Y %H:%M:%S}] {metin}")
        HATA_KAYDI_DOSYASI.write_text("\n".join(satirlar) + "\n", encoding="utf-8")
    except OSError:
        pass  # yayındaki uygulamada dosya yazılamayabilir; sorun değil


def hata_aciklamasi(hata: Exception) -> str:
    """Teknik hatayı yöneticinin anlayacağı Türkçe bir açıklamaya çevirir."""
    kod = getattr(hata, "code", None)
    msj = str(hata).lower()
    if "api key" in msj or "api_key" in msj or kod == 401:
        return ("API anahtarı geçersiz ya da bu API için uygun değil. "
                "aistudio.google.com → Get API key bölümünden yeni bir anahtar al.")
    if kod == 403:
        return ("Anahtarın bu işleme izni yok. Depo başka bir anahtarla/projede "
                "oluşturulmuş olabilir: Yönetici Paneli → Kurulum'dan yeni depo oluştur.")
    if kod == 404 and ("filesearchstore" in msj or "file_search" in msj or "store" in msj):
        return ("Bilgi deposu bulunamadı. Yönetici Paneli → Kurulum'dan yeni depo oluştur "
                "ve belgeleri tekrar yükle.")
    if kod == 404:
        return "Model bulunamadı. GEMINI_MODEL ayarıyla güncel bir model adı ver."
    if kod and kod >= 500:
        return "Google tarafında geçici bir sorun var. Birkaç dakika sonra tekrar dene."
    return "Beklenmeyen bir hata."


def _model_hatasi_mi(hata: Exception) -> bool:
    """Başka bir modelle denemeye değer bir hata mı? (model yok / desteklenmiyor)"""
    kod = getattr(hata, "code", None)
    msj = str(hata).lower()
    if "api key" in msj or "api_key" in msj or "store" in msj:
        return False  # anahtar/depo sorunu; başka model denemek işe yaramaz
    return kod in (400, 404)


def _gecici_hata_mi(hata: Exception) -> bool:
    """Google tarafında geçici sorun mu? (yoğunluk / sunucu hatası)"""
    kod = getattr(hata, "code", None)
    return kod in (500, 502, 503, 504) or "UNAVAILABLE" in str(hata)


class Asistan:
    """Soruları Gemini + File Search ile cevaplar."""

    def __init__(self, istemci, depo: str, model: str):
        self.istemci = istemci
        self.depo = depo
        self.model = model

    def _hesaptaki_flash_modelleri(self) -> list[str]:
        """Hesapta kullanılabilen 'flash' modelleri, en uygun olan başta."""
        import re

        adaylar = []
        try:
            for m in self.istemci.models.list():
                ad = (m.name or "").removeprefix("models/")
                eylemler = m.supported_actions or []
                if "flash" not in ad or "generateContent" not in eylemler:
                    continue
                if any(k in ad for k in ("image", "tts", "live", "audio", "embedding")):
                    continue
                surum = re.search(r"gemini-(\d+(?:\.\d+)?)", ad)
                kararli = not any(k in ad for k in ("preview", "exp"))
                adaylar.append((kararli, float(surum.group(1)) if surum else 0.0,
                                "lite" not in ad, ad))
        except Exception as hata:  # noqa: BLE001
            hata_kaydet(f"Model listesi alınamadı: {type(hata).__name__}: {hata}")
            return []
        return [a[3] for a in sorted(adaylar, reverse=True)]

    def _model_sirasi(self):
        """Denenecek modelleri sırayla verir (en fazla 3 farklı model).
        Hesaptaki modeller ancak ilk adaylar başarısız olursa sorgulanır."""
        denenen: list[str] = []

        def adaylar():
            yield _CALISAN_MODEL.get(self.model, self.model)
            yield from YEDEK_MODELLER
            yield from self._hesaptaki_flash_modelleri()

        for ad in adaylar():
            if ad and ad not in denenen:
                denenen.append(ad)
                yield ad
            if len(denenen) >= 3:
                return

    def _cagir(self, model, icerik, ayar_):
        """Modeli çağırır; yoğunluk hatasında kısa bekleyip tekrar dener."""
        for deneme in range(YOGUNLUK_DENEME_SAYISI):
            try:
                return self.istemci.models.generate_content(
                    model=model, contents=icerik, config=ayar_)
            except Exception as hata:  # noqa: BLE001
                if not _gecici_hata_mi(hata) or deneme == YOGUNLUK_DENEME_SAYISI - 1:
                    raise
                time.sleep(YOGUNLUK_BEKLEME_SN * (deneme + 1))

    def cevapla(self, gecmis: list[dict], soru: str, dil: str = "tr") -> Cevap:
        """Soruyu cevaplar. dil: 'tr' veya 'en' (cevabın ve mesajların dili)."""
        from google.genai import types

        dil = dil if dil in DILLER else "tr"

        icerik = []
        for m in gecmis[-GECMIS_MESAJ_SAYISI:]:
            rol = "user" if m["rol"] == "user" else "model"
            icerik.append(types.Content(role=rol, parts=[types.Part(text=m["metin"])]))
        icerik.append(types.Content(role="user", parts=[types.Part(text=soru)]))
        ayar_ = types.GenerateContentConfig(
            system_instruction=sistem_talimati(dil),
            temperature=0.1,
            tools=[types.Tool(file_search=types.FileSearch(file_search_store_names=[self.depo]))],
        )

        son_hata, son_model = None, self.model
        for model in self._model_sirasi():
            son_model = model
            try:
                yanit = self._cagir(model, icerik, ayar_)
            except Exception as hata:  # noqa: BLE001
                if kota_hatasi_mi(hata):
                    return Cevap(mesaj("kota", dil), hata=True)
                son_hata = hata
                hata_kaydet(f"Model {model}: {type(hata).__name__}: {hata}")
                if _model_hatasi_mi(hata) or _gecici_hata_mi(hata):
                    continue  # başka bir modelle dene
                break
            if model != self.model:
                _CALISAN_MODEL[self.model] = model
                hata_kaydet(f"Bilgi: '{self.model}' yerine '{model}' modeli kullanılıyor.")
            return cevabi_denetle(yanit.text or "", kaynaklari_cikar(yanit), dil)

        print(f"[HATA] Gemini çağrısı başarısız: {son_hata!r}")
        ayrinti = (f"{hata_aciklamasi(son_hata)}\n\nModel: {son_model}\n"
                   f"{type(son_hata).__name__}: {son_hata}")[:1500]
        tur = "yogunluk" if _gecici_hata_mi(son_hata) else "genel"
        return Cevap(mesaj(tur, dil), hata=True, ayrinti=ayrinti)


def cevabi_denetle(metin: str, kaynaklar: list[str], dil: str = "tr") -> Cevap:
    """Güvenlik kontrolü: belgeye dayanmayan cevabı göstermeyiz.

    - Hiç kaynak yoksa model belgelerden bir şey bulamamıştır; ne yazarsa yazsın
      uydurma riski vardır, bu yüzden 'bulamadım' mesajını gösteririz.
    - Model 'bulamadım' dediyse altında kaynak göstermeyiz (kafa karıştırmasın).
    """
    metin = metin.strip()
    bulunamadi = Cevap(mesaj("bulunamadi", dil))
    if not kaynaklar or not metin:
        return bulunamadi
    kucuk = metin.lower().replace("’", "'")
    if any(i in kucuk for i in BULUNAMADI_ISARETLERI):
        return bulunamadi
    return Cevap(metin, kaynaklar)
