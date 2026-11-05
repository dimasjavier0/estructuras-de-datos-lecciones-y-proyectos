"""Ejecutar desde la carpeta del proyecto: python -m unittest discover -s pruebas -v"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from grafos.grafo import GrafoDiccionario, GrafoTDA
from grafos.lista_enlazada import ListaEnlazada
from grafos.recorridos import bfs, camino_mas_corto, dfs, todos_los_caminos
from main import construir_mapa


class PruebaLista(unittest.TestCase):
    def test_agregar_sin_repetir_y_quitar(self):
        lista = ListaEnlazada()
        self.assertTrue(lista.agregar("a"))
        self.assertTrue(lista.agregar("b"))
        self.assertFalse(lista.agregar("a"))
        self.assertEqual(list(lista), ["a", "b"])
        self.assertTrue(lista.contiene("b"))
        self.assertTrue(lista.quitar("a"))
        self.assertFalse(lista.quitar("a"))
        self.assertEqual(len(lista), 1)
        self.assertTrue(lista.quitar("b"))
        self.assertEqual(list(lista), [])


class PruebaGrafoDiccionario(unittest.TestCase):
    def test_dirigido(self):
        g = GrafoDiccionario()
        g.agregar_arista("A", "B")
        self.assertEqual(g.vecinos("A"), ["B"])
        self.assertEqual(g.vecinos("B"), [])
        self.assertEqual(g.conectados_con("B"), ["A"])

    def test_no_dirigido_con_peso(self):
        g = GrafoDiccionario(dirigido=False)
        g.agregar_arista("A", "B", 5)
        self.assertEqual(g.peso("B", "A"), 5)

    def test_peso_negativo(self):
        with self.assertRaises(ValueError):
            GrafoDiccionario().agregar_arista("A", "B", -1)

    def test_eliminar_vertice_quita_aristas_entrantes(self):
        g = GrafoDiccionario()
        g.agregar_arista("A", "B")
        g.agregar_arista("C", "B")
        self.assertTrue(g.eliminar_vertice("B"))
        self.assertFalse(g.eliminar_vertice("B"))
        self.assertEqual(g.vecinos("A"), [])
        self.assertEqual(g.vertices(), ["A", "C"])


class PruebaGrafoTDA(unittest.TestCase):
    def setUp(self):
        self.g = GrafoTDA()
        for v in "ABC":
            self.g.agregar_vertice(v)

    def test_operaciones(self):
        self.assertFalse(self.g.agregar_vertice("A"))
        self.assertTrue(self.g.agregar_arista("A", "B"))
        self.assertFalse(self.g.agregar_arista("A", "B"))
        self.g.agregar_arista("C", "B")
        self.assertEqual(self.g.vecinos("A"), ["B"])
        self.assertTrue(self.g.eliminar_vertice("B"))
        self.assertFalse(self.g.eliminar_vertice("B"))
        self.assertEqual(self.g.vecinos("A"), [])
        self.assertEqual(self.g.vertices(), ["A", "C"])

    def test_errores(self):
        with self.assertRaises(KeyError):
            self.g.agregar_arista("A", "Z")
        with self.assertRaises(KeyError):
            self.g.vecinos("Z")


class PruebaRecorridos(unittest.TestCase):
    def setUp(self):
        self.mapa = construir_mapa()

    def test_bfs_y_dfs(self):
        self.assertEqual(bfs(self.mapa, "Estadio"), ["Estadio", "Teatro", "Museo", "Parque", "Biblioteca"])
        self.assertEqual(dfs(self.mapa, "Estadio"), ["Estadio", "Teatro", "Museo", "Biblioteca", "Parque"])

    def test_todos_los_caminos(self):
        caminos = todos_los_caminos(self.mapa, "Biblioteca", "Estadio")
        self.assertCountEqual(caminos, [
            ["Biblioteca", "Museo", "Teatro", "Estadio"],
            ["Biblioteca", "Museo", "Parque", "Teatro", "Estadio"],
            ["Biblioteca", "Parque", "Teatro", "Estadio"],
            ["Biblioteca", "Parque", "Museo", "Teatro", "Estadio"],
        ])

    def test_dijkstra_elige_mas_saltos_si_es_mas_corto(self):
        self.assertEqual(camino_mas_corto(self.mapa, "Biblioteca", "Parque"), (3, ["Biblioteca", "Museo", "Parque"]))
        self.assertEqual(camino_mas_corto(self.mapa, "Biblioteca", "Estadio")[0], 8)

    def test_dijkstra_coincide_con_fuerza_bruta(self):
        for origen in self.mapa.vertices():
            for destino in self.mapa.vertices():
                if origen != destino:
                    caminos = todos_los_caminos(self.mapa, origen, destino)
                    menor = min(sum(self.mapa.peso(a, b) for a, b in zip(c, c[1:])) for c in caminos)
                    self.assertEqual(camino_mas_corto(self.mapa, origen, destino)[0], menor)

    def test_sin_camino(self):
        g = GrafoDiccionario()
        g.agregar_arista("A", "B")
        g.agregar_vertice("Z")
        self.assertEqual(todos_los_caminos(g, "A", "Z"), [])
        self.assertEqual(camino_mas_corto(g, "A", "Z"), (None, []))

    def test_ciclos_no_cuelgan_el_recorrido(self):
        g = GrafoDiccionario()
        g.agregar_arista("A", "B")
        g.agregar_arista("B", "A")
        self.assertEqual(bfs(g, "A"), ["A", "B"])
        self.assertEqual(dfs(g, "A"), ["A", "B"])


if __name__ == "__main__":
    unittest.main()
