"""Pruebas del núcleo y de la interfaz. Ejecutar desde la carpeta del proyecto:
    python -m unittest discover -s pruebas -v
Corren sin ventana visible y usan una carpeta temporal: no tocan Memoria/.
"""
import os
import sys
import tempfile
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMessageBox

from main import ACTUAL, ARRIBA, GUISistemaArchivo
from Nucleo.Clases.comparar import Compare
from Nucleo.Clases.GenericTree import Tree
from Nucleo.Clases.Lista import List
from Nucleo.Clases.TXT import ErrorMemoria, GestionTree

app = QApplication.instance() or QApplication([])


class PruebaCompare(unittest.TestCase):
    def test_orden(self):
        c = Compare()
        self.assertEqual(c.compare("a", "a"), 0)
        self.assertEqual(c.compare("a", "b"), -1)
        self.assertEqual(c.compare("b", "a"), 1)
        self.assertEqual(c.compare("a", "A"), -1)
        self.assertEqual(c.compare("Hola", "HolaMundo"), -1)
        self.assertEqual(c.compare(10, "9"), -1)

    def test_letras_fuera_del_alfabeto_no_fallan(self):
        c = Compare()
        self.assertEqual(c.compare("año ñ", "año ñ"), 0)
        self.assertEqual(c.compare("z", "é"), -1)


class PruebaLista(unittest.TestCase):
    def test_ordena_y_no_repite(self):
        lista = List()
        for nombre in ["c", "a", "d", "b"]:
            self.assertTrue(lista.add(nombre))
        self.assertFalse(lista.add("b"))
        self.assertEqual([n.name for n in lista.toArray()], ["a", "b", "c", "d"])
        self.assertEqual(len(lista), 4)

    def test_buscar_indice_y_quitar(self):
        lista = List()
        for nombre in ["a", "b", "c"]:
            lista.add(nombre)
        self.assertEqual(lista.searchName("b").name, "b")
        self.assertIsNone(lista.searchName("x"))
        self.assertEqual(lista._index(2).name, "c")
        self.assertIsNone(lista._index(3))
        self.assertTrue(lista.popName("a"))   # primero
        self.assertTrue(lista.popName("c"))   # último
        self.assertFalse(lista.popName("x"))
        self.assertEqual([n.name for n in lista.toArray()], ["b"])
        self.assertTrue(lista.popName("b"))
        self.assertIsNone(lista.first)
        self.assertFalse(lista.popName("b"))  # lista vacía

    def test_addnode_rechaza_lo_que_no_es_nodo(self):
        self.assertFalse(List().addNode("texto"))


class PruebaTree(unittest.TestCase):
    def setUp(self):
        self.tree = Tree()
        self.docs = self.tree.TreeaddFolder("Documentos")
        self.notas = self.tree.TreeaddFile("notas", self.docs)

    def test_agregar_y_ruta(self):
        self.assertEqual(self.docs.name, "Documentos/")
        self.assertEqual(self.notas.name, "notas.txt")
        self.assertEqual(self.tree.ruta(self.notas), "root/Documentos/notas.txt")

    def test_no_duplica_txt_ni_nombres(self):
        self.assertEqual(self.tree.TreeaddFile("otro.txt").name, "otro.txt")
        self.assertIsNone(self.tree.TreeaddFile("notas", self.docs))
        self.assertIsNone(self.tree.TreeaddFolder("Documentos"))

    def test_nombres_invalidos(self):
        for nombre in ["", "   ", ".", "..", "a/b", "a\\b", "a\tb"]:
            self.assertIsNone(self.tree.TreeaddFolder(nombre), nombre)
            self.assertIsNone(self.tree.TreeaddFile(nombre), nombre)

    def test_no_agrega_dentro_de_un_archivo(self):
        self.assertIsNone(self.tree.TreeaddFile("x", self.notas))
        self.assertIsNone(self.tree.TreeaddFolder("x", self.notas))

    def test_eliminar_carpeta_con_contenido(self):
        self.assertTrue(self.tree.TreepopName("Documentos/"))
        self.assertIsNone(self.tree.TreesearchName("Documentos/"))
        self.assertFalse(self.tree.TreepopName("Documentos/"))

    def test_copia_profunda_independiente(self):
        destino = Tree()
        copia = destino.Copy(self.docs, destino.root)
        self.assertEqual(destino.show(), "root/\n\tDocumentos/\n\t\tnotas.txt\n")
        self.assertIs(copia.parent, destino.root)
        destino.TreepopName("notas.txt", copia)
        self.assertIsNotNone(self.tree.TreesearchName("notas.txt", self.docs))

    def test_copia_rechaza_repetido_y_dentro_de_si_misma(self):
        destino = Tree()
        self.assertIsNotNone(destino.Copy(self.docs, destino.root))
        self.assertIsNone(destino.Copy(self.docs, destino.root))
        self.assertIsNone(self.tree.Copy(self.docs, self.docs))


class PruebaMemoria(unittest.TestCase):
    def test_guardar_y_cargar(self):
        tree = Tree()
        a = tree.TreeaddFolder("A")
        b = tree.TreeaddFolder("B", a)
        tree.TreeaddFile("uno", b)
        tree.TreeaddFile("dos", a)
        tree.TreeaddFolder("vacia")
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = os.path.join(carpeta, "t.mem")
            GestionTree().Guardar(tree, ruta)
            cargado = GestionTree().Cargar(ruta)
        self.assertEqual(cargado.show(), tree.show())
        self.assertIs(cargado.root.children.searchName("A/").parent, cargado.root)

    def test_vacio_o_inexistente(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = os.path.join(carpeta, "t.mem")
            self.assertEqual(GestionTree().Cargar(ruta).show(), "root/\n")
            open(ruta, "w").close()
            self.assertEqual(GestionTree().Cargar(ruta).show(), "root/\n")

    def test_contenido_invalido(self):
        for lineas in (["otra/"], ["root/", "\t\t\tprofundo.txt"], ["root/", "sin-tab.txt"], ["root/", "\ta", "\ta"]):
            with self.assertRaises(ErrorMemoria, msg=lineas):
                GestionTree().textoATree(lineas)

    def test_archivo_dentro_de_archivo_es_invalido(self):
        with self.assertRaises(ErrorMemoria):
            GestionTree().textoATree(["root/", "\ta.txt", "\t\tb.txt"])


class PruebaInterfaz(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.gui = GUISistemaArchivo(self.temporal.name)

    def tearDown(self):
        self.gui.close()
        self.temporal.cleanup()

    def responder(self, dialogo, entrada, boton, texto):
        def escribir():
            entrada.setText(texto)
            boton.click()
        QTimer.singleShot(0, escribir)

    def carpeta(self, boton, texto):
        d = self.gui.dialogoCarpeta
        self.responder(d, d.InputTextFile, d.AcceptButtonFile_1, texto)
        boton.click()

    def archivo(self, boton, texto):
        d = self.gui.dialogoArchivo
        self.responder(d, d.InputTextArchive, d.AcceptButtonArchive_1, texto)
        boton.click()

    def textos(self, lista):
        return [lista.item(i).text() for i in range(lista.count())]

    def item(self, lista, texto):
        return lista.findItems(texto, Qt.MatchExactly)[0]

    def test_inicio_vacio(self):
        self.assertEqual(self.textos(self.gui.ListTree_1), [ACTUAL, ARRIBA])
        self.assertEqual(self.gui.label.text(), "Memoria A: root/")
        self.assertEqual(self.gui.label_3.text(), "Memoria B: root/")

    def test_crear_navegar_y_regresar(self):
        self.carpeta(self.gui.AddFileButton_1, "Fotos")
        self.archivo(self.gui.AddArchiveButton_1, "leeme")
        # El alfabeto de Compare pone las minúsculas antes que las mayúsculas
        self.assertEqual(self.textos(self.gui.ListTree_1), [ACTUAL, ARRIBA, "leeme.txt", "Fotos/"])

        self.gui.abrir(self.gui.panelA, self.item(self.gui.ListTree_1, "Fotos/"))
        self.assertEqual(self.gui.label.text(), "Memoria A: root/Fotos/")
        self.archivo(self.gui.AddArchiveButton_1, "playa")
        self.assertEqual(self.textos(self.gui.ListTree_1), [ACTUAL, ARRIBA, "playa.txt"])

        self.gui.abrir(self.gui.panelA, self.item(self.gui.ListTree_1, ACTUAL))
        self.assertEqual(self.gui.label.text(), "Memoria A: root/Fotos/")
        self.gui.abrir(self.gui.panelA, self.item(self.gui.ListTree_1, ARRIBA))
        self.assertEqual(self.gui.label.text(), "Memoria A: root/")
        self.gui.abrir(self.gui.panelA, self.item(self.gui.ListTree_1, ARRIBA))
        self.assertIn("raíz", self.gui.statusbar.currentMessage())

    def test_doble_clic_en_archivo_no_cambia_de_carpeta(self):
        self.archivo(self.gui.AddArchiveButton_1, "uno")
        self.gui.abrir(self.gui.panelA, self.item(self.gui.ListTree_1, "uno.txt"))
        self.assertEqual(self.gui.label.text(), "Memoria A: root/")
        self.assertIn("es un archivo", self.gui.statusbar.currentMessage())

    def test_errores_de_nombre(self):
        self.carpeta(self.gui.AddFileButton_1, "   ")
        self.assertIn("inválido", self.gui.statusbar.currentMessage())
        self.carpeta(self.gui.AddFileButton_1, "a/b")
        self.assertIn("inválido", self.gui.statusbar.currentMessage())
        self.carpeta(self.gui.AddFileButton_1, "Fotos")
        self.carpeta(self.gui.AddFileButton_1, "Fotos")
        self.assertIn("Ya existe", self.gui.statusbar.currentMessage())
        self.assertEqual(self.textos(self.gui.ListTree_1), [ACTUAL, ARRIBA, "Fotos/"])

    def test_cancelar_dialogo_no_crea(self):
        QTimer.singleShot(0, self.gui.dialogoCarpeta.reject)
        self.gui.AddFileButton_1.click()
        self.assertEqual(self.textos(self.gui.ListTree_1), [ACTUAL, ARRIBA])

    def test_eliminar(self):
        self.carpeta(self.gui.AddFileButton_2, "Fotos")
        self.gui.DeleteButton_2.click()
        self.assertIn("Selecciona", self.gui.statusbar.currentMessage())
        self.item(self.gui.ListTree_2, ARRIBA).setSelected(True)
        self.gui.DeleteButton_2.click()
        self.assertIn("Selecciona", self.gui.statusbar.currentMessage())
        self.item(self.gui.ListTree_2, "Fotos/").setSelected(True)
        self.gui.DeleteButton_2.click()
        self.assertEqual(self.textos(self.gui.ListTree_2), [ACTUAL, ARRIBA])

    def test_copiar_en_los_dos_sentidos(self):
        self.carpeta(self.gui.AddFileButton_1, "Fotos")
        self.gui.abrir(self.gui.panelA, self.item(self.gui.ListTree_1, "Fotos/"))
        self.archivo(self.gui.AddArchiveButton_1, "playa")
        self.gui.abrir(self.gui.panelA, self.item(self.gui.ListTree_1, ARRIBA))

        self.gui.CopyButtonTree_1.click()
        self.assertIn("Selecciona", self.gui.statusbar.currentMessage())

        self.item(self.gui.ListTree_1, "Fotos/").setSelected(True)
        self.gui.CopyButtonTree_1.click()
        self.assertEqual(self.gui.panelB.tree.show(), "root/\n\tFotos/\n\t\tplaya.txt\n")

        self.item(self.gui.ListTree_1, "Fotos/").setSelected(True)
        self.gui.CopyButtonTree_1.click()
        self.assertIn("Ya existían", self.gui.statusbar.currentMessage())

        self.archivo(self.gui.AddArchiveButton_2, "solo-en-b")
        self.item(self.gui.ListTree_2, "solo-en-b.txt").setSelected(True)
        self.gui.CopyButtonTree_2.click()
        self.assertIsNotNone(self.gui.panelA.tree.TreesearchName("solo-en-b.txt"))

    def test_los_datos_persisten_al_reabrir(self):
        self.carpeta(self.gui.AddFileButton_1, "Fotos")
        self.archivo(self.gui.AddArchiveButton_2, "uno")
        otra = GUISistemaArchivo(self.temporal.name)
        self.assertEqual(self.textos(otra.ListTree_1), [ACTUAL, ARRIBA, "Fotos/"])
        self.assertEqual(self.textos(otra.ListTree_2), [ACTUAL, ARRIBA, "uno.txt"])
        otra.close()

    def test_memoria_danada_no_se_pierde(self):
        ruta = os.path.join(self.temporal.name, "Tree-A.mem")
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write("esto no es un árbol\n")
        original = QMessageBox.warning
        avisos = []
        QMessageBox.warning = staticmethod(lambda *a: avisos.append(a[2]))
        try:
            otra = GUISistemaArchivo(self.temporal.name)
        finally:
            QMessageBox.warning = original
        self.assertEqual(len(avisos), 1)
        self.assertTrue(os.path.exists(ruta + ".danado"))
        self.assertEqual(self.textos(otra.ListTree_1), [ACTUAL, ARRIBA])
        otra.close()


if __name__ == "__main__":
    unittest.main()
