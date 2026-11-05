# -*- coding: utf-8 -*-
import os
import shutil
import sys

from PyQt5 import QtGui, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QDesktopWidget, QDialog, QListWidgetItem, QMainWindow, QMessageBox,
)

from Nucleo.Clases.TXT import ErrorMemoria, GestionTree

CARPETA = os.path.dirname(os.path.abspath(__file__))
ACTUAL = " ."
ARRIBA = " . ."


def ruta(*partes):
    return os.path.join(CARPETA, *partes)


class Panel:
    """Una de las dos memorias: su árbol, la carpeta abierta y los controles que la muestran."""

    def __init__(self, nombre, lista, etiqueta, archivo):
        self.nombre = nombre
        self.lista = lista
        self.etiqueta = etiqueta
        self.archivo = archivo
        self.gestion = GestionTree()
        self.tree = None
        self.actual = None

    def cargar(self):
        """Lee el archivo .mem. Si está dañado, lo conserva como .danado y empieza vacío."""
        aviso = None
        try:
            self.tree = self.gestion.Cargar(self.archivo)
        except (ErrorMemoria, UnicodeDecodeError) as error:
            shutil.copy2(self.archivo, self.archivo + ".danado")
            aviso = "%s: el archivo estaba dañado (%s). Se guardó una copia .danado." % (self.nombre, error)
            self.tree = GestionTree().textoATree([])
        self.actual = self.tree.root
        self.mostrar()
        return aviso

    def guardar(self):
        self.gestion.Guardar(self.tree, self.archivo)

    def mostrar(self):
        self.lista.clear()
        for texto in (ACTUAL, ARRIBA):
            self.lista.addItem(QListWidgetItem(texto))
        for nodo in self.tree.nodeToArray(self.actual):
            icono = "carpeta.png" if nodo.esCarpeta() else "archivo.png"
            item = QListWidgetItem(QtGui.QIcon(ruta("Nucleo", "Iconoss", icono)), nodo.name)
            item.setData(Qt.UserRole, nodo)
            self.lista.addItem(item)
        self.etiqueta.setText("%s: %s" % (self.nombre, self.tree.ruta(self.actual)))
        self.etiqueta.adjustSize()

    def seleccionados(self):
        """Nodos seleccionados, sin contar las entradas . y .."""
        nodos = [item.data(Qt.UserRole) for item in self.lista.selectedItems()]
        return [nodo for nodo in nodos if nodo is not None]


class GUISistemaArchivo(QMainWindow):
    def __init__(self, carpetaMemoria=None):
        super().__init__()
        uic.loadUi(ruta("Nucleo", "GUI", "GuiSistemaArchivos1.ui"), self)
        marco = self.frameGeometry()
        marco.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(marco.topLeft())

        self.dialogoCarpeta = uic.loadUi(ruta("Nucleo", "GUI", "VentanaFileAdd1.ui"), QDialog())
        self.dialogoCarpeta.AcceptButtonFile_1.clicked.connect(self.dialogoCarpeta.accept)
        self.dialogoArchivo = uic.loadUi(ruta("Nucleo", "GUI", "VentanaArchiveAdd1.ui"), QDialog())
        self.dialogoArchivo.AcceptButtonArchive_1.clicked.connect(self.dialogoArchivo.accept)

        carpetaMemoria = carpetaMemoria or ruta("Memoria")
        os.makedirs(carpetaMemoria, exist_ok=True)
        self.panelA = Panel("Memoria A", self.ListTree_1, self.label, os.path.join(carpetaMemoria, "Tree-A.mem"))
        self.panelB = Panel("Memoria B", self.ListTree_2, self.label_3, os.path.join(carpetaMemoria, "Tree-B.mem"))

        for panel in (self.panelA, self.panelB):
            aviso = panel.cargar()
            if aviso:
                QMessageBox.warning(self, "Memoria dañada", aviso)

        self.conectar(self.panelA, self.AddFileButton_1, self.AddArchiveButton_1, self.DeleteButton_1)
        self.conectar(self.panelB, self.AddFileButton_2, self.AddArchiveButton_2, self.DeleteButton_2)
        self.CopyButtonTree_1.setToolTip("Copiar a la Memoria B")
        self.CopyButtonTree_2.setToolTip("Copiar a la Memoria A")
        self.CopyButtonTree_1.clicked.connect(lambda: self.copiar(self.panelA, self.panelB))
        self.CopyButtonTree_2.clicked.connect(lambda: self.copiar(self.panelB, self.panelA))
        self.statusbar.showMessage("Doble clic en una carpeta para abrirla; en . . para regresar")

    def conectar(self, panel, botonCarpeta, botonArchivo, botonBorrar):
        botonCarpeta.setToolTip("Nueva carpeta")
        botonArchivo.setToolTip("Nuevo archivo")
        botonBorrar.setToolTip("Eliminar lo seleccionado")
        botonCarpeta.clicked.connect(lambda: self.agregarCarpeta(panel))
        botonArchivo.clicked.connect(lambda: self.agregarArchivo(panel))
        botonBorrar.clicked.connect(lambda: self.eliminar(panel))
        panel.lista.itemDoubleClicked.connect(lambda item: self.abrir(panel, item))

    def pedirNombre(self, dialogo, entrada):
        entrada.clear()
        entrada.setFocus()
        if dialogo.exec_() != QDialog.Accepted:
            return None
        return entrada.text()

    def agregarCarpeta(self, panel):
        nombre = self.pedirNombre(self.dialogoCarpeta, self.dialogoCarpeta.InputTextFile)
        if nombre is not None:
            self.crear(panel, nombre, panel.tree.TreeaddFolder)

    def agregarArchivo(self, panel):
        nombre = self.pedirNombre(self.dialogoArchivo, self.dialogoArchivo.InputTextArchive)
        if nombre is not None:
            self.crear(panel, nombre, panel.tree.TreeaddFile)

    def crear(self, panel, nombre, funcion):
        if not panel.tree.nombreValido(nombre):
            self.statusbar.showMessage("Nombre inválido: no puede estar vacío ni tener / \\ o tabuladores")
            return
        nodo = funcion(nombre, panel.actual)
        if nodo is None:
            self.statusbar.showMessage("Ya existe «%s» en esta carpeta" % nombre.strip())
            return
        panel.guardar()
        panel.mostrar()
        self.statusbar.showMessage("Creado: %s" % panel.tree.ruta(nodo))

    def eliminar(self, panel):
        nodos = panel.seleccionados()
        if not nodos:
            self.statusbar.showMessage("Selecciona primero lo que quieres eliminar")
            return
        for nodo in nodos:
            panel.tree.TreepopName(nodo.name, panel.actual)
        panel.guardar()
        panel.mostrar()
        self.statusbar.showMessage("Eliminados: %d" % len(nodos))

    def copiar(self, origen, destino):
        nodos = origen.seleccionados()
        if not nodos:
            self.statusbar.showMessage("Selecciona primero lo que quieres copiar")
            return
        copiados = 0
        repetidos = []
        for nodo in nodos:
            if destino.tree.Copy(nodo, destino.actual):
                copiados += 1
            else:
                repetidos.append(nodo.name)
        destino.guardar()
        destino.mostrar()
        mensaje = "Copiados: %d" % copiados
        if repetidos:
            mensaje += ". Ya existían: %s" % ", ".join(repetidos)
        self.statusbar.showMessage(mensaje)

    def abrir(self, panel, item):
        if item.text() == ARRIBA:
            if panel.actual.parent:
                panel.actual = panel.actual.parent
                panel.mostrar()
            else:
                self.statusbar.showMessage("Ya estás en la raíz")
            return
        nodo = item.data(Qt.UserRole)
        if nodo is None:  # la entrada . solo vuelve a mostrar la carpeta
            panel.mostrar()
        elif nodo.esCarpeta():
            panel.actual = nodo
            panel.mostrar()
        else:
            self.statusbar.showMessage("%s es un archivo: no se puede abrir" % nodo.name)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = GUISistemaArchivo()
    GUI.show()
    sys.exit(app.exec_())
