"""Ejecutar desde la carpeta del proyecto: python -m unittest discover -s pruebas -v"""
import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from cifrado import cesar, cifrar_texto, descifrar_texto, xor_bytes
from main import main


class PruebaCesar(unittest.TestCase):
    def test_desplaza_y_conserva_lo_demas(self):
        self.assertEqual(cesar("abc XYZ, 123!", 1), "bcd YZA, 123!")
        self.assertEqual(cesar("ñ", 1), "o")
        self.assertEqual(cesar("z", 1), "a")

    def test_ida_y_vuelta(self):
        for d in (0, 3, 27, 100, -5):
            self.assertEqual(cesar(cesar("Mañana salimos", d), -d), "Mañana salimos")


class PruebaXor(unittest.TestCase):
    def test_a_mano(self):
        # 'a' = 0x61, 'b' = 0x62: 0x61 ^ 0x62 = 0x03
        self.assertEqual(xor_bytes(b"a", b"b"), b"\x03")

    def test_la_clave_se_repite(self):
        self.assertEqual(xor_bytes(b"\x00\x00\x00", b"\x01\x02"), b"\x01\x02\x01")

    def test_ida_y_vuelta_con_acentos(self):
        for texto in ("Hola mundo", "¿Mañana? ñandú 🙂", ""):
            for clave in ("z", "clave larga", "ñ"):
                self.assertEqual(descifrar_texto(cifrar_texto(texto, clave), clave), texto)

    def test_errores(self):
        with self.assertRaises(ValueError):
            xor_bytes(b"x", b"")
        with self.assertRaises(ValueError):
            cifrar_texto("x", "")
        with self.assertRaisesRegex(ValueError, "hexadecimal"):
            descifrar_texto("no es hex", "clave")
        with self.assertRaisesRegex(ValueError, "incorrecta"):
            descifrar_texto(cifrar_texto("ñandú", "a"), "éé")


class PruebaPrograma(unittest.TestCase):
    def correr(self, *argumentos):
        salida, errores = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(salida), contextlib.redirect_stderr(errores):
            codigo = main(list(argumentos))
        return codigo, salida.getvalue().strip(), errores.getvalue().strip()

    def test_cesar(self):
        self.assertEqual(self.correr("cesar", "abc", "1"), (0, "bcd", ""))

    def test_cifrar_y_descifrar(self):
        _, cifrado, _ = self.correr("cifrar", "Hola", "k")
        self.assertEqual(self.correr("descifrar", cifrado, "k"), (0, "Hola", ""))

    def test_archivo_binario_ida_y_vuelta(self):
        with tempfile.TemporaryDirectory() as carpeta:
            entrada = os.path.join(carpeta, "a.bin")
            cifrado = os.path.join(carpeta, "b.bin")
            final = os.path.join(carpeta, "c.bin")
            Path(entrada).write_bytes(bytes(range(256)))
            self.assertEqual(self.correr("archivo", entrada, cifrado, "k")[0], 0)
            self.assertNotEqual(Path(cifrado).read_bytes(), bytes(range(256)))
            self.correr("archivo", cifrado, final, "k")
            self.assertEqual(Path(final).read_bytes(), bytes(range(256)))

    def test_errores_devuelven_codigo_1(self):
        self.assertEqual(self.correr("descifrar", "zz", "k")[0], 1)
        self.assertEqual(self.correr("cifrar", "a", "")[0], 1)
        codigo, _, error = self.correr("archivo", "no-existe.bin", "x.bin", "k")
        self.assertEqual(codigo, 1)
        self.assertIn("Error", error)


if __name__ == "__main__":
    unittest.main()
