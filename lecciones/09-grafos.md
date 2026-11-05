# Lección 09: grafos

**Aprenderás:** a representar relaciones como un grafo y a recorrerlo con BFS, DFS y Dijkstra.

**Proyectos:** [`grafos-python`](../proyectos/grafos-python)

## La idea

Un **grafo** son **vértices** unidos por **aristas**. Sirve para redes, mapas, dependencias y, en general, cualquier cosa que tenga relaciones.

| Tipo | Significa | Ejemplo |
|---|---|---|
| Dirigido | Las aristas tienen sentido | Seguir a alguien en una red social |
| No dirigido | Valen en los dos sentidos | Una carretera de doble vía |
| Con peso | Cada arista tiene un valor | La distancia entre dos ciudades |

### Dos formas de guardarlo

[`grafos/grafo.py`](../proyectos/grafos-python/grafos/grafo.py) tiene las dos:

- **`GrafoDiccionario`:** `{"Museo": {"Parque": 1, "Teatro": 7}}`. Es corto y rápido.
- **`GrafoTDA`:** vértices y aristas en listas enlazadas. Es más lento, pero muestra que un grafo se puede hacer con lo que viste en la lección 01.

Como los recorridos solo llaman a `vecinos(vertice)`, funcionan con ambos. Esa es la utilidad de un TDA: el algoritmo no sabe cómo se guardan los datos.

### Cuatro recorridos

Están en [`grafos/recorridos.py`](../proyectos/grafos-python/grafos/recorridos.py):

| Recorrido | Usa | Sirve para |
|---|---|---|
| BFS | Una cola | Menos saltos; visitar por niveles |
| DFS | Recursividad (una pila) | Explorar a fondo; detectar ciclos |
| Todos los caminos | DFS con retroceso | Listar alternativas |
| Dijkstra | Un heap | Camino de menor costo, con pesos no negativos |

El retroceso es la parte clave de `todos_los_caminos`:

```python
for vecino in grafo.vecinos(actual):
    if vecino not in camino:
        camino.append(vecino)
        explorar(vecino)
        camino.pop()      # se deshace, para probar el siguiente vecino
```

Un error clásico en Python es escribir `def buscar(grafo, v, camino=[])`: esa lista se crea **una sola vez** y se comparte entre todas las llamadas. Por eso aquí `camino` se crea dentro de la función.

**Dijkstra** siempre saca del heap el vértice pendiente más barato. Con pesos negativos deja de ser correcto, porque un camino ya cerrado podría mejorar después.

### Cuánto cuesta cada uno

Listar todos los caminos puede ser inviable incluso con pocos cientos de vértices, porque su cantidad crece de forma exponencial. Dijkstra, en cambio, es O((V + E) log V), donde V son los vértices y E las aristas.

## Lee el código

1. Corre `python main.py` en `proyectos/grafos-python`. ¿Por qué el camino más corto tiene más saltos que otras opciones?
2. Compara `bfs` y `dfs`. ¿Qué cambia en el orden de visita?
3. Sigue `camino_mas_corto` a mano, de Biblioteca a Parque. ¿Qué hace la línea `if costo > mejor[actual]: continue`?
4. Lee `test_dijkstra_coincide_con_fuerza_bruta`. ¿Qué hace que esta prueba sea tan convincente?

## Ejercicios

1. **Básico:** agrega `grado(vertice)` a `GrafoDiccionario`: cuántas aristas salen de él.
2. **Básico:** con BFS, escribe `saltos(grafo, a, b)`, que diga el mínimo de aristas entre dos vértices.
3. **Intermedio:** agrega pesos a `GrafoTDA`, de modo que Dijkstra también funcione con él.

## Reto

Escribe `tiene_ciclo(grafo)` para un grafo dirigido. Pista: durante el DFS, distingue entre los vértices que están en el camino actual y los que ya terminaste. Luego escribe un orden topológico: dadas las materias de una carrera y sus requisitos, propón un orden para cursarlas.

## Repaso

- ¿Qué estructura usa BFS, y cuál DFS?
- ¿Por qué Dijkstra necesita pesos no negativos?
- ¿Qué problema tiene un parámetro `camino=[]` en Python?
- ¿Por qué listar todos los caminos no escala?

Siguiente: [Lección 10: bits y cifrado](10-bits-y-cifrado.md)
