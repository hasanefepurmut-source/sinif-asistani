"""Görünüm: modern, koyu, 'teknolojik' tema.

Renkler, yazı tipleri ve kart görünümü buradaki CSS ile belirlenir.
Renkleri değiştirmek için :root içindeki değişkenleri düzenlemen yeterli.
"""
from __future__ import annotations

import html

import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
  --panel: rgba(17, 24, 50, 0.55);
  --kenar: rgba(120, 140, 255, 0.18);
  --camgobegi: #22d3ee;
  --mor: #a78bfa;
  --metin: #e6ecff;
  --soluk: #93a0c4;
}

html, body, .stApp, .stMarkdown, button, input, textarea {
  font-family: 'Inter', system-ui, sans-serif;
}
h1, h2, h3, h4, [data-testid="stMetricValue"] {
  font-family: 'Space Grotesk', 'Inter', sans-serif !important;
  letter-spacing: -0.02em;
}

/* Arka plan: koyu lacivert + renkli ışık lekeleri + silik ızgara */
.stApp {
  isolation: isolate;
  background:
    radial-gradient(1100px 560px at 8% -12%, rgba(34, 211, 238, 0.13), transparent 60%),
    radial-gradient(900px 520px at 100% 0%, rgba(167, 139, 250, 0.16), transparent 60%),
    linear-gradient(180deg, #070b18 0%, #0a1024 100%);
  background-attachment: fixed;
}
.stApp::before {
  content: "";
  position: fixed;
  inset: 0;
  z-index: -1;
  pointer-events: none;
  background-image:
    linear-gradient(rgba(120, 140, 255, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(120, 140, 255, 0.06) 1px, transparent 1px);
  background-size: 44px 44px;
  -webkit-mask-image: radial-gradient(ellipse at top, black 15%, transparent 70%);
  mask-image: radial-gradient(ellipse at top, black 15%, transparent 70%);
}

[data-testid="stHeader"] { background: transparent; }
[data-testid="stAppDeployButton"], [data-testid="stDecoration"] { display: none; }

[data-testid="stSidebar"] {
  background: rgba(8, 12, 28, 0.82);
  backdrop-filter: blur(14px);
  border-right: 1px solid var(--kenar);
}

/* Başlık alanı */
.hero { padding: 0.4rem 0 1.2rem; }
.hero .ust-yazi {
  font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.22em;
  color: var(--camgobegi); margin-bottom: 0.35rem; font-weight: 600;
}
.hero h1 {
  font-size: clamp(2rem, 5.5vw, 3.1rem);
  line-height: 1.08; margin: 0; padding: 0;
  background: linear-gradient(90deg, #67e8f9 0%, #a78bfa 55%, #f0abfc 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.hero p { color: var(--soluk); margin: 0.6rem 0 0.8rem; max-width: 46rem; }
.rozet {
  display: inline-flex; align-items: center; gap: 0.45rem;
  padding: 0.28rem 0.75rem; margin: 0.2rem 0.35rem 0 0;
  border-radius: 999px; border: 1px solid var(--kenar);
  background: rgba(34, 211, 238, 0.06);
  font-size: 0.8rem; color: #c7d2fe;
}
.rozet .nokta {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--camgobegi); box-shadow: 0 0 10px var(--camgobegi);
}

/* Sohbet balonları */
[data-testid="stChatMessage"] {
  background: var(--panel);
  border: 1px solid var(--kenar);
  border-radius: 18px;
  backdrop-filter: blur(10px);
  padding: 0.9rem 1rem;
  margin-bottom: 0.6rem;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
  background: linear-gradient(135deg, rgba(34, 211, 238, 0.10), rgba(167, 139, 250, 0.10));
}
[data-testid="stChatInput"] {
  border-radius: 16px;
  border: 1px solid var(--kenar);
  box-shadow: 0 10px 40px rgba(34, 211, 238, 0.08);
}
[data-testid="stChatInput"]:focus-within {
  border-color: var(--camgobegi);
  box-shadow: 0 0 0 1px var(--camgobegi), 0 10px 40px rgba(34, 211, 238, 0.18);
}

/* Kaynak etiketleri */
.kaynaklar { margin-top: 0.7rem; display: flex; flex-wrap: wrap; gap: 0.4rem; align-items: center; }
.kaynak-etiket {
  font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--soluk);
}
.cip {
  font-size: 0.78rem; padding: 0.2rem 0.65rem; border-radius: 999px;
  background: rgba(167, 139, 250, 0.12); border: 1px solid rgba(167, 139, 250, 0.35);
  color: #ddd6fe;
}
.bolum-baslik {
  font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.14em;
  color: var(--soluk); margin: 0.4rem 0 0.5rem;
}

/* Düğmeler */
.stButton > button, [data-testid="stFormSubmitButton"] > button {
  border-radius: 12px;
  border: 1px solid var(--kenar);
  background: rgba(20, 28, 60, 0.6);
  color: var(--metin);
  transition: all 0.2s ease;
}
.stButton > button:hover {
  border-color: var(--camgobegi);
  color: #fff;
  box-shadow: 0 0 18px rgba(34, 211, 238, 0.35);
}
[data-testid="stFormSubmitButton"] > button, .stButton > button[kind="primary"] {
  background: linear-gradient(90deg, #06b6d4, #8b5cf6);
  border: none; color: #fff; font-weight: 600;
}
[data-testid="stFormSubmitButton"] > button:hover, .stButton > button[kind="primary"]:hover {
  box-shadow: 0 0 22px rgba(139, 92, 246, 0.55); filter: brightness(1.08);
}
.st-key-dil_dugmesi button {
  border-radius: 999px; font-size: 0.85rem; padding: 0.15rem 0.9rem;
  background: rgba(34, 211, 238, 0.08);
}

/* Kartlar: formlar, açılır kutular, metrikler */
[data-testid="stForm"], [data-testid="stExpander"] details, [data-testid="stMetric"] {
  background: var(--panel);
  border: 1px solid var(--kenar) !important;
  border-radius: 16px;
  backdrop-filter: blur(10px);
}
[data-testid="stMetric"] { padding: 0.8rem 1rem; }
[data-testid="stMetricValue"] { color: #67e8f9; font-size: 1.5rem; }

/* Sekmeler: hap görünümü */
.stTabs [data-baseweb="tab-list"] {
  gap: 0.35rem; padding: 0.35rem; border-radius: 14px;
  background: rgba(10, 16, 36, 0.6); border: 1px solid var(--kenar);
  flex-wrap: wrap;
}
.stTabs [data-baseweb="tab"] { border-radius: 10px; padding: 0.4rem 0.9rem; height: auto; }
.stTabs [aria-selected="true"] {
  background: linear-gradient(90deg, rgba(6, 182, 212, 0.25), rgba(139, 92, 246, 0.25));
}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }

[data-testid="stAlert"] { border-radius: 14px; }
input, textarea { border-radius: 10px !important; }

@media (max-width: 640px) {
  .hero h1 { font-size: 2rem; }
  .st-key-dil_dugmesi { max-width: 150px !important; margin-left: auto; }
  [data-testid="stChatMessage"] { padding: 0.75rem; }
}
</style>
"""


def uygula() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def hero(ust_yazi: str, baslik: str, alt: str = "", rozetler: list[str] | None = None) -> None:
    """Sayfanın üstündeki büyük başlık alanı."""
    e = html.escape
    rozet_html = "".join(
        f'<span class="rozet"><span class="nokta"></span>{e(r)}</span>' for r in rozetler or []
    )
    alt_html = f"<p>{e(alt)}</p>" if alt else ""
    st.markdown(
        f'<div class="hero"><div class="ust-yazi">{e(ust_yazi)}</div>'
        f"<h1>{e(baslik)}</h1>{alt_html}<div>{rozet_html}</div></div>",
        unsafe_allow_html=True,
    )


def kaynak_ciplari(etiket: str, kaynaklar: list[str]) -> None:
    e = html.escape
    cipler = "".join(f'<span class="cip">📄 {e(k)}</span>' for k in kaynaklar)
    st.markdown(
        f'<div class="kaynaklar"><span class="kaynak-etiket">{e(etiket)}</span>{cipler}</div>',
        unsafe_allow_html=True,
    )


def bolum_baslik(metin: str) -> None:
    st.markdown(f'<div class="bolum-baslik">{html.escape(metin)}</div>', unsafe_allow_html=True)
