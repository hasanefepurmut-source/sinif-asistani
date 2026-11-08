"""Sohbet sayfası: sınıf arkadaşlarının soru sorduğu yer."""
import streamlit as st

import stil
from dil import dil, t
from servisler import servisleri_al

asistan, _, sorun = servisleri_al()

stil.hero(t("sohbet_ust"), t("sohbet_baslik"), t("sohbet_alt"),
          [t("rozet_belge"), t("rozet_kaynak"), t("rozet_uydurmaz")])

if "mesajlar" not in st.session_state:
    st.session_state["mesajlar"] = []


def mesaji_goster(m: dict):
    kullanici = m["rol"] == "user"
    with st.chat_message("user" if kullanici else "assistant",
                         avatar="🧑‍🎓" if kullanici else "✨"):
        st.markdown(m["metin"])
        if m.get("kaynaklar"):
            stil.kaynak_ciplari(t("kaynak"), m["kaynaklar"])
        if m.get("ayrinti"):
            with st.expander(t("teknik")):
                st.code(m["ayrinti"], language=None)


def ornek_sec(metin: str):
    st.session_state["bekleyen_soru"] = metin


for m in st.session_state["mesajlar"]:
    mesaji_goster(m)

if sorun:
    st.warning(t(sorun))

# Boş sohbette örnek sorular
if (asistan is not None and not st.session_state["mesajlar"]
        and "bekleyen_soru" not in st.session_state):
    stil.bolum_baslik(t("ornek_baslik"))
    sutunlar = st.columns(3)
    for sutun, anahtar in zip(sutunlar, ("ornek1", "ornek2", "ornek3")):
        with sutun:
            st.button(t(anahtar), key=f"ornek_{anahtar}", width="stretch",
                      on_click=ornek_sec, args=(t(anahtar),))

soru = st.chat_input(t("soru_yaz"), disabled=asistan is None)
if not soru:
    soru = st.session_state.pop("bekleyen_soru", None)

if soru and asistan is not None:
    gecmis = [
        {"rol": m["rol"], "metin": m["metin"]}
        for m in st.session_state["mesajlar"]
        if not m.get("hata")  # cevaplanamayan sorular modele geri gönderilmez
    ]
    yeni = {"rol": "user", "metin": soru}
    st.session_state["mesajlar"].append(yeni)
    mesaji_goster(yeni)

    with st.spinner(t("dusunuyor")):
        cevap = asistan.cevapla(gecmis, soru, dil())

    yeni["hata"] = cevap.hata
    yanit = {"rol": "assistant", "metin": cevap.metin, "kaynaklar": cevap.kaynaklar,
             "hata": cevap.hata, "ayrinti": cevap.ayrinti}
    st.session_state["mesajlar"].append(yanit)
    mesaji_goster(yanit)

if st.session_state["mesajlar"]:
    if st.button(t("temizle"), key="temizle"):
        st.session_state["mesajlar"] = []
        st.rerun()
