from Nucleo.Clases.GenericNode import Node
from Nucleo.Clases.Lista import List


class Tree:
    """Árbol n-ario: cada carpeta guarda a sus hijos en una lista enlazada ordenada."""

    CARACTERES_PROHIBIDOS = "/\\\t\n\r"

    def __init__(self):
        self.root = Node("root/")
        self.root.children = List()

    def nombreValido(self, nombre):
        nombre = nombre.strip()
        if nombre in ("", ".", ".."):
            return False
        return not any(c in nombre for c in self.CARACTERES_PROHIBIDOS)

    def TreeaddFolder(self, folder, current=None):
        """Crea una carpeta en current (por defecto, la raíz). Devuelve el nodo o None."""
        current = current or self.root
        if not current.esCarpeta():
            return None
        if isinstance(folder, str):
            if not self.nombreValido(folder):
                return None
            nodo = Node(folder.strip() + "/")
            nodo.children = List()
        else:
            nodo = folder
        if not current.children.addFolder(nodo):
            return None
        nodo.parent = current
        return nodo

    def TreeaddFile(self, file, current=None):
        """Crea un archivo .txt en current (por defecto, la raíz). Devuelve el nodo o None."""
        current = current or self.root
        nombre = "%s" % file
        if not current.esCarpeta() or not self.nombreValido(nombre):
            return None
        nombre = nombre.strip()
        if not nombre.endswith(".txt"):
            nombre += ".txt"
        nodo = Node(nombre)
        if not current.children.addNode(nodo):
            return None
        nodo.parent = current
        return nodo

    def TreesearchName(self, name, current=None):
        """Busca un nombre entre los hijos directos de current."""
        current = current or self.root
        if not current.esCarpeta():
            return None
        return current.children.searchName(name)

    def TreepopName(self, name, current=None):
        """Elimina un hijo de current, con todo lo que contenga."""
        current = current or self.root
        if not current.esCarpeta():
            return False
        return current.children.popName(name)

    def Copy(self, nodo, destino):
        """Copia nodo (y sus hijos) dentro de la carpeta destino. Devuelve la copia o None."""
        if not destino.esCarpeta() or self.esDescendiente(destino, nodo):
            return None
        copia = self.clonar(nodo)
        if not destino.children.addNode(copia):
            return None
        copia.parent = destino
        return copia

    def clonar(self, nodo):
        copia = Node(nodo.name)
        if nodo.esCarpeta():
            copia.children = List()
            for hijo in nodo.children.toArray():
                copiaHijo = self.clonar(hijo)
                copiaHijo.parent = copia
                copia.children.addNode(copiaHijo)
        return copia

    def esDescendiente(self, nodo, posibleAncestro):
        """True si nodo es posibleAncestro o está dentro de él."""
        actual = nodo
        while actual:
            if actual is posibleAncestro:
                return True
            actual = actual.parent
        return False

    def ruta(self, nodo):
        """Ruta completa de un nodo, por ejemplo root/Documentos/notas.txt."""
        partes = []
        actual = nodo
        while actual:
            partes.append(actual.name)
            actual = actual.parent
        return "".join(reversed(partes))

    def nodeToArray(self, node):
        """Hijos de una carpeta, en orden."""
        return node.children.toArray() if node.esCarpeta() else []

    def show(self, nodo=None, nivel=0):
        """Texto con una línea por nodo; la profundidad se indica con tabuladores."""
        nodo = nodo or self.root
        texto = "\t" * nivel + nodo.name + "\n"
        for hijo in self.nodeToArray(nodo):
            texto += self.show(hijo, nivel + 1)
        return texto
