# Lección 07: complejidad y notación Big-O

**Aprenderás:** a estimar cómo crece el costo de un algoritmo, sin depender de qué tan rápida sea tu computadora.

**Proyectos:** [`ordenamiento-y-rendimiento-python`](../proyectos/ordenamiento-y-rendimiento-python)

## La idea

Medir segundos no sirve para comparar algoritmos: el resultado cambia con la máquina. Lo que sí se mantiene es **cómo crece el trabajo** cuando crece la entrada `n`. Por eso se cuentan operaciones.

```python
def suma(lista):
    total = 0              # 1 asignación
    for valor in lista:    # n vueltas
        total += valor     # n sumas
    return total           # 1
```

Esto da T(n) = 2n + 2, aproximadamente. Para `n` grande, lo que importa es que crece **linealmente**: decimos que es O(n). Dos ciclos anidados de `n` vueltas hacen n² operaciones: O(n²).

### Las definiciones

| Notación | Se lee | Definición |
|---|---|---|
| f(n) es O(g(n)) | Cota superior | Existen c > 0 y n₀ tales que f(n) ≤ c·g(n) para todo n ≥ n₀ |
| f(n) es Ω(g(n)) | Cota inferior | Existen c > 0 y n₀ tales que f(n) ≥ c·g(n) para todo n ≥ n₀ |
| f(n) es Θ(g(n)) | Cota exacta | f(n) es O(g(n)) y también Ω(g(n)) |

Ejemplo: 3n² + 5n − 9 es O(n²), con c = 4 y n₀ = 1, porque n² − 5n + 9 nunca es negativo.

**Una confusión muy común.** Muchos apuntes dicen "Big-O es el peor caso y Big-Ω es el mejor caso". No es así: O y Ω son cotas de una función, y **el peor caso y el mejor caso son funciones distintas**. Se pueden combinar: el peor caso de inserción es Θ(n²) y su mejor caso es Θ(n).

### Reglas prácticas

| Regla | Ejemplo |
|---|---|
| Se ignoran las constantes | O(6n³) = O(n³) |
| Se conserva el término dominante | O(n² + n) = O(n²) |
| Dos partes seguidas: gana la mayor | O(n) + O(n²) = O(n²) |
| Una parte dentro de otra: se multiplican | Un ciclo de `n` con otro de `n` adentro: O(n²) |

### Cuánto importa

| n | log₂ n | n log₂ n | n² |
|---|---|---|---|
| 100 | 7 | 664 | 10 000 |
| 10 000 | 13 | 132 877 | 100 000 000 |
| 1 000 000 | 20 | 19 931 569 | 1 000 000 000 000 |

## Lee el código

Corre el programa dos veces, con los mismos tamaños y casos distintos:

```
cd proyectos/ordenamiento-y-rendimiento-python
python rendimiento.py --tamanos 100 1000
python rendimiento.py --tamanos 100 1000 --caso ordenado
```

1. Con datos aleatorios, las comparaciones son estas. Calcula la última columna y compárala con la teoría, sabiendo que `n` se multiplicó por 10:

   | Algoritmo | n = 100 | n = 1000 | Crecimiento |
   |---|---|---|---|
   | selección | 4950 | 499 500 | |
   | inserción | 2912 | 247 789 | |
   | mezcla | 543 | 8708 | |

2. Con `--caso ordenado`, ¿qué algoritmos cambian muchísimo, y cuál no cambia nada?
3. Lee `Contador` en [`ordenamientos.py`](../proyectos/ordenamiento-y-rendimiento-python/ordenamientos.py). ¿Por qué contar comparaciones es más confiable que medir el tiempo?
4. Lee `test_al_multiplicar_n_por_10...` en [`pruebas/test_ordenamiento.py`](../proyectos/ordenamiento-y-rendimiento-python/pruebas/test_ordenamiento.py).

## Ejercicios

1. **Básico:** calcula T(n) y el orden de un método con dos ciclos anidados, cuyo ciclo interno empieza en `i`.
2. **Básico:** demuestra con la definición que 5n + 3 es O(n). Indica tus valores de `c` y `n₀`.
3. **Intermedio:** agrega `--caso casi-ordenado`: una lista ordenada con 10 elementos cambiados de lugar. Predice qué pasará antes de correrlo.

## Reto

Escribe tres funciones que resuelvan "¿hay valores repetidos en esta lista?": en O(n²), en O(n log n) y en O(n). Mide las tres con 10, 1000 y 10 000 datos, y explica cuánta memoria usa cada una.

## Repaso

- ¿Por qué se ignoran las constantes?
- ¿Es correcto decir que un algoritmo O(n²) es también O(n³)?
- ¿Qué tiene de malo decir "Big-O significa peor caso"?
- ¿Cuándo preferirías un O(n²) a un O(n log n)?

Siguiente: [Lección 08: ordenamiento](08-ordenamiento.md)
