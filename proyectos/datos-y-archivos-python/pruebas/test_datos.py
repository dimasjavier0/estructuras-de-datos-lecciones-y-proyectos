"""Ejecutar desde la carpeta del proyecto: python -m unittest discover -s pruebas -v"""
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from datos import a_lista_html, arbol_a_html, arbol_a_texto, contar_hojas, generar_csv, leer_tabla

EJEMPLOS = Path(__file__).resolve().parent.parent / "ejemplos"


class PruebaTablas(unittest.TestCase):
    def test_csv_y_tsv_dan_lo_mismo(self):
        self.assertEqual(leer_tabla(EJEMPLOS / "productos.csv"), leer_tabla(EJEMPLOS / "productos.tsv"))
        self.assertEqual(leer_tabla(EJEMPLOS / "productos.csv")[0], ["producto", "precio", "cantidad"])

    def test_extension_desconocida(self):
        for ruta in ("datos.txt", "sin-extension"):
            with self.assertRaisesRegex(ValueError, "Extensión"):
                leer_tabla(ruta)

    def test_archivo_inexistente_y_vacio(self):
        with self.assertRaises(FileNotFoundError):
            leer_tabla("no-existe.csv")
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = os.path.join(carpeta, "vacio.csv")
            open(ruta, "w").close()
            self.assertEqual(leer_tabla(ruta), [])


class PruebaGenerador(unittest.TestCase):
    def test_tamano_y_rango(self):
        filas = generar_csv(4, 3, semilla=1, minimo=5, maximo=9).splitlines()
        self.assertEqual(len(filas), 4)
        for fila in filas:
            valores = [int(v) for v in fila.split(",")]
            self.assertEqual(len(valores), 3)
            self.assertTrue(all(5 <= v <= 9 for v in valores))

    def test_semilla_reproducible(self):
        self.assertEqual(generar_csv(3, 3, semilla=7), generar_csv(3, 3, semilla=7))
        self.assertNotEqual(generar_csv(3, 3, semilla=7), generar_csv(3, 3, semilla=8))

    def test_argumentos_invalidos(self):
        for args in ((0, 1), (1, 0), (-1, 1)):
            with self.assertRaises(ValueError):
                generar_csv(*args)
        with self.assertRaises(ValueError):
            generar_csv(1, 1, minimo=2, maximo=1)

    def test_lo_generado_se_puede_leer(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "a.csv"
            ruta.write_text(generar_csv(2, 2, semilla=1), encoding="utf-8")
            self.assertEqual(len(leer_tabla(ruta)), 2)


class PruebaArboles(unittest.TestCase):
    ARBOL = {"root": {"a": {"x": 1}, "b": {}, "c": 2}}

    def test_lista_html_anidada(self):
        self.assertEqual(a_lista_html([1, [2]]), "<ul><li>1</li><li><ul><li>2</li></ul></li></ul>")
        self.assertEqual(a_lista_html([]), "<ul></ul>")

    def test_arbol_a_html(self):
        self.assertEqual(
            arbol_a_html(self.ARBOL),
            "<ul><li>root<ul><li>a<ul><li>x: 1</li></ul></li><li>b</li><li>c: 2</li></ul></li></ul>",
        )

    def test_el_html_se_escapa(self):
        self.assertNotIn("<script>", a_lista_html(["<script>alert(1)</script>"]))
        self.assertNotIn("<b>", arbol_a_html({"<b>": "<b>"}))

    def test_arbol_a_texto(self):
        self.assertEqual(arbol_a_texto(self.ARBOL), ["root", "    a", "        x: 1", "    b", "    c: 2"])

    def test_contar_hojas(self):
        self.assertEqual(contar_hojas(self.ARBOL), 2)
        self.assertEqual(contar_hojas({}), 0)


if __name__ == "__main__":
    unittest.main()
