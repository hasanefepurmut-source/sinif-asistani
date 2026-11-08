"""Yönetici paneli: kurulum ve bilgi yönetimi. Her zaman şifre ister.

Şifre yoksa: kendi bilgisayarında ilk açılışta şifre belirleme formu çıkar;
yayındaki uygulamada panel kapalı kalır (şifre Secrets'a girilmeli).

Kurulum bitmemişse sadece Kurulum adımları gösterilir. Bittiyse sekmeler:
  Belge yükle | Metin yaz | Kayıtlı belgeler | Kurulum
"""
import streamlit as st

import ortak
import servisler
import stil
from dil import t
from ortak import DESTEKLENEN_UZANTILAR, kota_hatasi_mi, mime_turu

stil.hero(t("panel_ust"), t("panel_baslik"), t("panel_alt"))


# ------------------------------------------------------------------ Giriş ---
def yeni_sifre_hatasi(s1: str, s2: str) -> str | None:
    if len(s1) < servisler.SIFRE_EN_AZ:
        return t("sifre_kisa")
    if s1 != s2:
        return t("sifre_eslesmiyor")
    return None


def sifre_belirle_formu():
    with st.form("sifre_formu"):
        st.markdown(f"#### 🛡️ {t('sifre_belirle_baslik')}")
        st.caption(t("sifre_belirle_aciklama"))
        s1 = st.text_input(t("yeni_sifre"), type="password")
        s2 = st.text_input(t("sifre_tekrar"), type="password")
        kaydet = st.form_submit_button(t("sifre_kaydet"))
    if kaydet:
        if hata := yeni_sifre_hatasi(s1, s2):
            st.error(hata)
            return
        servisler.sifre_belirle(s1)
        st.session_state["yonetici"] = True
        st.session_state["panel_mesaji"] = ("ok", t("sifre_kaydedildi"))
        st.rerun()


def giris_formu():
    with st.form("giris_formu"):
        st.markdown(f"#### 🔐 {t('giris_baslik')}")
        sifre = st.text_input(t("sifre"), type="password")
        giris = st.form_submit_button(t("giris"))
    if not giris:
        return
    kalan = servisler.kilit_kalan_sn()
    if kalan:
        st.error(t("kilitli", sn=kalan))
    elif servisler.sifre_dogru_mu(sifre):
        servisler.denemeleri_sifirla()
        st.session_state["yonetici"] = True
        st.rerun()
    else:
        servisler.yanlis_deneme_kaydet()
        kalan = servisler.kilit_kalan_sn()
        st.error(t("kilitli", sn=kalan) if kalan else t("sifre_yanlis"))


def giris_yapildi_mi() -> bool:
    if st.session_state.get("yonetici") and servisler.sifre_modu():
        return True
    st.session_state["yonetici"] = False
    if servisler.sifre_modu() is None:
        if servisler.yerel_mi():
            sifre_belirle_formu()
        else:
            st.warning(t("panel_kapali"))
        return False
    giris_formu()
    return False


if not giris_yapildi_mi():
    st.page_link("sayfalar/sohbet.py", label=t("sohbete_don"), icon="💬")
    st.stop()

if st.sidebar.button(t("cikis"), key="cikis"):
    st.session_state["yonetici"] = False
    st.rerun()


# ---------------------------------------------------------- Yardımcılar ---
def islem_yap(islem, basari_mesaji: str):
    """İşlemi çalıştırır, sonucu bir sonraki çizimde göstermek üzere saklar."""
    with st.spinner(t("isleniyor")):
        try:
            islem()
            st.session_state["panel_mesaji"] = ("ok", basari_mesaji)
        except Exception as hata:  # noqa: BLE001
            metin = t("kota_doldu") if kota_hatasi_mi(hata) else t("islem_basarisiz", hata=hata)
            st.session_state["panel_mesaji"] = ("hata", metin)
    st.rerun()


def boyut_yaz(bayt: int) -> str:
    if bayt < 1024:
        return f"{bayt} B"
    if bayt < 1024 * 1024:
        return f"{bayt / 1024:.1f} KB"
    return f"{bayt / 1024 / 1024:.1f} MB"


if mesaj := st.session_state.pop("panel_mesaji", None):
    (st.success if mesaj[0] == "ok" else st.error)(mesaj[1])


# --------------------------------------------------------------- Kurulum ---
def kurulum_bolumu():
    istemci = servisler.istemci_al()
    depo = servisler.depo_adi()

    # Adım 1: API anahtarı
    st.subheader(t("adim1"))
    kaynak = servisler.anahtar_kaynagi()
    if kaynak == "ayarlar":
        st.success(t("anahtar_ayarlardan"))
    elif kaynak == "bellek":
        st.success(t("anahtar_bellekte"))
    if kaynak != "ayarlar":
        if servisler.yerel_mi():
            st.markdown(t("anahtar_nasil"))
            with st.form("anahtar_formu", clear_on_submit=True):
                yeni = st.text_input(t("anahtar_etiket"), type="password")
                kaydet = st.form_submit_button(t("anahtar_kullan"))
            if kaydet:
                anahtari_kaydet(yeni.strip())
        elif kaynak is None:
            st.warning(t("anahtar_yok_bulut"))

    # Adım 2: Depo
    st.subheader(t("adim2"))
    if depo:
        st.success(t("depo_hazir"))
    elif istemci is None:
        st.caption(t("once_adim1"))
    elif st.button(t("depo_olustur"), type="primary"):
        islem_yap(lambda: depo_kaydet(ortak.depo_olustur(istemci)), t("depo_olusturuldu"))

    # Adım 3: Toplu yükleme (isteğe bağlı)
    st.subheader(t("adim3"))
    st.caption(t("adim3_aciklama"))
    if st.button(t("toplu_dugme"), disabled=not (istemci and depo)):
        toplu_yukleme_yap(istemci, depo)

    # Adım 4: Yayınlama bilgisi
    if depo:
        st.subheader(t("adim4"))
        st.caption(t("adim4_aciklama"))
        st.code(
            'GEMINI_API_KEY = "..."\n'
            'YONETICI_SIFRESI = "..."\n'
            f'DEPO_ADI = "{depo}"',
            language="toml",
        )

    # Şifre değiştirme (sadece panelden belirlenen şifre için)
    if servisler.sifre_modu() == "dosya":
        with st.expander(f"🛡️ {t('sifre_degistir_baslik')}"):
            sifre_degistir_formu()


def sifre_degistir_formu():
    with st.form("sifre_degistir_formu", clear_on_submit=True):
        mevcut = st.text_input(t("mevcut_sifre"), type="password")
        s1 = st.text_input(t("yeni_sifre"), type="password")
        s2 = st.text_input(t("sifre_tekrar"), type="password")
        kaydet = st.form_submit_button(t("sifre_kaydet"))
    if kaydet:
        if not servisler.sifre_dogru_mu(mevcut):
            st.error(t("sifre_yanlis"))
        elif hata := yeni_sifre_hatasi(s1, s2):
            st.error(hata)
        else:
            servisler.sifre_belirle(s1)
            st.session_state["panel_mesaji"] = ("ok", t("sifre_kaydedildi"))
            st.rerun()


def anahtari_kaydet(yeni: str):
    if not yeni:
        st.error(t("anahtar_bos"))
        return
    try:
        istemci = ortak.istemci_olustur(yeni)
        next(iter(istemci.file_search_stores.list()), None)  # anahtar çalışıyor mu?
    except Exception as hata:  # noqa: BLE001
        st.error(t("anahtar_calismadi", hata=hata))
        return
    servisler.bellek()["anahtar"] = yeni
    st.session_state["panel_mesaji"] = ("ok", t("anahtar_kabul"))
    st.rerun()


def depo_kaydet(ad: str):
    servisler.bellek()["depo"] = ad
    try:
        ortak.DEPO_ADI_DOSYASI.write_text(ad, encoding="utf-8")
    except OSError:
        pass  # yayındaki uygulamada dosya yazılamayabilir; bellek yeterli


def toplu_yukleme_yap(istemci, depo):
    satirlar = []
    with st.spinner(t("yukleniyor")):
        try:
            for ad, durum, ayrinti in ortak.toplu_yukle(ortak.BelgeDeposu(istemci, depo)):
                satirlar.append(f"- **{ad}**: {t('d_' + durum)} {ayrinti}".rstrip())
        except Exception as hata:  # noqa: BLE001
            satirlar.append(t("depo_okunamadi", hata=hata))
    st.markdown("\n".join(satirlar) or t("dosya_yok"))


# ------------------------------------------------------ Bilgi yönetimi ---
def belge_yukle_bolumu(depo):
    st.markdown(t("yukle_aciklama"))
    with st.form("dosya_formu", clear_on_submit=True):
        dosyalar = st.file_uploader(
            t("dosya_sec"),
            type=[u.lstrip(".") for u in DESTEKLENEN_UZANTILAR],
            accept_multiple_files=True,
        )
        yukle = st.form_submit_button(t("yukle_dugme"))
    if yukle:
        if not dosyalar:
            st.error(t("once_dosya"))
            return

        def hepsini_yukle():
            for d in dosyalar:
                depo.yukle(d.getvalue(), d.name, mime_turu(d.name) or "text/plain")

        islem_yap(hepsini_yukle, t("yuklendi_mesaj", adlar=", ".join(d.name for d in dosyalar)))


def metin_yaz_bolumu(depo):
    st.markdown(t("metin_aciklama"))
    with st.form("metin_formu", clear_on_submit=True):
        baslik = st.text_input(t("baslik_etiket"), placeholder=t("baslik_ornek"))
        metin = st.text_area(t("metin_etiket"), height=200)
        kaydet = st.form_submit_button(t("kaydet"))
    if kaydet:
        if not baslik.strip() or not metin.strip():
            st.error(t("bos_hata"))
            return
        islem_yap(lambda: depo.metin_kaydet(baslik.strip(), metin),
                  t("kaydedildi", ad=baslik.strip()))


def belgeler_bolumu(depo, belgeler, liste_hatasi):
    if liste_hatasi:
        st.error(t("liste_hata", hata=liste_hatasi))
        return
    if not belgeler:
        st.info(t("liste_bos"))
        return
    st.caption(t("liste_ozet", n=len(belgeler)))
    st.dataframe(
        [{t("kolon_belge"): b.gorunen_ad, t("kolon_boyut"): boyut_yaz(b.boyut),
          t("kolon_tarih"): b.tarih} for b in belgeler],
        hide_index=True, width="stretch",
    )
    secenekler = {b.gorunen_ad: b.ad for b in belgeler}
    secilen = st.selectbox(t("silinecek"), list(secenekler), index=None,
                           placeholder=t("belge_sec"))
    if st.button(t("sil_dugme"), disabled=secilen is None):
        islem_yap(lambda: depo.sil(secenekler[secilen]), t("silindi", ad=secilen))


# ------------------------------------------------------------- Yerleşim ---
asistan, depo, _ = servisler.servisleri_al()

if depo is None:
    st.info(t("kurulum_tamamlanmadi"))
    kurulum_bolumu()
else:
    try:
        belgeler, liste_hatasi = depo.listele(), None
    except Exception as hata:  # noqa: BLE001
        belgeler, liste_hatasi = [], hata

    m1, m2, m3 = st.columns(3)
    m1.metric(t("metrik_belge"), len(belgeler))
    m2.metric(t("metrik_model"), ortak._CALISAN_MODEL.get(asistan.model, asistan.model))
    m3.metric(t("metrik_durum"), t("durum_hazir"))

    s_yukle, s_metin, s_liste, s_kurulum = st.tabs(
        [t("sekme_yukle"), t("sekme_metin"), t("sekme_liste"), t("sekme_kurulum")])
    with s_yukle:
        belge_yukle_bolumu(depo)
    with s_metin:
        metin_yaz_bolumu(depo)
    with s_liste:
        belgeler_bolumu(depo, belgeler, liste_hatasi)
    with s_kurulum:
        kurulum_bolumu()
