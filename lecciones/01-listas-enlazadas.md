# Lección 01: listas enlazadas

**Aprenderás:** a guardar datos en nodos conectados y a saber cuándo eso conviene más que un arreglo.

**Proyectos:** [`estructuras-lineales-js`](../proyectos/estructuras-lineales-js)

## La idea

Un arreglo guarda sus elementos juntos en memoria. Una lista enlazada los guarda separados: cada **nodo** tiene un valor y una referencia al siguiente.

```
primero → [ 9 ] → [ 3 ] → [ 1 ] → null
```

El código completo está en [`js/estructuras.js`](../proyectos/estructuras-lineales-js/js/estructuras.js). El nodo es muy simple:

```js
class Nodo {
  constructor(valor) {
    this.valor = valor;
    this.siguiente = null;
  }
}
```

Agregar al inicio solo cambia dos referencias, sin importar cuántos elementos haya:

```js
agregarAlInicio(valor) {
  const nuevo = new Nodo(valor);
  nuevo.siguiente = this.primero;
  this.primero = nuevo;
  this.tamano++;
}
```

| Operación | Arreglo | Lista enlazada |
|---|---|---|
| Leer la posición `i` | O(1) | O(n): hay que caminar |
| Agregar al inicio | O(n): hay que mover todo | O(1) |
| Agregar al final | O(1) en promedio | O(n), o O(1) si se guarda el último |
| Eliminar un nodo que ya tienes localizado | O(n) | O(1) en una lista doble |

La notación O se explica en la [lección 07](07-complejidad-big-o.md). Por ahora: O(1) no depende del tamaño y O(n) crece con él.

### Las variantes

- **Ordenada:** cada valor se inserta en su lugar. Mira la función `comparar`: compara `"10"` y `"9"` como números; como texto, `"10"` iría antes.
- **Doble:** cada nodo conoce también al anterior, y se puede recorrer al revés.
- **Circular:** el último nodo apunta al primero. Por eso `recorrer` cuenta los pasos: un `while (actual)` daría vueltas para siempre.

## Lee el código

1. Abre `index.html` y agrega `3`, `1` y `2` en la lista enlazada. Luego abre [`js/estructuras.js`](../proyectos/estructuras-lineales-js/js/estructuras.js) y sigue `agregar`. ¿Cuántos nodos visita con el tercer valor?
2. Lee `eliminar` en `ListaEnlazada`. ¿Por qué necesita la variable `anterior`? ¿Qué pasa cuando se elimina el primero?
3. Lee `invertir`. Dibuja en papel los enlaces de una lista de tres nodos después de cada vuelta del ciclo.
4. Compara `eliminar` de `ListaDoble`. ¿Qué dos casos especiales aparecen, y por qué no existían en la lista simple?

## Ejercicios

1. **Básico:** agrega `contiene(valor)` a `ListaEnlazada` usando `buscar`, y una prueba en `pruebas/estructuras.test.js`.
2. **Básico:** agrega `obtener(posicion)`, que lance un error si la posición no existe.
3. **Intermedio:** guarda una referencia al último nodo en `ListaEnlazada` para que `agregar` sea O(1). Ten cuidado con `eliminar` e `invertir`. Las pruebas existentes deben seguir pasando.

## Reto

Escribe `eliminarRepetidos()`, que deje solo la primera aparición de cada valor, sin crear un arreglo ni otra lista. ¿Cuántas comparaciones hace en el peor caso?

## Repaso

- ¿Qué tiene un nodo?
- ¿Por qué agregar al inicio es O(1) y leer la posición `i` es O(n)?
- ¿Qué pasaría en `invertir` si no guardaras `siguiente` antes de cambiar el enlace?
- ¿Qué condición de parada usarías en una lista circular?

Siguiente: [Lección 02: pilas y colas](02-pilas-y-colas.md)
