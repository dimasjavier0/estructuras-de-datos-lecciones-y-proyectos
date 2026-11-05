"""Ejecutar desde la carpeta del proyecto: python -m unittest discover -s pruebas -v"""
import os
import sys
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from PyQt5.QtWidgets import QApplication, QMessageBox

from main import EJEMPLO, VentanaRed
from red.lector import ErrorDeFormato, leer_red
from red.modelo import Enlace, Red
from red.rutas import mejor_ruta, todas_las_rutas

app = QApplication.instance() or QApplication([])
DATOS = "distancia=100 capacidad=100 usuarios=0 trafico=0 medio=fibra"


def red_de(*lineas):
    return leer_red("\n".join(f"{linea} : {DATOS}" for linea in lineas))


class PruebaEnlace(unittest.TestCase):
    def test_costo_calculado_a_mano(self):
        e = Enlace("A", "B", distancia=200, capacidad=100, usuarios=50, trafico=25, medio="wifi")
        # 200/100 + 10*0.25 + 20*(1-0.80) + 50/100 = 2 + 2.5 + 4 + 0.5
        self.assertEqual(e.costo, 9.0)
        self.assertEqual(e.disponible, 75)

    def test_enlace_saturado_no_da_disponible_negativo(self):
        self.assertEqual(Enlace("A", "B", 10, 10, 0, 50, "cat6").disponible, 0)


class PruebaLector(unittest.TestCase):
    def test_flechas_comentarios_y_lineas_vacias(self):
        red = leer_red(f"# comentario\n\nA -> B : {DATOS}  # fin\nB <-> C : {DATOS}\n")
        self.assertEqual(red.servidores(), ["A", "B", "C"])
        self.assertEqual(red.vecinos("A"), ["B"])
        self.assertEqual(red.vecinos("B"), ["C"])
        self.assertEqual(red.vecinos("C"), ["B"])

    def test_errores_indican_la_linea(self):
        casos = {
            "": "ningún enlace",
            "# solo comentario": "ningún enlace",
            "esto no sirve": "Línea 1",
            f"A -> A : {DATOS}": "consigo mismo",
            f"A -> B : {DATOS}\nA -> B : {DATOS}": "Línea 2: el enlace A -> B está repetido",
            f"A <-> B : {DATOS}\nB -> A : {DATOS}": "repetido",
            "A -> B : distancia=1": "faltan datos",
            f"A -> B : {DATOS} extra=1": "desconocidos",
            "A -> B : distancia=x capacidad=1 usuarios=0 trafico=0 medio=fibra": "distancia debe ser",
            "A -> B : distancia=-1 capacidad=1 usuarios=0 trafico=0 medio=fibra": "distancia debe ser",
            "A -> B : distancia=0 capacidad=1 usuarios=0 trafico=0 medio=fibra": "mayores que 0",
            "A -> B : distancia=1 capacidad=0 usuarios=0 trafico=0 medio=fibra": "mayores que 0",
            "A -> B : distancia=1 capacidad=1 usuarios=0 trafico=0 medio=humo": "medio desconocido",
            "A -> B : distancia=101 capacidad=1 usuarios=0 trafico=0 medio=wifi": "alcanza 100",
            "A -> B : distancia": "nombre=valor",
        }
        for texto, esperado in casos.items():
            with self.assertRaises(ErrorDeFormato, msg=texto) as contexto:
                leer_red(texto)
            self.assertIn(esperado, str(contexto.exception), texto)

    def test_ejemplo_incluido_se_puede_leer(self):
        red = leer_red(EJEMPLO.read_text(encoding="utf-8"))
        self.assertIn("Datos", red)
        self.assertEqual(len(red.servidores()), 6)


class PruebaRutas(unittest.TestCase):
    def test_todas_las_rutas_sin_ciclos(self):
        red = red_de("A -> B", "B -> C", "A -> C", "C -> A", "B -> D", "C -> D")
        rutas = [r.servidores for r in todas_las_rutas(red, "A", "D")]
        self.assertCountEqual(rutas, [("A", "B", "D"), ("A", "C", "D"), ("A", "B", "C", "D")])
        for ruta in rutas:
            self.assertEqual(len(ruta), len(set(ruta)))

    def test_sin_camino(self):
        red = red_de("A -> B", "C -> D")
        self.assertEqual(todas_las_rutas(red, "A", "D"), [])
        self.assertIsNone(mejor_ruta(red, "A", "D"))

    def test_camino_barato_con_mas_saltos_gana(self):
        red = Red()
        red.agregar_enlace(Enlace("A", "C", 30000, 100, 0, 0, "fibra"))  # muy largo
        red.agregar_enlace(Enlace("A", "B", 10, 100, 0, 0, "fibra"))
        red.agregar_enlace(Enlace("B", "C", 10, 100, 0, 0, "fibra"))
        self.assertEqual(mejor_ruta(red, "A", "C").servidores, ("A", "B", "C"))

    def test_disponible_es_el_cuello_de_botella(self):
        red = Red()
        red.agregar_enlace(Enlace("A", "B", 10, 1000, 0, 100, "fibra"))
        red.agregar_enlace(Enlace("B", "C", 10, 100, 0, 90, "fibra"))
        self.assertEqual(mejor_ruta(red, "A", "C").disponible, 10)

    def test_dijkstra_coincide_con_la_fuerza_bruta(self):
        red = leer_red(EJEMPLO.read_text(encoding="utf-8"))
        for origen in red.servidores():
            for destino in red.servidores():
                if origen == destino:
                    continue
                rutas = todas_las_rutas(red, origen, destino)
                mejor = mejor_ruta(red, origen, destino)
                if rutas:
                    self.assertEqual(mejor.costo, rutas[0].costo, (origen, destino))
                else:
                    self.assertIsNone(mejor, (origen, destino))


class PruebaVentana(unittest.TestCase):
    def setUp(self):
        self.ventana = VentanaRed()
        self.avisos = []
        self.ventana.avisar = self.avisos.append

    def tearDown(self):
        self.ventana.close()

    def test_flujo_completo_con_el_ejemplo(self):
        self.assertFalse(self.ventana.boton_rutas.isEnabled())
        self.ventana.boton_leer.click()
        self.assertEqual(self.avisos, [])
        self.assertTrue(self.ventana.boton_rutas.isEnabled())
        self.ventana.origen.setCurrentText("Internet")
        self.ventana.destino.setCurrentText("Datos")
        self.ventana.boton_rutas.click()
        self.assertIn("Mejor ruta: Internet → Firewall", self.ventana.resultado.text())
        self.assertGreater(self.ventana.tabla.rowCount(), 1)
        costos = [float(self.ventana.tabla.item(f, 2).text()) for f in range(self.ventana.tabla.rowCount())]
        self.assertEqual(costos, sorted(costos))

    def test_texto_invalido_limpia_el_estado_anterior(self):
        self.ventana.boton_leer.click()
        self.ventana.boton_rutas.click()
        self.ventana.texto.setPlainText("no es una red")
        self.ventana.boton_leer.click()
        self.assertIn("Línea 1", self.avisos[-1])
        self.assertFalse(self.ventana.boton_rutas.isEnabled())
        self.assertEqual(self.ventana.origen.count(), 0)
        self.assertEqual(self.ventana.tabla.rowCount(), 0)

    def test_mismo_origen_y_destino(self):
        self.ventana.boton_leer.click()
        self.ventana.destino.setCurrentIndex(self.ventana.origen.currentIndex())
        self.ventana.boton_rutas.click()
        self.assertIn("distintos", self.avisos[-1])

    def test_servidores_sin_conexion(self):
        self.ventana.texto.setPlainText(f"A -> B : {DATOS}\nC -> D : {DATOS}")
        self.ventana.boton_leer.click()
        self.ventana.origen.setCurrentText("A")
        self.ventana.destino.setCurrentText("D")
        self.ventana.boton_rutas.click()
        self.assertIn("No hay ninguna ruta", self.ventana.resultado.text())
        self.assertEqual(self.ventana.tabla.rowCount(), 0)

    def test_archivo_inexistente(self):
        self.ventana.abrir_archivo("no-existe.txt")
        self.assertIn("No se pudo leer", self.avisos[-1])


if __name__ == "__main__":
    unittest.main()
