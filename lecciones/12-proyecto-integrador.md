# Lección 12: proyecto integrador

**Aprenderás:** a unir grafos, validación, archivos e interfaz en una aplicación completa, y a diseñar una métrica que tenga sentido.

**Proyectos:** [`red-de-servidores-pyqt`](../proyectos/red-de-servidores-pyqt)

## La idea

La aplicación lee una red de servidores en texto, la dibuja, lista todas las rutas entre dos servidores y resalta la mejor.

```
Web <-> Aplicacion : distancia=15 capacidad=1000 usuarios=40 trafico=500 medio=cat6
```

| Pieza | Archivo | Lección |
|---|---|---|
| Lista de adyacencia | [`red/modelo.py`](../proyectos/red-de-servidores-pyqt/red/modelo.py) | 09 |
| Lector con validación | [`red/lector.py`](../proyectos/red-de-servidores-pyqt/red/lector.py) | 06 |
| DFS con retroceso y Dijkstra | [`red/rutas.py`](../proyectos/red-de-servidores-pyqt/red/rutas.py) | 05, 07 y 09 |
| Ventana | [`main.py`](../proyectos/red-de-servidores-pyqt/main.py) | 11 |

### Una métrica que tenga sentido

¿Qué significa "la mejor ruta"? Es una decisión de diseño, y es fácil tomarla mal. Imagina que le das a cada enlace un **puntaje de calidad**, donde más es mejor, y que sumas los puntajes de la ruta. Sumar premia dar más vueltas: una ruta de cinco enlaces mediocres puede ganarle a una directa y excelente.

Por eso aquí se usa un **costo**, donde menos es mejor, de modo que cada salto agregado siempre pesa:

```python
@property
def costo(self):
    ocupacion = self.trafico / self.capacidad
    confiabilidad = MEDIOS[self.medio][0]
    return round(self.distancia / 100 + 10 * ocupacion + 20 * (1 - confiabilidad) + self.usuarios / 100, 2)
```

Un costo nunca negativo es justo lo que Dijkstra necesita. La fórmula es un modelo para aprender, no una medida real de redes; sus números se pueden discutir, y ese es el ejercicio.

La tabla también muestra los **Mbps libres**. Eso no se suma: una ruta vale lo que su enlace más cargado. Es el **cuello de botella**, y se calcula con `min`.

En el ejemplo, de Internet a Datos, la ruta más barata tiene 4 saltos y cuesta 18.85. Una de 3 saltos cuesta 22.10 y deja solo 30 Mbps libres: menos saltos no siempre es mejor.

### Validar con mensajes útiles

Un mensaje como "formato inválido" no ayuda a nadie. [`leer_red`](../proyectos/red-de-servidores-pyqt/red/lector.py) indica la línea y el motivo: `Línea 4: wifi alcanza 100 m como máximo`. Todo el texto se valida **antes** de que llegue al resto del programa, y por eso `rutas.py` no necesita defenderse de datos malos.

### Probar un algoritmo con otro

`test_dijkstra_coincide_con_la_fuerza_bruta` compara Dijkstra con la lista de todas las rutas, en cada par de servidores. La búsqueda exhaustiva es lenta pero muy simple, y por eso es una buena referencia para un algoritmo más complejo.

## Lee el código

1. Corre el programa, pulsa **Leer la red** y busca rutas de `Internet` a `Datos`.
2. Escribe `Web -> Web : distancia=1 capacidad=1 usuarios=0 trafico=0 medio=fibra` en el texto. Prueba otros errores, y luego lee `_leer_datos`.
3. Compara `todas_las_rutas` y `mejor_ruta` en `rutas.py`. ¿Cuál visita más caminos?
4. En `main.py`, lee `leer`. ¿Qué limpia cuando hay un error, y por qué es importante?

## Ejercicios

1. **Básico:** agrega un medio nuevo, `cat7`, con sus valores y una prueba.
2. **Intermedio:** agrega una columna con la distancia total de cada ruta.
3. **Intermedio:** agrega un selector para buscar la mejor ruta por costo o por menos saltos. Pista: BFS.

## Reto

Agrega la **ruta de mayor capacidad libre**: la que maximiza el cuello de botella. Dijkstra se puede adaptar: en vez de sumar y buscar el mínimo, usa `min` y busca el máximo. Compruébalo contra `todas_las_rutas`, como hace la prueba de esta lección, y explica por qué esa adaptación sí es correcta.

## Repaso

- ¿Por qué sumar puntajes de calidad favorece las rutas largas?
- ¿Por qué el cuello de botella usa `min` y no una suma?
- ¿Qué gana el resto del programa cuando el lector valida todo?
- ¿Por qué es útil comparar un algoritmo con la fuerza bruta?

## ¿Y ahora?

Terminaste la ruta. Algunas ideas para seguir:

- Publica tu versión con los retos resueltos y explica en el README qué decidiste y por qué.
- Implementa una tabla hash, un árbol AVL o el algoritmo de Kruskal.
- Practica con ejercicios de algoritmos en línea, midiendo siempre el costo de tu solución.
