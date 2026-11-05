from Nucleo.Clases.comparar import Compare
from Nucleo.Clases.GenericNode import Node


class List:
    """Lista enlazada de nodos hermanos, siempre ordenada alfabéticamente y sin nombres repetidos."""

    def __init__(self):
        self.first = None

    def addFolder(self, value):
        """Agrega una carpeta; value es su nombre o un nodo ya creado."""
        if isinstance(value, str):
            value = Node(value)
            value.children = List()
        return self.addNode(value)

    def add(self, value):
        """Agrega un archivo con nombre value."""
        return self.addNode(Node("%s" % value))

    def addNode(self, node):
        """Inserta en orden. Devuelve False si no es un nodo o si el nombre ya existe."""
        if not isinstance(node, Node):
            return False

        comparador = Compare()
        anterior = None
        actual = self.first

        while actual:
            resultado = comparador.compare(node.name, actual.name)
            if resultado == 0:
                return False
            if resultado < 0:
                break
            anterior = actual
            actual = actual.next

        node.next = actual
        if anterior:
            anterior.next = node
        else:
            self.first = node
        return True

    def searchName(self, Name):
        """Devuelve el nodo con ese nombre o None."""
        actual = self.first
        while actual:
            if actual.name == "%s" % Name:
                return actual
            actual = actual.next
        return None

    def _index(self, index):
        """Devuelve el nodo en esa posición o None."""
        posicion = 0
        actual = self.first
        while actual:
            if posicion == index:
                return actual
            posicion += 1
            actual = actual.next
        return None

    def popName(self, Name):
        """Quita de la lista el nodo con ese nombre. Devuelve True si existía."""
        anterior = None
        actual = self.first
        while actual:
            if actual.name == "%s" % Name:
                if anterior:
                    anterior.next = actual.next
                else:
                    self.first = actual.next
                actual.next = None
                return True
            anterior = actual
            actual = actual.next
        return False

    def toArray(self):
        """Devuelve los nodos en orden, en un arreglo de Python."""
        nodos = []
        actual = self.first
        while actual:
            nodos.append(actual)
            actual = actual.next
        return nodos

    def __len__(self):
        return len(self.toArray())
