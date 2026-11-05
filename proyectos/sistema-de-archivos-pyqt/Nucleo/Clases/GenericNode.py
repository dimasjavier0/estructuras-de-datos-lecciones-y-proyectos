class Node:
    """Elemento del árbol: una carpeta (children es una List) o un archivo (children es None)."""

    def __init__(self, name):
        self.name = "%s" % name
        self.next = None      # siguiente hermano en la lista
        self.parent = None    # carpeta que lo contiene
        self.children = None  # List() si es carpeta

    def esCarpeta(self):
        return self.children is not None
