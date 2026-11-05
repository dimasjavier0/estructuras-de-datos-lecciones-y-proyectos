# Lección 04: árboles binarios de búsqueda

**Aprenderás:** a organizar datos para buscarlos sin revisarlos todos, y a eliminar un nodo sin romper el árbol.

**Proyectos:** [`arboles-y-heap-js`](../proyectos/arboles-y-heap-js)

## La idea

En un **árbol binario** cada nodo tiene como máximo dos hijos. En uno **de búsqueda** (BST) hay una regla más: los menores van a la izquierda y los mayores a la derecha, en cada nodo.

```
        50
       /  \
     30    70
    /  \   / \
  20  40  60  80
```

Buscar `60` visita solo `50 → 70 → 60`. Cada comparación descarta una rama entera. Si el árbol está equilibrado, la búsqueda es O(log n): con un millón de datos bastan unas 20 comparaciones.

**Cuidado con el peor caso.** Si insertas `1, 2, 3, 4` en orden, cada nodo queda a la derecha del anterior y el árbol es una lista: la búsqueda vuelve a ser O(n). Compruébalo en la página.

### Los recorridos

| Recorrido | Orden | Sirve para |
|---|---|---|
| Inorden | izquierda, nodo, derecha | Obtener los valores **ordenados** |
| Preorden | nodo, izquierda, derecha | Copiar la estructura |
| Postorden | izquierda, derecha, nodo | Procesar los hijos antes que el padre |
| Por niveles | nivel por nivel, con una cola | Ver la forma del árbol |

### Eliminar: el caso interesante

Mira [`_eliminar`](../proyectos/arboles-y-heap-js/js/arboles.js). Hay tres casos:

- **Sin hijos o con uno:** el hijo, si existe, ocupa su lugar.
- **Con dos hijos:** no se puede quitar sin más. Se copia el valor de su **sucesor** (el menor de la rama derecha) y se elimina ese sucesor, que como mucho tiene un hijo.

```js
} else if (nodo.izquierdo && nodo.derecho) {
  let sucesor = nodo.derecho;
  while (sucesor.izquierdo) sucesor = sucesor.izquierdo;
  nodo.valor = sucesor.valor;
  nodo.derecho = this._eliminar(nodo.derecho, sucesor.valor);
}
```

## Lee el código

1. Abre `index.html`, busca `60` y mira qué nodos se resaltan. Luego busca `65`.
2. Lee `insertar` en [`js/arboles.js`](../proyectos/arboles-y-heap-js/js/arboles.js). ¿Por qué no necesita recursividad? ¿Qué hace con un valor repetido?
3. Elimina `50` en la página y compara con el dibujo de arriba. ¿Qué valor quedó en la raíz, y por qué ese?
4. Lee la prueba "el inorden siempre queda ordenado" en [`pruebas/arboles.test.js`](../proyectos/arboles-y-heap-js/pruebas/arboles.test.js). ¿Qué estructura usa para comprobar el resultado?

## Ejercicios

1. **Básico:** agrega `minimo()` y `maximo()`. ¿Cuántos nodos visitan?
2. **Intermedio:** agrega `contarHojas()`, de forma recursiva.
3. **Intermedio:** muestra en la página si el árbol está equilibrado (la altura de sus dos ramas difiere en 1 o menos, en todo nodo).

## Reto

Escribe `esBST(nodo)`, que compruebe si un árbol cualquiera cumple la regla. Cuidado: revisar solo que cada hijo sea correcto respecto a su padre **no alcanza**. Construye a mano un árbol que pase esa revisión y aun así sea inválido.

## Repaso

- ¿Por qué el inorden sale ordenado?
- ¿Cuándo la búsqueda en un BST es O(n)?
- ¿Por qué el sucesor tiene como mucho un hijo?

Siguiente: [Lección 05: heap](05-heap.md)
