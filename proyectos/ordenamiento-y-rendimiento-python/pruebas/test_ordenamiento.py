"""Ejecutar desde la carpeta del proyecto: python -m unittest discover -s pruebas -v"""
import contextlib
import io
import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ordenamientos import ALGORITMOS, Contador, burbuja, insercion, seleccion
from rendimiento import main, medir, tabla


class PruebaAlgoritmos(unittest.TestCase):
    def test_casos_borde(self):
        for nombre, algoritmo in ALGORITMOS.items():
            for datos in ([], [1], [2, 1], [1, 2], [3, 3, 3], [5, -1, 0, -1, 5], ["b", "a", "c"]):
                self.assertEqual(algoritmo(datos), sorted(datos), (nombre, datos))

    def test_datos_aleatorios(self):
        azar = random.Random(1)
        for _ in range(100):
            datos = [azar.randrange(50) for _ in range(azar.randrange(60))]
            for nombre, algoritmo in ALGORITMOS.items():
                self.assertEqual(algoritmo(datos), sorted(datos), nombre)

    def test_no_modifica_la_lista_original(self):
        for algoritmo in ALGORITMOS.values():
            datos = [3, 1, 2]
            algoritmo(datos)
            self.assertEqual(datos, [3, 1, 2])


class PruebaComplejidad(unittest.TestCase):
    def comparaciones(self, algoritmo, datos):
        contador = Contador()
        algoritmo(datos, contador)
        return contador.comparaciones

    def test_seleccion_hace_exactamente_n_por_n_menos_1_entre_2(self):
        self.assertEqual(self.comparaciones(seleccion, list(range(100))), 100 * 99 // 2)

    def test_burbuja_e_insercion_son_lineales_si_ya_esta_ordenado(self):
        self.assertEqual(self.comparaciones(burbuja, list(range(100))), 99)
        self.assertEqual(self.comparaciones(insercion, list(range(100))), 99)

    def test_insercion_es_cuadratica_si_esta_invertido(self):
        self.assertEqual(self.comparaciones(insercion, list(range(100, 0, -1))), 100 * 99 // 2)

    def test_al_multiplicar_n_por_10_crecen_como_predice_la_notacion_o(self):
        azar = random.Random(5)
        pequena = [azar.random() for _ in range(300)]
        grande = [azar.random() for _ in range(3000)]
        razon = lambda a: self.comparaciones(a, grande) / self.comparaciones(a, pequena)
        self.assertGreater(razon(seleccion), 90)                # n²: unas 100 veces
        self.assertLess(razon(ALGORITMOS["mezcla"]), 20)        # n log n: unas 14 veces
        self.assertLess(razon(ALGORITMOS["quicksort"]), 20)


class PruebaRendimiento(unittest.TestCase):
    def test_medir_detecta_un_algoritmo_incorrecto(self):
        def roto(datos, contador):
            return list(datos)
        with self.assertRaises(AssertionError):
            medir(roto, [2, 1])

    def test_tabla_es_reproducible(self):
        a = [fila[:3] for fila in tabla([50], "aleatorio", 7)]
        b = [fila[:3] for fila in tabla([50], "aleatorio", 7)]
        self.assertEqual(a, b)
        self.assertEqual(len(a), len(ALGORITMOS))

    def test_programa(self):
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            main(["--tamanos", "20", "--caso", "invertido"])
        self.assertIn("Caso: invertido", salida.getvalue())
        self.assertIn("quicksort", salida.getvalue())

    def test_argumentos_invalidos(self):
        for argumentos in (["--tamanos", "0"], ["--tamanos", "x"], ["--caso", "otro"]):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                main(argumentos)


if __name__ == "__main__":
    unittest.main()
