"""Arayüz metinleri (Türkçe / English).

Kullanım:  from dil import t;  st.write(t("sohbet_baslik"))
Yeni bir metin eklemek için METINLER sözlüğüne iki dilde ekle.
Seçili dil st.session_state["dil"] içinde ve adreste (?lang=en) tutulur.
"""
from __future__ import annotations

import streamlit as st

from ortak import DILLER

METINLER: dict[str, dict[str, str]] = {
    # ---- genel
    "sayfa_sohbet": {"tr": "Sohbet", "en": "Chat"},
    "sayfa_yonetici": {"tr": "Yönetici Paneli", "en": "Admin Panel"},
    "dil_dugmesi": {"tr": "🌐 English", "en": "🌐 Türkçe"},
    "dil_ipucu": {"tr": "Switch to English", "en": "Türkçeye geç"},

    # ---- sohbet
    "sohbet_ust": {"tr": "Yapay zeka destekli", "en": "AI-powered"},
    "sohbet_baslik": {"tr": "Sınıf Asistanı", "en": "Class Assistant"},
    "sohbet_alt": {
        "tr": "Sınav tarihleri, devamsızlık, ders kaydı… Sorunu yaz, cevabı sınıf "
              "temsilcisinin yüklediği belgelerden bulayım.",
        "en": "Exam dates, attendance, course registration… Ask your question and I'll "
              "find the answer in the documents uploaded by your class representative.",
    },
    "rozet_belge": {"tr": "Sadece yüklenen belgeler", "en": "Only uploaded documents"},
    "rozet_kaynak": {"tr": "Kaynak gösterir", "en": "Cites its sources"},
    "rozet_uydurmaz": {"tr": "Tahmin yürütmez", "en": "Never guesses"},
    "ornek_baslik": {"tr": "Şunlardan birini deneyebilirsin", "en": "Try one of these"},
    "ornek1": {"tr": "Vize tarihleri ne zaman?", "en": "When are the midterm exams?"},
    "ornek2": {"tr": "Kaç hafta devamsızlık yapabilirim?",
               "en": "How many weeks can I be absent?"},
    "ornek3": {"tr": "Ders kaydından sonra ne yapmalıyım?",
               "en": "What should I do after course registration?"},
    "soru_yaz": {"tr": "Sorunu yaz…", "en": "Type your question…"},
    "dusunuyor": {"tr": "Belgelere bakıyorum…", "en": "Checking the documents…"},
    "kaynak": {"tr": "Kaynak", "en": "Source"},
    "teknik": {"tr": "Teknik ayrıntı (sınıf temsilcisi için)",
               "en": "Technical details (for the class representative)"},
    "temizle": {"tr": "Sohbeti temizle", "en": "Clear chat"},
    "sorun_anahtar": {
        "tr": "Asistan henüz hazır değil. Lütfen sınıf temsilcisine haber ver.",
        "en": "The assistant is not ready yet. Please let your class representative know.",
    },
    "sorun_depo": {
        "tr": "Asistan henüz hazır değil. Lütfen sınıf temsilcisine haber ver.",
        "en": "The assistant is not ready yet. Please let your class representative know.",
    },
    "sohbete_don": {"tr": "Sohbete dön", "en": "Back to chat"},

    # ---- yönetici: giriş
    "panel_ust": {"tr": "Kontrol merkezi", "en": "Control center"},
    "panel_baslik": {"tr": "Yönetici Paneli", "en": "Admin Panel"},
    "panel_alt": {"tr": "Kurulum ve bilgi yönetimi", "en": "Setup and knowledge management"},
    "giris_baslik": {"tr": "Yönetici girişi", "en": "Admin sign-in"},
    "sifre": {"tr": "Şifre", "en": "Password"},
    "giris": {"tr": "Giriş yap", "en": "Sign in"},
    "sifre_yanlis": {"tr": "Şifre yanlış.", "en": "Wrong password."},
    "kilitli": {"tr": "Çok fazla yanlış deneme. {sn} saniye sonra tekrar dene.",
                "en": "Too many wrong attempts. Try again in {sn} seconds."},
    "panel_kapali": {
        "tr": "Yönetici paneli kapalı: şifre ayarlanmamış. Streamlit Cloud'da uygulama → "
              "Settings → Secrets bölümüne YONETICI_SIFRESI ekle.",
        "en": "The admin panel is locked: no password is set. On Streamlit Cloud add "
              "YONETICI_SIFRESI under app → Settings → Secrets.",
    },
    "sifre_belirle_baslik": {"tr": "Yönetici şifresi belirle", "en": "Set an admin password"},
    "sifre_belirle_aciklama": {
        "tr": "İlk kullanım: paneli korumak için bir şifre belirle. Şifre bu bilgisayarda "
              "geri çözülemez şekilde (özet olarak) saklanır.",
        "en": "First use: choose a password to protect the panel. It is stored on this "
              "computer as an irreversible hash.",
    },
    "yeni_sifre": {"tr": "Yeni şifre", "en": "New password"},
    "sifre_tekrar": {"tr": "Yeni şifre (tekrar)", "en": "New password (again)"},
    "sifre_kaydet": {"tr": "Şifreyi kaydet", "en": "Save password"},
    "sifre_kisa": {"tr": "Şifre en az 6 karakter olmalı.",
                   "en": "The password must be at least 6 characters."},
    "sifre_eslesmiyor": {"tr": "Şifreler eşleşmiyor.", "en": "Passwords do not match."},
    "sifre_kaydedildi": {"tr": "Şifre kaydedildi.", "en": "Password saved."},
    "sifre_degistir_baslik": {"tr": "Yönetici şifresini değiştir",
                              "en": "Change the admin password"},
    "mevcut_sifre": {"tr": "Mevcut şifre", "en": "Current password"},
    "cikis": {"tr": "Çıkış yap", "en": "Sign out"},

    # ---- yönetici: genel
    "isleniyor": {"tr": "İşleniyor… (büyük dosyalarda biraz sürebilir)",
                  "en": "Processing… (large files may take a while)"},
    "islem_basarisiz": {"tr": "İşlem başarısız: {hata}", "en": "Operation failed: {hata}"},
    "kota_doldu": {"tr": "Kota doldu, biraz sonra tekrar dene.",
                   "en": "Quota exceeded, try again a bit later."},
    "metrik_belge": {"tr": "Belgeler", "en": "Documents"},
    "metrik_model": {"tr": "Model", "en": "Model"},
    "metrik_durum": {"tr": "Durum", "en": "Status"},
    "durum_hazir": {"tr": "● Çevrimiçi", "en": "● Online"},

    # ---- yönetici: kurulum
    "kurulum_tamamlanmadi": {"tr": "Kurulum henüz tamamlanmadı. Adımları sırayla yap.",
                             "en": "Setup is not complete yet. Follow the steps in order."},
    "adim1": {"tr": "1 · Gemini API anahtarı", "en": "1 · Gemini API key"},
    "anahtar_ayarlardan": {"tr": "✅ Anahtar ayarlardan okunuyor.",
                           "en": "✅ The key is read from the settings."},
    "anahtar_bellekte": {
        "tr": "✅ Anahtar bu oturumda girildi (sadece bellekte, uygulama kapanınca unutulur).",
        "en": "✅ Key entered in this session (memory only, forgotten when the app closes).",
    },
    "anahtar_nasil": {
        "tr": "[aistudio.google.com](https://aistudio.google.com) → **Get API key** → "
              "**Create API key** (bu iş için yeni bir proje oluştur), sonra buraya yapıştır.",
        "en": "[aistudio.google.com](https://aistudio.google.com) → **Get API key** → "
              "**Create API key** (create a new project for this), then paste it here.",
    },
    "anahtar_etiket": {"tr": "API anahtarı", "en": "API key"},
    "anahtar_kullan": {"tr": "Anahtarı kullan", "en": "Use key"},
    "anahtar_bos": {"tr": "Anahtar boş olamaz.", "en": "The key cannot be empty."},
    "anahtar_calismadi": {
        "tr": "Anahtar çalışmadı, doğru kopyaladığından emin ol. ({hata})",
        "en": "The key did not work, make sure you copied it correctly. ({hata})",
    },
    "anahtar_kabul": {"tr": "Anahtar kabul edildi.", "en": "Key accepted."},
    "anahtar_yok_bulut": {
        "tr": "Anahtar yok. Streamlit Cloud → Settings → Secrets'a GEMINI_API_KEY ekle.",
        "en": "No key. Add GEMINI_API_KEY under Streamlit Cloud → Settings → Secrets.",
    },
    "adim2": {"tr": "2 · Bilgi deposu", "en": "2 · Knowledge store"},
    "depo_hazir": {"tr": "✅ Depo hazır.", "en": "✅ The store is ready."},
    "once_adim1": {"tr": "Önce 1. adımı tamamla.", "en": "Complete step 1 first."},
    "depo_olustur": {"tr": "Bilgi deposunu oluştur", "en": "Create the knowledge store"},
    "depo_olusturuldu": {"tr": "Depo oluşturuldu.", "en": "Store created."},
    "adim3": {"tr": "3 · Klasördeki bilgileri yükle (isteğe bağlı)",
              "en": "3 · Upload the local folder (optional)"},
    "adim3_aciklama": {
        "tr": "Bilgisayarındaki **bilgiler.txt** dosyasını ve **belgeler** klasörünü depoya "
              "yükler. Değişmeyen dosyalar atlanır, panelden eklediklerine dokunulmaz.",
        "en": "Uploads **bilgiler.txt** and the **belgeler** folder from this computer. "
              "Unchanged files are skipped; documents added from the panel are kept.",
    },
    "toplu_dugme": {"tr": "bilgiler.txt ve belgeler klasörünü yükle",
                    "en": "Upload bilgiler.txt and the belgeler folder"},
    "yukleniyor": {"tr": "Yükleniyor…", "en": "Uploading…"},
    "dosya_yok": {"tr": "Yüklenecek dosya bulunamadı.", "en": "No files to upload."},
    "depo_okunamadi": {"tr": "❌ Depo okunamadı: {hata}", "en": "❌ Could not read the store: {hata}"},
    "d_yuklendi": {"tr": "✅ yüklendi", "en": "✅ uploaded"},
    "d_guncellendi": {"tr": "🔄 güncellendi", "en": "🔄 updated"},
    "d_degismedi": {"tr": "➖ değişmemiş, atlandı", "en": "➖ unchanged, skipped"},
    "d_desteklenmiyor": {"tr": "⚠️ desteklenmeyen tür, atlandı",
                         "en": "⚠️ unsupported type, skipped"},
    "d_hata": {"tr": "❌ hata", "en": "❌ error"},
    "d_kota": {"tr": "❌ kota doldu, biraz sonra tekrar dene",
               "en": "❌ quota exceeded, try again later"},
    "adim4": {"tr": "4 · İnternette yayınlarken", "en": "4 · When publishing online"},
    "adim4_aciklama": {
        "tr": "Streamlit Cloud → Settings → Secrets kutusuna şunu yapıştır "
              "(anahtarı ve şifreyi kendininkiyle değiştir):",
        "en": "Paste this into Streamlit Cloud → Settings → Secrets "
              "(replace the key and password with your own):",
    },

    # ---- yönetici: sekmeler
    "sekme_yukle": {"tr": "📎 Belge yükle", "en": "📎 Upload"},
    "sekme_metin": {"tr": "✍️ Metin yaz", "en": "✍️ Write a note"},
    "sekme_liste": {"tr": "📚 Kayıtlı belgeler", "en": "📚 Documents"},
    "sekme_kurulum": {"tr": "⚙️ Kurulum", "en": "⚙️ Setup"},
    "yukle_aciklama": {
        "tr": "Yeni bir belge (ders programı, sınav takvimi, duyuru, yönetmelik…) yükle. "
              "**Aynı dosya adıyla** tekrar yüklersen eskisinin yerine geçer.",
        "en": "Upload a new document (timetable, exam schedule, announcement, regulation…). "
              "Uploading again **with the same file name** replaces the old one.",
    },
    "dosya_sec": {"tr": "PDF, Word (DOCX) veya TXT dosyası seç",
                  "en": "Choose a PDF, Word (DOCX) or TXT file"},
    "yukle_dugme": {"tr": "Yükle", "en": "Upload"},
    "once_dosya": {"tr": "Önce dosya seç.", "en": "Choose a file first."},
    "yuklendi_mesaj": {"tr": "Yüklendi: {adlar}", "en": "Uploaded: {adlar}"},
    "metin_aciklama": {
        "tr": "Kısa bir bilgiyi elle yaz (örn. *'Vize tarihi değişti'*). "
              "**Aynı başlıkla** tekrar kaydedersen eskisinin yerine geçer.",
        "en": "Write a short note by hand (e.g. *'The midterm date changed'*). "
              "Saving again **with the same title** replaces the old one.",
    },
    "baslik_etiket": {"tr": "Başlık", "en": "Title"},
    "baslik_ornek": {"tr": "Örn: Vize Tarihleri", "en": "e.g. Midterm Dates"},
    "metin_etiket": {"tr": "Metin", "en": "Text"},
    "kaydet": {"tr": "Kaydet", "en": "Save"},
    "bos_hata": {"tr": "Başlık ve metin boş olamaz.", "en": "Title and text cannot be empty."},
    "kaydedildi": {"tr": "'{ad}' kaydedildi.", "en": "'{ad}' saved."},
    "liste_hata": {"tr": "Belgeler listelenemedi: {hata}", "en": "Could not list documents: {hata}"},
    "liste_bos": {"tr": "Depoda henüz belge yok. 'Belge yükle' sekmesinden ekleyebilirsin.",
                  "en": "No documents yet. You can add some from the 'Upload' tab."},
    "liste_ozet": {"tr": "Asistan şu {n} belgeye bakarak cevap veriyor:",
                   "en": "The assistant answers using these {n} documents:"},
    "kolon_belge": {"tr": "Belge", "en": "Document"},
    "kolon_boyut": {"tr": "Boyut", "en": "Size"},
    "kolon_tarih": {"tr": "Tarih", "en": "Date"},
    "silinecek": {"tr": "Silinecek belge", "en": "Document to delete"},
    "belge_sec": {"tr": "Belge seç", "en": "Choose a document"},
    "sil_dugme": {"tr": "🗑️ Seçili belgeyi sil", "en": "🗑️ Delete selected document"},
    "silindi": {"tr": "'{ad}' silindi.", "en": "'{ad}' deleted."},
}


def dil() -> str:
    """Seçili dil ('tr' / 'en'). İlk açılışta adresteki ?lang= değerine bakar."""
    secili = st.session_state.get("dil")
    if secili not in DILLER:
        adres = st.query_params.get("lang", "tr")
        secili = adres if adres in DILLER else "tr"
        st.session_state["dil"] = secili
    return secili


def dil_degistir() -> None:
    yeni = "en" if dil() == "tr" else "tr"
    st.session_state["dil"] = yeni
    st.query_params["lang"] = yeni


def t(anahtar: str, **degerler) -> str:
    metin = METINLER[anahtar][dil()]
    return metin.format(**degerler) if degerler else metin
