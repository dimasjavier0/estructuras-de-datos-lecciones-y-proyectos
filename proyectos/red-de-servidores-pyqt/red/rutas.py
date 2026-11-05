"""Búsqueda de rutas: DFS con retroceso para listarlas todas y Dijkstra para hallar la mejor."""
import heapq
from dataclasses import dataclass


@dataclass(frozen=True)
class Ruta:
    servidores: tuple
    costo: float
    disponible: int  # el enlace más cargado de la ruta limita lo que queda libre (cuello de botella)

    def __str__(self):
        return " → ".join(self.servidores)


def describir(red, servidores):
    enlaces = [red.enlace(a, b) for a, b in zip(servidores, servidores[1:])]
    return Ruta(
        tuple(servidores),
        round(sum(e.costo for e in enlaces), 2),
        min(e.disponible for e in enlaces),
    )


def todas_las_rutas(red, origen, destino):
    """Todas las rutas sin ciclos, de la más barata a la más cara. En el peor caso crece de forma exponencial."""
    encontradas = []
    camino = [origen]

    def explorar(actual):
        if actual == destino:
            encontradas.append(describir(red, camino))
            return
        for vecino in red.vecinos(actual):
            if vecino not in camino:
                camino.append(vecino)
                explorar(vecino)
                camino.pop()  # retroceso: se prueba el siguiente vecino

    explorar(origen)
    return sorted(encontradas, key=lambda r: (r.costo, r.servidores))


def mejor_ruta(red, origen, destino):
    """Dijkstra con cola de prioridad: O((V + E) log V). Devuelve una Ruta o None."""
    distancias = {origen: 0}
    anterior = {}
    pendientes = [(0, origen)]

    while pendientes:
        acumulado, actual = heapq.heappop(pendientes)
        if actual == destino:
            camino = [destino]
            while camino[-1] != origen:
                camino.append(anterior[camino[-1]])
            return describir(red, camino[::-1])
        if acumulado > distancias[actual]:
            continue  # entrada vieja: ya se encontró un camino más corto a este servidor
        for vecino in red.vecinos(actual):
            nuevo = acumulado + red.enlace(actual, vecino).costo
            if nuevo < distancias.get(vecino, float("inf")):
                distancias[vecino] = nuevo
                anterior[vecino] = actual
                heapq.heappush(pendientes, (nuevo, vecino))
    return None
