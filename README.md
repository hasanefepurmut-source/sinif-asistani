# 🎓 Sınıf Asistanı

Sınıf arkadaşlarının okulla ilgili sorularını (sınav tarihleri, devamsızlık, ders kaydı…)
**yalnızca senin verdiğin belgelere bakarak** cevaplayan sohbet uygulaması.

- Cevap belgelerde yoksa uydurmaz: *"Bu konuda bilgi bulamadım, sınıf temsilcisine danışabilirsin."*
- Her cevabın altında hangi belgeden geldiği yazar.
- Arkadaşların sadece linke girer, hesap açmaz.
- **Yönetici Paneli öğrencilere görünmez.** Onlar sadece sohbeti görür. Sen panele linkin
  sonuna `/yonetici` ekleyerek girersin (örn. `https://uygulaman.streamlit.app/yonetici`)
  ve şifreni yazarsın. Şifreyi bilmeyen içeri giremez.
- Sen ayrı ve **şifreli** bir sayfa olan **Yönetici Paneli**'nden kurulumu yapar, istediğin
  zaman yeni belge yükleyerek bilgileri güncellersin. **Kod yazmana veya terminal kullanmana gerek yok.**
- **Türkçe / English:** Sağ üstteki 🌐 düğmesiyle arayüz ve asistanın cevapları İngilizceye
  geçer. Doğrudan İngilizce açılan link için adresin sonuna `?lang=en` ekle.
- Modern, koyu, mobil uyumlu tasarım.

Altyapı: Python + Streamlit (arayüz) + Google Gemini API'nin hazır **File Search** aracı
(belgeler Google'ın sunduğu bir "depo"da tutulur ve aranır).

## Dosyalar

| Dosya | Ne işe yarar |
|---|---|
| `baslat.bat` | **Çift tıkla, uygulama açılsın** (Windows) |
| `app.py` | Giriş noktası; iki sayfayı (Sohbet, Yönetici Paneli) bağlar |
| `sayfalar/sohbet.py` | Sınıf arkadaşlarının soru sorduğu sayfa |
| `sayfalar/yonetici.py` | Yönetici Paneli (kurulum, belge yükleme, silme) |
| `ortak.py` | Depo işlemleri, Gemini'ye soru sorma (model adı burada) |
| `servisler.py` | Ayarları/anahtarı bulan, şifreyi kontrol eden yardımcı kod |
| `dil.py` | Arayüzdeki tüm yazılar (Türkçe + English) |
| `stil.py`, `.streamlit/config.toml` | Tasarım (renkler, yazı tipleri, tema) |
| `yonetici_sifresi.json` | Panelden belirlediğin şifrenin geri çözülemez özeti (GitHub'a yüklenmez) |
| `teshis.py` | Sorun teşhis aracı (isteğe bağlı) |
| `bilgi_yukle.py` | (İsteğe bağlı) Panel yerine terminalden toplu yükleme |
| `bilgiler.txt` | Elle yazdığın bilgiler (**içindeki tarihler örnektir, değiştir!**) |
| `belgeler/` | PDF / DOCX / TXT dosyalarını buraya koy |
| `depo_adi.txt` | İlk yüklemede otomatik oluşur; deponun adını tutar |
| `tests/` | API anahtarı gerektirmeyen testler |

---

## 1. Uygulamayı aç

Bilgisayarında Python 3.10 veya üstü kurulu olmalı (<https://www.python.org/downloads/>,
kurarken **"Add Python to PATH"** kutusunu işaretle).

Bu klasördeki **`baslat.bat`** dosyasına **çift tıkla**. İlk seferde gerekli paketleri
kurar (birkaç dakika), sonra tarayıcıda uygulama açılır. Siyah pencereyi kapatınca
uygulama da kapanır.

> Mac'te: Terminal'de bu klasöre gir ve
> `SINIF_ASISTANI_YEREL=1 python3 -m streamlit run app.py --server.address localhost` çalıştır.

## 2. API anahtarı al

1. <https://aistudio.google.com> adresine Google hesabınla gir.
2. Sol menüden **Get API key** → **Create API key**.
3. Anahtarı oluştururken **yeni bir proje** seç/oluştur (örn. `sinif-asistani`).
   Bu iş için ayrı proje açmak önemli: kota ve olası faturalar diğer işlerinle karışmaz,
   bir sorun olursa sadece bu projeyi kapatırsın.
4. Anahtarı kopyala. **Kimseyle paylaşma, hiçbir dosyaya yazma, GitHub'a yükleme.**

## 3. Panelden kurulum

Uygulamada sol menüden **Yönetici Paneli**'ne tıkla (kendi bilgisayarında menü görünür;
internetteki uygulamada menü gizlidir, oraya linkin sonuna `/yonetici` ekleyerek girersin).
Adımları sırayla yap:

0. **Şifre belirle (ilk açılışta bir kez):** Panel ilk açılışta senden bir yönetici şifresi
   ister (en az 6 karakter, iki kez). Sonraki her girişte bu şifre sorulur. Şifre
   bilgisayarında açık metin olarak değil, geri çözülemez bir özet olarak saklanır.
   5 kez yanlış girilirse giriş 60 saniye kilitlenir. Şifreyi değiştirmek için:
   *⚙️ Kurulum → Yönetici şifresini değiştir*. Şifreni unutursan bu klasördeki
   `yonetici_sifresi.json` dosyasını sil; panel yeniden şifre belirlemeni ister.
1. **API anahtarı:** kopyaladığın anahtarı kutuya yapıştır → *Anahtarı kullan*.
   Anahtar hiçbir dosyaya yazılmaz, sadece uygulama açıkken hatırlanır. Uygulamayı
   kapatıp açınca tekrar yapıştırman gerekir (belgelerin silinmez).
2. **Bilgi deposu:** *Bilgi deposunu oluştur* düğmesine bas. Bir kez yapılır.
3. **(İsteğe bağlı)** `bilgiler.txt` dosyasını kendi bilgilerinle düzenleyip (içindeki
   tarihler örnektir!) *bilgiler.txt ve belgeler klasörünü yükle* düğmesine basabilirsin.
   Ya da bu adımı atlayıp belgelerini doğrudan *Belge yükle* sekmesinden ekle.

## 4. Bilgileri istediğin zaman güncelle

Kurulumdan sonra Yönetici Paneli'nde dört sekme var:

| Sekme | Ne yapar |
|---|---|
| 📎 **Belge yükle** | PDF / Word / TXT dosyası yükle. **Aynı dosya adıyla** tekrar yüklersen eskisinin yerine geçer. |
| ✍️ **Metin yaz** | Kısa bir bilgiyi elle yaz (örn. "Vize ertelendi"). **Aynı başlıkla** kaydedersen eskisinin yerine geçer. |
| 📚 **Kayıtlı belgeler** | Asistanın baktığı tüm belgeleri gör, yanlış/eski olanı sil. |
| ⚙️ **Kurulum** | Anahtar/depo durumu ve yayınlama için gereken Secrets metni. |

Yüklediğin belgeler Google'ın deposunda saklanır; uygulama kapansa veya yeniden
yayınlansa da kaybolmaz. Bir sınav tarihi değişince bilgiyi **hemen** güncelle;
asistan sadece depodakini bilir. Eski bir belgede yanlış tarih kaldıysa onu sil.

Yayına aldıktan sonra da aynı paneli **internetteki linkten** kullanabilirsin
(orada şifre sorar), yani bilgisayarını açmadan telefondan bile belge yükleyebilirsin.

## 5. Dene

Sol menüden **Sohbet** sayfasına dön:
- Bilgilerde **olan** bir şey sor (örn. vize tarihi) → cevap + altında kaynak adı görmelisin.
- Bilgilerde **olmayan** bir şey sor (örn. "Yemekhanede bugün ne var?") →
  *"Bu konuda bilgi bulamadım…"* demeli. **Yayınlamadan önce bunu mutlaka dene.**

## 6. İleri kullanıcılar için (isteğe bağlı)

- Varsayılan model `gemini-3.8-flash`. Değiştirmek için `GEMINI_MODEL` ayarını Secrets'a
  veya ortam değişkenine ekle. Model bulunamazsa uygulama hesabındaki başka bir flash
  modelini kendisi bulur; Google sunucuları yoğunsa kısa bekleyip tekrar dener.
- Bir sorun olursa ayrıntılar `hata_kaydi.txt` dosyasına yazılır (anahtar içermez).
- Panel yerine terminalden toplu yükleme: `GEMINI_API_KEY` ortam değişkenini tanımlayıp
  `python bilgi_yukle.py`. Bu, `belgeler/` klasöründen sildiğin dosyayı depodan silmez.
- Testler (API anahtarı gerekmez): `python -m unittest discover tests`

## 7. GitHub'a yükle ve Streamlit Community Cloud'da yayınla

1. <https://github.com> → **New repository** → ad ver (örn. `sinif-asistani`).
   Repo **Private** olabilir; Streamlit Cloud private repoları da yayınlayabilir.
2. Bu klasördeki dosyaları yükle (*Add file → Upload files* ile sürükle-bırak yeterli).
   `.gitignore` sayesinde `secrets.toml` yüklenmez; yine de yüklemeden önce hiçbir
   dosyada API anahtarın olmadığından emin ol.
3. <https://share.streamlit.io> → GitHub ile giriş yap → **Create app** →
   repoyu seç, *Main file path*: `app.py` (repo kökü bu klasör değilse `sinif_asistani/app.py`).
4. **Advanced settings → Secrets** kutusuna şunu yapıştır. Hazır halini Yönetici Paneli →
   **⚙️ Kurulum** sekmesinin en altında bulursun (depo adı orada dolu gelir); sadece
   anahtarı ve kendi seçtiğin şifreyi yaz. **Yayındaki panel bu şifreyle açılır.**

   ```toml
   GEMINI_API_KEY = "buraya-anahtarin"
   YONETICI_SIFRESI = "buraya-sifren"
   DEPO_ADI = "depo_adi.txt dosyasının içindeki değer"
   ```

5. **Deploy**. Birkaç dakika sonra `https://....streamlit.app` linkin hazır; bunu
   sınıf grubuna at. Herkes hesap açmadan kullanabilir.

Secrets'ı sonradan değiştirmek için: uygulama sayfası → **⋮ → Settings → Secrets**.

> Uygulama birkaç gün kimse girmezse "uyku"ya geçer; ilk giren kişi
> "Yes, get this app back up" düğmesine basınca bir dakika içinde açılır.

## 8. Ücretsiz katman sınırları — önemli

- Gemini API'nin ücretsiz katmanında **dakika başına ve gün başına istek sınırı** vardır.
  Güncel sayıları AI Studio'da projenin **Rate limits / Usage** sayfasından görebilirsin;
  ücretsiz katmanda bu sınırlar genelde dakikada birkaç on, günde birkaç yüz istek
  mertebesindedir ve Google zaman zaman değiştirir.
- Bu kota **senin API anahtarına** aittir; yani **tüm sınıf aynı kotayı paylaşır**.
  Sınav öncesi herkes aynı anda sorarsa sınır dolabilir.
- Sınır dolunca uygulama çökmez; soran kişiye *"Şu an çok fazla soru geldi… biraz sonra
  tekrar dene"* mesajı gösterilir. Dakikalık sınır bir dakika içinde, günlük sınır
  ertesi gün (Pasifik saatiyle gece yarısı) sıfırlanır.
- Arkadaşlarına "tek mesajda net soru sor" demek kotayı korur.

## 9. Kişisel veri uyarısı

Depoya **asla** şunları yükleme: öğrenci numaraları, not listeleri, TC kimlik no,
telefon numaraları, sağlık raporları veya herhangi bir kişiye ait özel bilgi.

- Uygulamayı linki bilen herkes kullanabilir; asistan depodaki her şeyi cevaplarında
  kullanabilir, yani yüklediğin bilgi **herkese açık** sayılmalıdır.
- Ücretsiz katmanda Google, gönderilen içerikleri ürünlerini geliştirmek için
  kullanabilir. Sadece herkese duyurulmuş genel bilgileri (takvim, yönetmelik, duyuru) yükle.

## 10. Faturalandırma (billing) açarsan

Ücretsiz kota yetmezse projede faturalandırmayı açabilirsin; bu durumda kullanım
**ücretli** olur. Açarsan mutlaka bütçe uyarısı kur:

1. <https://console.cloud.google.com> → doğru projeyi seç (`sinif-asistani`).
2. **Billing → Budgets & alerts → Create budget**.
3. Düşük bir tutar gir (örn. aylık 5 $) ve %50 / %90 / %100 e-posta uyarılarını aç.

Bütçe uyarısı harcamayı **durdurmaz**, sadece haber verir. Beklenmedik bir artış
görürsen API anahtarını AI Studio'dan silerek kullanımı hemen durdurabilirsin.
API anahtarın sızdığından şüphelenirsen de aynısını yap ve yeni anahtar oluştur
(yeni anahtarı Streamlit Secrets'a girmeyi unutma).

## Sorun giderme

| Mesaj | Çözüm |
|---|---|
| `GEMINI_API_KEY ayarı bulunamadı` | Adım 3'teki komutu bu terminalde çalıştırdın mı? Cloud'da Secrets'ı kontrol et. |
| `Henüz bilgi deposu oluşturulmamış` | `python bilgi_yukle.py` çalıştır; Cloud'da `DEPO_ADI` secret'ını gir. |
| `Depo okunamadı` | `depo_adi.txt` başka bir anahtarın projesine ait olabilir. Dosyayı silip `bilgi_yukle.py`'yi tekrar çalıştır (yeni depo oluşur). |
| Model bulunamadı (404) | `GEMINI_MODEL` ile güncel bir model adı ver (AI Studio'daki listeye bak). |
| Asistan bildiği bir şeye "bulamadım" diyor | Bilgiyi daha açık yaz, başlık ve "Soru:/Cevap:" örneği ekle, tekrar yükle. |
