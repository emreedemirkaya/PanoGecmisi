import json
import os
import re

import objc
import pyperclip
import rumps
from AppKit import NSPasteboard, NSSearchField
from Foundation import NSMakeRect, NSObject

DOSYA = os.path.expanduser("~/.pano_gecmisi.json")
MAX_KAYIT = 15

# ---------- Şifre filtresi ayarları ----------
SIFRE_FILTRESI = True      # False yaparsanız filtre kapanır
SIFRE_MIN_UZUNLUK = 8
SIFRE_MAX_UZUNLUK = 64
SIFRE_MIN_SINIF = 3        # küçük harf, BÜYÜK harf, rakam, sembol: en az kaçı varsa şifre say


def gizli_isaretli_mi():
    """Şifre yöneticileri (1Password, Bitwarden vb.) panoya 'gizli' işareti koyar."""
    try:
        turler = NSPasteboard.generalPasteboard().types() or []
        return (
            "org.nspasteboard.ConcealedType" in turler
            or "org.nspasteboard.TransientType" in turler
        )
    except Exception:
        return False


def sifre_gibi_mi(metin):
    """Tek kelime, boşluksuz, karışık karakterli 8+ uzunluktaki metinleri şifre sayar."""
    m = metin.strip()
    if not (SIFRE_MIN_UZUNLUK <= len(m) <= SIFRE_MAX_UZUNLUK):
        return False
    if any(c.isspace() for c in m):
        return False
    # Bağlantı, dosya yolu ve e-posta şifre sayılmasın
    if m.lower().startswith(("http://", "https://", "www.", "/", "~")):
        return False
    if re.fullmatch(r"[^@]+@[^@]+\.[^@]+", m):
        return False
    sinif = 0
    sinif += any(c.islower() for c in m)
    sinif += any(c.isupper() for c in m)
    sinif += any(c.isdigit() for c in m)
    sinif += any(not c.isalnum() for c in m)
    return sinif >= SIFRE_MIN_SINIF


class AramaHedefi(NSObject):
    """Arama kutusuna her harf yazıldığında çağrılır."""

    def initWithUygulama_(self, uygulama):
        self = objc.super(AramaHedefi, self).init()
        if self is None:
            return None
        self.uygulama = uygulama
        return self

    # Her harf yazıldığında / silindiğinde çalışır
    def controlTextDidChange_(self, bildirim):
        kutu = bildirim.object()
        self.uygulama.filtrele(kutu.stringValue())

    # Enter'a basılırsa da çalışsın (yedek)
    def aramaDegisti_(self, gonderen):
        self.uygulama.filtrele(gonderen.stringValue())


class PanoUygulamasi(rumps.App):
    def __init__(self):
        super().__init__("📋", quit_button=None)
        self.gecmis = self.yukle()
        self.son = pyperclip.paste()
        self.kayit_ogeleri = []   # (metin, MenuItem) çiftleri
        self.sonuc_yok = None
        self.hedef = AramaHedefi.alloc().initWithUygulama_(self)
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
            self.son = simdiki  # Atlansa bile hatırla
            if gizli_isaretli_mi():
                return
            if SIFRE_FILTRESI and sifre_gibi_mi(simdiki):
                return
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

        # En üstte arama kutusu
        self.arama_kutusu = NSSearchField.alloc().initWithFrame_(
            NSMakeRect(0, 0, 270, 24)
        )
        self.arama_kutusu.setPlaceholderString_("Ara…")
        self.arama_kutusu.setDelegate_(self.hedef)
        self.arama_kutusu.setTarget_(self.hedef)
        self.arama_kutusu.setAction_(b"aramaDegisti:")
        self.arama_kutusu.setSendsSearchStringImmediately_(True)

        arama_ogesi = rumps.MenuItem("arama")
        arama_ogesi._menuitem.setView_(self.arama_kutusu)
        ogeler.append(arama_ogesi)
        ogeler.append(rumps.separator)

        # Kayıtlar
        self.kayit_ogeleri = []
        for i, metin in enumerate(self.gecmis):
            onizleme = metin.replace("\n", " ").strip()
            if len(onizleme) > 50:
                onizleme = onizleme[:50] + "…"
            oge = rumps.MenuItem(
                f"{i + 1}. {onizleme}", callback=self.kopyala_fabrikasi(metin)
            )
            self.kayit_ogeleri.append((metin, oge))
            ogeler.append(oge)

        # "Sonuç yok" satırı (başta gizli)
        self.sonuc_yok = rumps.MenuItem(
            "(Henüz kayıt yok)" if not self.gecmis else "(Sonuç bulunamadı)"
        )
        self.sonuc_yok._menuitem.setHidden_(bool(self.gecmis))
        ogeler.append(self.sonuc_yok)

        ogeler.append(rumps.separator)
        ogeler.append(rumps.MenuItem("Geçmişi temizle", callback=self.temizle))
        ogeler.append(rumps.MenuItem("Çıkış", callback=rumps.quit_application))
        self.menu = ogeler

    def filtrele(self, aranan):
        """Yazılan kelimeyi içermeyen kayıtları gizler."""
        aranan = (aranan or "").strip().casefold()
        gorunen = 0
        for metin, oge in self.kayit_ogeleri:
            gorunur = (not aranan) or (aranan in metin.casefold())
            oge._menuitem.setHidden_(not gorunur)
            gorunen += gorunur

        if self.gecmis:
            self.sonuc_yok.title = "(Sonuç bulunamadı)"
            self.sonuc_yok._menuitem.setHidden_(gorunen > 0)

    def kopyala_fabrikasi(self, metin):
        def kopyala(_):
            pyperclip.copy(metin)
            self.son = metin
            self.ekle(metin)  # En başa taşır, menü yenilenir, arama sıfırlanır
            rumps.notification("Pano", "", "Panoya kopyalandı")

        return kopyala

    def temizle(self, _):
        self.gecmis = []
        self.kaydet()
        self.menuyu_yenile()


if __name__ == "__main__":
    PanoUygulamasi().run()