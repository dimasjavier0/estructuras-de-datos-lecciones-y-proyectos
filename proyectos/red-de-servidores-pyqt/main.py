"""Ventana de la aplicación: escribe o abre una red, elige dos servidores y compara sus rutas."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Qt5Agg")
import networkx as nx
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QComboBox, QFileDialog, QGridLayout, QHBoxLayout, QHeaderView, QLabel, QMainWindow,
    QMessageBox, QPlainTextEdit, QPushButton, QSplitter, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
)
from PyQt5.QtCore import Qt

from red.lector import ErrorDeFormato, leer_red
from red.rutas import mejor_ruta, todas_las_rutas

EJEMPLO = Path(__file__).resolve().parent / "ejemplos" / "red-oficina.txt"
AZUL, GRIS, ROJO = "#2563a8", "#b8c0cc", "#c2410c"


class VentanaRed(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Red de servidores")
        self.resize(1080, 680)
        self.red = None

        self.texto = QPlainTextEdit()
        self.texto.setFont(QFont("Consolas", 9))
        self.texto.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.boton_abrir = QPushButton("Abrir archivo…")
        self.boton_leer = QPushButton("Leer la red")
        self.origen = QComboBox()
        self.destino = QComboBox()
        self.boton_rutas = QPushButton("Buscar rutas")
        self.boton_rutas.setEnabled(False)
        self.resultado = QLabel("Escribe la red y presiona «Leer la red».")
        self.resultado.setWordWrap(True)

        self.tabla = QTableWidget(0, 4)
        self.tabla.setHorizontalHeaderLabels(["Ruta", "Saltos", "Costo", "Mbps libres"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.verticalHeader().hide()
        self.tabla.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # el ancho no cambia al llenar la tabla

        self.figura = Figure(figsize=(6, 4), tight_layout=True)
        self.lienzo = FigureCanvasQTAgg(self.figura)

        izquierda = QVBoxLayout()
        izquierda.addWidget(QLabel("Enlaces: origen -> destino : distancia= capacidad= usuarios= trafico= medio="))
        izquierda.addWidget(self.texto)
        fila = QHBoxLayout()
        fila.addWidget(self.boton_abrir)
        fila.addWidget(self.boton_leer)
        izquierda.addLayout(fila)
        rejilla = QGridLayout()
        rejilla.addWidget(QLabel("Origen"), 0, 0)
        rejilla.addWidget(self.origen, 0, 1)
        rejilla.addWidget(QLabel("Destino"), 1, 0)
        rejilla.addWidget(self.destino, 1, 1)
        rejilla.addWidget(self.boton_rutas, 2, 0, 1, 2)
        izquierda.addLayout(rejilla)
        panel_izquierdo = QWidget()
        panel_izquierdo.setLayout(izquierda)

        derecha = QVBoxLayout()
        derecha.addWidget(self.lienzo, 3)
        derecha.addWidget(self.resultado)
        derecha.addWidget(self.tabla, 2)
        panel_derecho = QWidget()
        panel_derecho.setLayout(derecha)

        division = QSplitter(Qt.Horizontal)
        division.addWidget(panel_izquierdo)
        division.addWidget(panel_derecho)
        division.setSizes([380, 700])
        self.setCentralWidget(division)

        self.boton_abrir.clicked.connect(self.pedir_archivo)
        self.boton_leer.clicked.connect(self.leer)
        self.boton_rutas.clicked.connect(self.buscar)

        if EJEMPLO.exists():
            self.abrir_archivo(EJEMPLO)

    def avisar(self, mensaje):
        QMessageBox.warning(self, "Revisa los datos", mensaje)

    def pedir_archivo(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Abrir red", "", "Texto (*.txt);;Todos los archivos (*)")
        if ruta:
            self.abrir_archivo(ruta)

    def abrir_archivo(self, ruta):
        try:
            self.texto.setPlainText(Path(ruta).read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError) as error:
            self.avisar(f"No se pudo leer el archivo: {error}")

    def leer(self):
        try:
            self.red = leer_red(self.texto.toPlainText())
        except ErrorDeFormato as error:
            self.red = None
            self.boton_rutas.setEnabled(False)
            self.origen.clear()
            self.destino.clear()
            self.tabla.setRowCount(0)
            self.resultado.setText("")
            self.figura.clear()
            self.lienzo.draw_idle()
            self.avisar(str(error))
            return

        servidores = self.red.servidores()
        for combo in (self.origen, self.destino):
            combo.clear()
            combo.addItems(servidores)
        self.destino.setCurrentIndex(len(servidores) - 1)
        self.boton_rutas.setEnabled(True)
        self.tabla.setRowCount(0)
        self.resultado.setText(f"{len(servidores)} servidores y {len(self.red.enlaces())} enlaces.")
        self.dibujar()

    def buscar(self):
        origen, destino = self.origen.currentText(), self.destino.currentText()
        if origen == destino:
            self.avisar("Elige dos servidores distintos.")
            return
        rutas = todas_las_rutas(self.red, origen, destino)
        self.tabla.setRowCount(len(rutas))
        for fila, ruta in enumerate(rutas):
            valores = (str(ruta), str(len(ruta.servidores) - 1), f"{ruta.costo:.2f}", str(ruta.disponible))
            for columna, valor in enumerate(valores):
                self.tabla.setItem(fila, columna, QTableWidgetItem(valor))
        self.tabla.resizeRowsToContents()  # las rutas largas ocupan varias líneas en vez de cortarse
        mejor = mejor_ruta(self.red, origen, destino)
        if mejor is None:
            self.resultado.setText(f"No hay ninguna ruta de {origen} a {destino}.")
            self.dibujar()
            return
        self.resultado.setText(f"Mejor ruta: {mejor}. Costo {mejor.costo:.2f}, {mejor.disponible} Mbps libres.")
        self.dibujar(mejor.servidores)

    def dibujar(self, resaltada=()):
        grafo = nx.DiGraph()
        grafo.add_nodes_from(self.red.servidores())
        grafo.add_weighted_edges_from((e.origen, e.destino, e.costo) for e in self.red.enlaces())
        tramos = set(zip(resaltada, resaltada[1:]))

        self.figura.clear()
        eje = self.figura.add_subplot(111)
        eje.set_axis_off()
        eje.margins(0.15)
        posiciones = nx.spring_layout(grafo, seed=7, k=1.4)
        nx.draw_networkx_nodes(grafo, posiciones, ax=eje, node_color=AZUL, node_size=1500)
        nx.draw_networkx_labels(grafo, posiciones, ax=eje, font_color="white", font_size=8)
        for arista in grafo.edges():
            en_ruta = arista in tramos
            nx.draw_networkx_edges(
                grafo, posiciones, ax=eje, edgelist=[arista], node_size=1500, connectionstyle="arc3,rad=0.12",
                edge_color=ROJO if en_ruta else GRIS, width=2.8 if en_ruta else 1.2, arrowsize=14,
            )
        self.lienzo.draw_idle()


if __name__ == "__main__":
    aplicacion = QApplication(sys.argv)
    ventana = VentanaRed()
    ventana.show()
    ventana.leer()
    sys.exit(aplicacion.exec_())
