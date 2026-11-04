from setuptools import setup

APP = ["pano.py"]
OPTIONS = {
    "argv_emulation": False,
    "iconfile": "simge.icns",
    "plist": {
        "CFBundleName": "PanoGecmisi",
        "CFBundleDisplayName": "PanoGecmisi",
        "CFBundleIdentifier": "com.benim.panogecmisi",
        "CFBundleVersion": "1.0.0",
        "LSUIElement": True,
    },
    "packages": ["rumps", "objc", "AppKit", "Foundation"],
}

setup(
    app=APP,
    options={"py2app": OPTIONS},
)