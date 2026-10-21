"""El arranque de la app apaga la telemetria sin sobrescribir lo que defina el usuario."""

import os
import subprocess
import sys
import unittest

SRC = os.path.join(os.path.dirname(__file__), "..", "src")


def _valor_tras_importar(extra_env):
    env = {k: v for k, v in os.environ.items() if k != "KOLIBRI_DISABLE_PING"}
    env.update(extra_env)
    env["PYTHONPATH"] = SRC
    salida = subprocess.run(
        [
            sys.executable,
            "-c",
            # _version.py lo genera la compilacion; aqui se simula.
            "import os, sys, types; m = types.ModuleType('kolibri_app._version'); "
            "m.__version__ = '0'; sys.modules['kolibri_app._version'] = m; "
            "import kolibri_app; print(os.environ.get('KOLIBRI_DISABLE_PING'))",
        ],
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    return salida.stdout.strip()


class TestDisablePing(unittest.TestCase):
    def test_se_activa_por_defecto(self):
        self.assertEqual(_valor_tras_importar({}), "1")

    def test_respeta_un_valor_definido(self):
        self.assertEqual(_valor_tras_importar({"KOLIBRI_DISABLE_PING": "0"}), "0")
