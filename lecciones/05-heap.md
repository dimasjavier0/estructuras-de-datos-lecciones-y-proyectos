# Lección 05: heap

**Aprenderás:** a obtener siempre el mayor o el menor elemento en poco tiempo, con un árbol guardado en un arreglo.

**Proyectos:** [`arboles-y-heap-js`](../proyectos/arboles-y-heap-js)

## La idea

Un **montículo** o *heap* es un árbol binario **completo** (se llena nivel por nivel, de izquierda a derecha) con una regla más débil que la del BST: cada padre le gana a sus hijos. En uno de máximos, el padre es mayor; en uno de mínimos, menor. No hay orden entre hermanos.

Como es completo, no necesita nodos ni referencias: cabe en un arreglo.

```
            40              arreglo: [40, 25, 18, 12, 3, 7]
          /    \
        25      18          hijos de i:  2i + 1  y  2i + 2
       /  \    /            padre de i:  (i - 1) / 2, sin decimales
     12    3  7
```

| Operación | Cómo funciona | Costo |
|---|---|---|
| Ver la raíz | `datos[0]` | O(1) |
| Insertar | Va al final y **sube** mientras le gane a su padre | O(log n) |
| Extraer la raíz | El último pasa a la raíz y **baja** cambiando con su mejor hijo | O(log n) |

Así sube un valor, en [`js/arboles.js`](../proyectos/arboles-y-heap-js/js/arboles.js):

```js
insertar(valor) {
  this.datos.push(valor);
  let i = this.datos.length - 1;
  while (i > 0) {
    const padre = Math.floor((i - 1) / 2);
    if (!this._antes(this.datos[i], this.datos[padre])) break;
    this._intercambiar(i, padre);
    i = padre;
  }
}
```

Un heap es la implementación habitual de una **cola de prioridad**: atender primero lo más urgente, no lo que llegó primero. Lo vas a usar en Dijkstra, en la [lección 09](09-grafos.md).

Y da un algoritmo de ordenamiento: mete todo y saca de uno en uno. Eso es O(n log n), en `ordenarConMonticulo`.

**Una trampa frecuente:** poner una lista en forma de árbol no la convierte en heap. Lo que la hace heap es que se cumpla la regla del padre.

## Lee el código

1. En la página, inserta `99` y mira cómo cambia el arreglo. ¿Cuántos intercambios hubo?
2. Pulsa "Extraer la raíz". ¿Qué valor pasó a la raíz antes de bajar?
3. Lee `_antes`. ¿Por qué con ese único método funciona el mismo código para máximos y para mínimos?
4. Lee `aNiveles`. ¿Cómo sabe dónde termina cada nivel?

## Ejercicios

1. **Básico:** agrega `tamano()` y una prueba.
2. **Intermedio:** escribe `esMonticulo(arreglo, tipo)` y úsala en las pruebas.
3. **Intermedio:** escribe `kMayores(valores, k)`, que devuelva los `k` valores mayores usando un heap.

## Reto

Construye un heap a partir de un arreglo completo **en O(n)**, sin insertar de uno en uno: recorre desde el último padre hasta la raíz y haz bajar cada elemento. Compara las comparaciones de los dos métodos con 100 000 datos.

## Repaso

- ¿Qué diferencia hay entre la regla de un BST y la de un heap?
- ¿Por qué un heap no sirve para buscar un valor cualquiera rápido?
- ¿Por qué se puede guardar en un arreglo sin perder información?

Siguiente: [Lección 06: archivos y datos](06-archivos-y-datos.md)
