import json
import os

import pyperclip
import rumps

# Geçmişin kaydedileceği dosya (ev klasöründe)
DOSYA = os.path.expanduser("~/.pano_gecmisi.json")
MAX_KAYIT = 15


class PanoUygulamasi(rumps.App):
    def __init__(self):
        # quit_button=None: Çıkış düğmesini kendimiz ekleyeceğiz
        super().__init__("📋", quit_button=None)
        self.gecmis = self.yukle()
        self.son = pyperclip.paste()
        self.menuyu_yenile()

        # Her 1 saniyede panoyu kontrol et
        self.zamanlayici = rumps.Timer(self.panoyu_kontrol_et, 1)
        self.zamanlayici.start()

    # ---------- Kayıt işlemleri ----------
    def yukle(self):
        try:
            with open(DOSYA, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def kaydet(self):
        with open(DOSYA, "w", encoding="utf-8") as f:
            json.dump(self.gecmis, f, ensure_ascii=False)

    # ---------- Pano takibi ----------
    def panoyu_kontrol_et(self, _):
        simdiki = pyperclip.paste()
        if simdiki and simdiki != self.son:
            self.son = simdiki
            self.ekle(simdiki)

    def ekle(self, metin):
        # Aynı metin varsa önce sil, sonra en başa ekle
        if metin in self.gecmis:
            self.gecmis.remove(metin)
        self.gecmis.insert(0, metin)
        self.gecmis = self.gecmis[:MAX_KAYIT]
        self.kaydet()
        self.menuyu_yenile()

    # ---------- Menü ----------
    def menuyu_yenile(self):
        self.menu.clear()
        ogeler = []

        if not self.gecmis:
            ogeler.append(rumps.MenuItem("(Henüz kayıt yok)"))

        for i, metin in enumerate(self.gecmis):
            # Menüde tek satır ve kısa görünsün
            onizleme = metin.replace("\n", " ").strip()
            if len(onizleme) > 50:
                onizleme = onizleme[:50] + "…"
            baslik = f"{i + 1}. {onizleme}"
            ogeler.append(
                rumps.MenuItem(baslik, callback=self.kopyala_fabrikasi(metin))
            )

        ogeler.append(rumps.separator)
        ogeler.append(rumps.MenuItem("Geçmişi temizle", callback=self.temizle))
        ogeler.append(rumps.MenuItem("Çıkış", callback=rumps.quit_application))
        self.menu = ogeler

    def kopyala_fabrikasi(self, metin):
        # Her menü öğesi kendi metnini hatırlasın diye iç fonksiyon döndürüyoruz
        def kopyala(_):
            pyperclip.copy(metin)
            self.son = metin
            self.ekle(metin)  # En başa taşı
            rumps.notification("Pano", "", "Panoya kopyalandı")

        return kopyala

    def temizle(self, _):
        self.gecmis = []
        self.kaydet()
        self.menuyu_yenile()


if __name__ == "__main__":
    PanoUygulamasi().run()