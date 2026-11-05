"""Lista enlazada mínima: el grafo por TDA la usa en vez de las listas de Python."""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None


class ListaEnlazada:
    def __init__(self):
        self.primero = None

    def agregar(self, valor):
        """Agrega al final. Devuelve False si el valor ya está."""
        if self.primero is None:
            self.primero = Nodo(valor)
            return True
        actual = self.primero
        while True:
            if actual.valor == valor:
                return False
            if actual.siguiente is None:
                actual.siguiente = Nodo(valor)
                return True
            actual = actual.siguiente

    def contiene(self, valor):
        return any(elemento == valor for elemento in self)

    def quitar(self, valor):
        anterior, actual = None, self.primero
        while actual:
            if actual.valor == valor:
                if anterior:
                    anterior.siguiente = actual.siguiente
                else:
                    self.primero = actual.siguiente
                return True
            anterior, actual = actual, actual.siguiente
        return False

    def __iter__(self):
        actual = self.primero
        while actual:
            yield actual.valor
            actual = actual.siguiente

    def __len__(self):
        return sum(1 for _ in self)
