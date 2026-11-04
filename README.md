# 📋 Pano Geçmişi

macOS menü çubuğunda çalışan, kopyaladığınız son 15 metni saklayan hafif bir pano geçmişi uygulaması. Bir kayda tıklayınca metin tekrar panoya kopyalanır.

## Özellikler

- Menü çubuğunda çalışır, Dock'ta yer kaplamaz
- Son 15 kopyalamayı saklar, aynı metni tekrar eklemez
- Kayda tıklayınca metni panoya geri kopyalar
- **Canlı arama:** Menünün en üstündeki kutuya yazdıkça, içinde o kelime geçmeyen kayıtlar anında elenir (büyük/küçük harf duyarsız)
- **Şifre filtresi:** Şifre benzeri metinleri ve şifre yöneticilerinin (1Password, Bitwarden vb.) "gizli" işaretli kopyalamalarını kaydetmez
- Geçmiş yeniden başlatmada korunur
- Tek tıkla geçmişi temizleme

## Gereksinimler

- macOS
- Python 3.12 (python.org'dan kurulum önerilir)
- Kütüphaneler: `rumps`, `pyperclip`, `py2app` (PyObjC, `rumps` ile birlikte gelir)

> Not: Anaconda tabanlı bir ortamda `.app` derlemek `libffi` hatası verebilir. Derleme için python.org Python'u kullanın.

## Kurulum ve çalıştırma

```bash
git clone https://github.com/emreedemirkaya/PanoGecmisi.git
cd PanoGecmisi
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python pano.py
```

Menü çubuğunda 📋 simgesi görünür.

## Kullanım

- **Kopyalama geçmişi:** 📋 simgesine tıklayın, istediğiniz kayda basın; metin panoya geri kopyalanır.
- **Arama:** Menü açıkken üstteki kutuya yazmaya başlayın, liste harf harf daralır.
- **Temizleme:** Menünün altındaki **Geçmişi temizle** ile tüm kayıtları silin.

## Şifre filtresi nasıl çalışır?

İki katmanı vardır:

1. Şifre yöneticileri panoya "gizli" işareti koyar. Bu işaretli kopyalamalar hiç kaydedilmez.
2. Tek kelimeden oluşan, boşluksuz, 8-64 karakter uzunluğunda ve küçük harf, BÜYÜK harf, rakam, sembol türlerinden en az 3'ünü içeren metinler şifre sayılıp atlanır. Bağlantılar, dosya yolları ve e-posta adresleri filtrelenmez.

Ayarlar `pano.py` dosyasının üstündeki `SIFRE_*` değişkenlerinden değiştirilebilir. Filtreyi kapatmak için `SIFRE_FILTRESI = False` yazın.

## .app olarak derleme

```bash
rm -rf build dist
python setup.py py2app
mkdir -p ~/Applications
ditto dist/PanoGecmisi.app ~/Applications/PanoGecmisi.app
open ~/Applications/PanoGecmisi.app
```

İlk açılışta macOS uyarı verirse uygulamaya sağ tıklayıp **Aç**'ı seçin.

## Açılışta otomatik başlatma

Sistem Ayarları → Genel → Giriş Öğeleri → **+** → `PanoGecmisi.app`

## Proje yapısı

```
PanoGecmisi/
├── pano.py            # Ana uygulama
├── setup.py           # py2app derleme ayarları
├── simge.icns         # Uygulama simgesi
├── requirements.txt   # Bağımlılıklar
├── LICENSE
└── README.md
```

## Gizlilik

Kopyalanan metinler `~/.pano_gecmisi.json` dosyasına **düz metin** olarak kaydedilir. Veriler yalnızca bilgisayarınızda kalır, hiçbir yere gönderilmez. Şifre filtresi her şeyi yakalamayı garanti etmez; hassas bir şey kopyaladıysanız **Geçmişi temizle**'yi kullanın.

## Sorun giderme

| Sorun | Çözüm |
|---|---|
| `.app` açılıp kapanıyor | `~/Applications/PanoGecmisi.app/Contents/MacOS/PanoGecmisi` komutunu terminalde çalıştırıp hatayı okuyun |
| `Library not loaded: libffi` | Anaconda yerine python.org Python'uyla yeni venv kurun |
| Simge değişmedi | `touch` ile uygulamayı güncelleyip `killall Finder Dock` çalıştırın |
| Pano izni isteniyor | Sistem Ayarları → Gizlilik ve Güvenlik'ten izin verin |
| Arama kutusuna yazılamıyor | Menüyü kapatıp tekrar açın; sorun sürerse bir Issue açın |
