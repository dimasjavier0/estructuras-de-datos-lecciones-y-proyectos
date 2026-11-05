# Lección 08: ordenamiento

**Aprenderás:** cómo funcionan cinco algoritmos clásicos de ordenamiento, y a elegir entre ellos.

**Proyectos:** [`ordenamiento-y-rendimiento-python`](../proyectos/ordenamiento-y-rendimiento-python)

## La idea

| Algoritmo | Idea | Mejor caso | Promedio | Peor caso | Memoria adicional |
|---|---|---|---|---|---|
| Burbuja | Intercambia vecinos desordenados | O(n) | O(n²) | O(n²) | O(1) |
| Inserción | Mete cada elemento en su lugar, como cartas en la mano | O(n) | O(n²) | O(n²) | O(1) |
| Selección | Busca el menor de lo que falta | O(n²) | O(n²) | O(n²) | O(1) |
| Quicksort | Parte alrededor de un pivote | O(n log n) | O(n log n) | O(n²) | O(log n) |
| Mezcla | Divide en dos, ordena y mezcla | O(n log n) | O(n log n) | O(n log n) | O(n) |

La memoria adicional de las tablas se refiere al algoritmo en sí. En este proyecto cada función primero copia la lista para no modificar la original.

### Dividir y vencer

Mezcla y quicksort usan la misma estrategia: partir el problema, resolver las partes con recursividad y unirlas. Mezcla hace el trabajo **al unir**; quicksort, **al partir**.

¿De dónde sale n log n en mezcla? Hay unos log₂ n niveles de división, porque la lista se parte a la mitad cada vez, y en cada nivel se recorren `n` elementos al mezclar.

```python
while i < len(izquierda) and j < len(derecha):
    if contador.mayor(izquierda[i], derecha[j]):
        resultado.append(derecha[j])
        j += 1
    else:
        resultado.append(izquierda[i])
        i += 1
return resultado + izquierda[i:] + derecha[j:]
```

Cuando los dos valores son iguales, se toma el de la izquierda. Eso hace que mezcla sea **estable**: los elementos iguales conservan su orden original, algo importante si ordenas por una columna y ya habías ordenado por otra.

### En la vida real

Casi nunca escribirás uno de estos: `sorted()` de Python usa Timsort, una mezcla de inserción y mezcla. Conocerlos sirve para entender los costos y razonar sobre tus propios algoritmos.

## Lee el código

1. Lee [`ordenamientos.py`](../proyectos/ordenamiento-y-rendimiento-python/ordenamientos.py). ¿Qué hace `hubo_cambio` en burbuja? ¿Cómo logra que sea O(n) con una lista ordenada?
2. En `quicksort`, ¿por qué se elige el elemento del medio como pivote? Corre `python rendimiento.py --caso ordenado` y piensa qué pasaría si se usara siempre el último.
3. Mira `seleccion` y explica por qué `--caso ordenado` no la ayuda en nada.
4. ¿Qué comprueba `medir` en [`rendimiento.py`](../proyectos/ordenamiento-y-rendimiento-python/rendimiento.py), además de medir el tiempo?

## Ejercicios

1. **Básico:** corre los tres casos con `--tamanos 2000` y anota el mejor y el peor algoritmo de cada uno.
2. **Intermedio:** agrega heapsort a `ALGORITMOS`. Puedes reutilizar la idea de la [lección 05](05-heap.md).
3. **Intermedio:** cuenta también los intercambios, y compara selección con burbuja.

## Reto

Cambia quicksort para que use el último elemento como pivote y corre `--caso ordenado --tamanos 3000`. ¿Qué pasa con las comparaciones? ¿Y con la recursión? Busca qué es `RecursionError` y propón dos formas de evitarlo.

## Repaso

- ¿Cuál hace el trabajo al partir y cuál al unir?
- ¿Por qué inserción puede ganarle a quicksort con pocos datos casi ordenados?
- ¿Qué significa que un ordenamiento sea estable? Da un ejemplo en el que importe.

Siguiente: [Lección 09: grafos](09-grafos.md)
