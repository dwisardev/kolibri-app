"""Compila los catalogos wxapp.po a wxapp.mo usando polib.

Reemplaza a `msgfmt` (que no existe en los runners de Windows). Los .mo estan
en .gitignore, asi que se generan antes de empaquetar con PyInstaller.
"""

import sys
from pathlib import Path

import polib


def main(root):
    count = 0
    for po_path in sorted(Path(root).glob("*/LC_MESSAGES/wxapp.po")):
        polib.pofile(str(po_path), encoding="utf-8").save_as_mofile(
            str(po_path.with_suffix(".mo"))
        )
        count += 1
    print("Compiled %d catalog(s)" % count)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "src/kolibri_app/locales")
