# 📋 Pano Geçmişi

macOS menü çubuğunda çalışan, kopyaladığınız son 15 metni saklayan hafif bir pano geçmişi uygulaması. Bir kayda tıklayınca metin tekrar panoya kopyalanır.

## Özellikler

- Menü çubuğunda çalışır, Dock'ta yer kaplamaz
- Son 15 kopyalamayı saklar
- Kayda tıklayınca metni panoya geri kopyalar
- Geçmiş yeniden başlatmada korunur
- Tek tıkla geçmişi temizleme

## Kurulum

```bash
git clone https://github.com/emreedemirkaya/PanoGecmisi.git
cd PanoGecmisi
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python pano.py
```

## .app olarak derleme

```bash
python setup.py py2app
```

Uygulama `dist/PanoGecmisi.app` olarak oluşur.

## Gizlilik

Kopyalanan metinler `~/.pano_gecmisi.json` dosyasına düz metin olarak kaydedilir. Şifre kopyaladıysanız menüden "Geçmişi temizle"yi kullanın.

## Lisans

MIT