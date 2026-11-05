"""Demostración de los grafos y sus recorridos: python main.py"""
from grafos.grafo import GrafoDiccionario, GrafoTDA
from grafos.recorridos import bfs, camino_mas_corto, dfs, todos_los_caminos


def construir_mapa():
    mapa = GrafoDiccionario(dirigido=False)
    for origen, destino, kilometros in [
        ("Biblioteca", "Parque", 4),
        ("Biblioteca", "Museo", 2),
        ("Museo", "Parque", 1),
        ("Museo", "Teatro", 7),
        ("Parque", "Teatro", 3),
        ("Teatro", "Estadio", 2),
    ]:
        mapa.agregar_arista(origen, destino, kilometros)
    return mapa


def main():
    mapa = construir_mapa()
    print("Vértices:", ", ".join(mapa.vertices()))
    print("Vecinos del Museo:", ", ".join(mapa.vecinos("Museo")))
    print("BFS desde la Biblioteca:", " → ".join(bfs(mapa, "Biblioteca")))
    print("DFS desde la Biblioteca:", " → ".join(dfs(mapa, "Biblioteca")))

    print("\nTodos los caminos de la Biblioteca al Estadio:")
    for camino in todos_los_caminos(mapa, "Biblioteca", "Estadio"):
        total = sum(mapa.peso(a, b) for a, b in zip(camino, camino[1:]))
        print(f"  {total:>3} km  {' → '.join(camino)}")

    costo, camino = camino_mas_corto(mapa, "Biblioteca", "Estadio")
    print(f"\nCamino más corto (Dijkstra): {' → '.join(camino)} ({costo} km)")

    print("\nEl mismo recorrido con el grafo hecho de listas enlazadas:")
    tda = GrafoTDA()
    for vertice in mapa.vertices():
        tda.agregar_vertice(vertice)
    for origen in mapa.vertices():
        for destino in mapa.vecinos(origen):
            tda.agregar_arista(origen, destino)
    print("BFS desde la Biblioteca:", " → ".join(bfs(tda, "Biblioteca")))


if __name__ == "__main__":
    main()
