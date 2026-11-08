"""Sınıf Asistanı - giriş noktası.

İki sayfa var (sol menüden seçilir):
  - Sohbet: sınıf arkadaşlarının soru sorduğu sayfa
  - Yönetici Paneli: kurulum ve bilgi yönetimi (şifreli)
Her sayfanın sağ üstünde Türkçe / English düğmesi bulunur.

Çalıştırmak için: baslat.bat dosyasına çift tıkla (veya: streamlit run app.py)
"""
import sys
from pathlib import Path

import streamlit as st

# Sayfa dosyaları ortak.py / servisler.py'yi bulabilsin
sys.path.insert(0, str(Path(__file__).resolve().parent))

st.set_page_config(page_title="Sınıf Asistanı · Class Assistant", page_icon="🎓",
                   layout="centered")

import servisler  # noqa: E402
import stil  # noqa: E402
from dil import dil, dil_degistir, t  # noqa: E402

stil.uygula()

# Sağ üstte dil düğmesi (her sayfada görünür)
_, sag = st.columns([4, 1.4])
with sag:
    st.button(t("dil_dugmesi"), key="dil_dugmesi", on_click=dil_degistir,
              help=t("dil_ipucu"), width="stretch")

# Menü sadece şifreyle giriş yapmış yöneticiye (veya kendi bilgisayarında, baslat.bat
# ile açana) görünür. Öğrenciler yalnızca sohbeti görür; yönetici paneline gizli
# adresten girilir: .../yonetici
menu_gorunsun = bool(st.session_state.get("yonetici")) or servisler.yerel_mi()
sayfa = st.navigation(
    [
        st.Page("sayfalar/sohbet.py", title=t("sayfa_sohbet"), icon="💬", default=True),
        st.Page("sayfalar/yonetici.py", title=t("sayfa_yonetici"), icon="🔐",
                url_path="yonetici"),
    ],
    position="sidebar" if menu_gorunsun else "hidden",
)
# Sayfa değişince adresteki dil kaybolmasın (yenileyince de aynı dil açılsın)
if st.query_params.get("lang") != dil():
    st.query_params["lang"] = dil()
sayfa.run()
