import os

from Nucleo.Clases.GenericTree import Tree
from Nucleo.Clases.GenericNode import Node
from Nucleo.Clases.Lista import List


class ErrorMemoria(Exception):
    """El contenido de un archivo .mem no se puede convertir en árbol."""


class GestionTree:
    """Guarda un árbol en un archivo de texto y lo vuelve a construir.

    Cada línea es un nodo. Los tabuladores indican el nivel, y una línea que termina en / es una carpeta.
    """

    def Guardar(self, tree, ruta):
        temporal = ruta + ".tmp"
        with open(temporal, "w", encoding="utf-8") as archivo:
            archivo.write(tree.show())
        os.replace(temporal, ruta)

    def Cargar(self, ruta):
        """Devuelve el árbol guardado. Un archivo vacío o inexistente es un árbol vacío."""
        if not os.path.exists(ruta):
            return Tree()
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.read().splitlines()
        return self.textoATree(lineas)

    def textoATree(self, lineas):
        tree = Tree()
        lineas = [linea for linea in lineas if linea.strip()]
        if not lineas:
            return tree
        if lineas[0] != tree.root.name:
            raise ErrorMemoria("La primera línea debe ser %s" % tree.root.name)

        # padres[n] es la última carpeta vista en el nivel n
        padres = [tree.root]
        for numero, linea in enumerate(lineas[1:], start=2):
            nombre = linea.lstrip("\t")
            nivel = len(linea) - len(nombre)
            if nivel < 1 or nivel > len(padres):
                raise ErrorMemoria("Línea %d: nivel de tabuladores inválido" % numero)

            nodo = Node(nombre)
            if nombre.endswith("/"):
                nodo.children = List()
            padre = padres[nivel - 1]
            if not padre.children.addNode(nodo):
                raise ErrorMemoria("Línea %d: nombre repetido (%s)" % (numero, nombre))
            nodo.parent = padre

            del padres[nivel:]
            if nodo.esCarpeta():
                padres.append(nodo)
        return tree
