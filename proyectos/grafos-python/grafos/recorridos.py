"""Recorridos que funcionan con cualquier grafo que tenga vecinos(vertice)."""
from collections import deque
import heapq


def bfs(grafo, inicio):
    """Por niveles, con una cola. Primero los vértices más cercanos."""
    visitados = [inicio]
    cola = deque([inicio])
    while cola:
        actual = cola.popleft()
        for vecino in grafo.vecinos(actual):
            if vecino not in visitados:
                visitados.append(vecino)
                cola.append(vecino)
    return visitados


def dfs(grafo, inicio, visitados=None):
    """En profundidad, con recursión: sigue un camino hasta el final antes de retroceder."""
    if visitados is None:
        visitados = []
    visitados.append(inicio)
    for vecino in grafo.vecinos(inicio):
        if vecino not in visitados:
            dfs(grafo, vecino, visitados)
    return visitados


def todos_los_caminos(grafo, origen, destino):
    """Todos los caminos simples (sin repetir vértices), con retroceso."""
    caminos = []
    camino = [origen]

    def explorar(actual):
        if actual == destino:
            caminos.append(list(camino))
            return
        for vecino in grafo.vecinos(actual):
            if vecino not in camino:
                camino.append(vecino)
                explorar(vecino)
                camino.pop()

    explorar(origen)
    return caminos


def camino_mas_corto(grafo, origen, destino):
    """Dijkstra. Devuelve (costo, camino), o (None, []) si no se puede llegar."""
    mejor = {origen: 0}
    anterior = {}
    pendientes = [(0, origen)]
    while pendientes:
        costo, actual = heapq.heappop(pendientes)
        if actual == destino:
            camino = [destino]
            while camino[-1] != origen:
                camino.append(anterior[camino[-1]])
            return costo, camino[::-1]
        if costo > mejor[actual]:
            continue
        for vecino in grafo.vecinos(actual):
            nuevo = costo + grafo.peso(actual, vecino)
            if nuevo < mejor.get(vecino, float("inf")):
                mejor[vecino] = nuevo
                anterior[vecino] = actual
                heapq.heappush(pendientes, (nuevo, vecino))
    return None, []
