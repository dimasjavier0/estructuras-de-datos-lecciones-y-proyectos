"""Dos formas de guardar el mismo grafo: un diccionario y un TDA hecho con listas enlazadas."""
from grafos.lista_enlazada import ListaEnlazada


class GrafoDiccionario:
    """Lista de adyacencia con diccionarios: {vértice: {vecino: peso}}."""

    def __init__(self, dirigido=True):
        self.dirigido = dirigido
        self.adyacencia = {}

    def agregar_vertice(self, nombre):
        self.adyacencia.setdefault(nombre, {})

    def agregar_arista(self, origen, destino, peso=1):
        if peso < 0:
            raise ValueError("El peso no puede ser negativo")
        self.agregar_vertice(origen)
        self.agregar_vertice(destino)
        self.adyacencia[origen][destino] = peso
        if not self.dirigido:
            self.adyacencia[destino][origen] = peso

    def eliminar_vertice(self, nombre):
        """Quita el vértice y todas las aristas que llegan a él."""
        if nombre not in self.adyacencia:
            return False
        del self.adyacencia[nombre]
        for vecinos in self.adyacencia.values():
            vecinos.pop(nombre, None)
        return True

    def vertices(self):
        return sorted(self.adyacencia)

    def vecinos(self, vertice):
        return sorted(self.adyacencia[vertice])

    def peso(self, origen, destino):
        return self.adyacencia[origen][destino]

    def conectados_con(self, vertice):
        """Vértices unidos a este por una arista en cualquier sentido."""
        salientes = set(self.adyacencia[vertice])
        entrantes = {v for v, vecinos in self.adyacencia.items() if vertice in vecinos}
        return sorted(salientes | entrantes)


class Vertice:
    def __init__(self, nombre):
        self.nombre = nombre
        self.aristas = ListaEnlazada()  # nombres de los vecinos


class GrafoTDA:
    """El mismo grafo sin diccionarios ni listas de Python: vértices y aristas en listas enlazadas."""

    def __init__(self):
        self.vertices_ = ListaEnlazada()

    def buscar(self, nombre):
        for vertice in self.vertices_:
            if vertice.nombre == nombre:
                return vertice
        return None

    def agregar_vertice(self, nombre):
        if self.buscar(nombre):
            return False
        self.vertices_.agregar(Vertice(nombre))
        return True

    def agregar_arista(self, origen, destino):
        vertice = self.buscar(origen)
        if vertice is None or self.buscar(destino) is None:
            raise KeyError("Los dos vértices deben existir antes de unirlos")
        return vertice.aristas.agregar(destino)

    def eliminar_vertice(self, nombre):
        vertice = self.buscar(nombre)
        if vertice is None:
            return False
        self.vertices_.quitar(vertice)
        for otro in self.vertices_:
            otro.aristas.quitar(nombre)
        return True

    def vertices(self):
        return sorted(v.nombre for v in self.vertices_)

    def vecinos(self, nombre):
        vertice = self.buscar(nombre)
        if vertice is None:
            raise KeyError(nombre)
        return sorted(vertice.aristas)
