# Lección 02: pilas y colas

**Aprenderás:** qué es un tipo de dato abstracto, y a usar una pila para resolver un problema real.

**Proyectos:** [`estructuras-lineales-js`](../proyectos/estructuras-lineales-js)

## La idea

Un **tipo de dato abstracto** (TDA) define *qué operaciones* tiene algo, sin decir *cómo* se guardan los datos. Una pila podría estar hecha con un arreglo o con nodos; quien la usa no lo nota.

| TDA | Regla | Operaciones | Se parece a |
|---|---|---|---|
| Pila | El último en entrar es el primero en salir | `apilar`, `desapilar`, `verTope` | Una pila de platos |
| Cola | El primero en entrar es el primero en salir | `encolar`, `desencolar`, `verFrente` | La fila de un banco |

Aquí es donde importa el detalle de implementación: si la cola solo guardara el frente, encolar tendría que caminar toda la fila. Por eso [`Cola`](../proyectos/estructuras-lineales-js/js/estructuras.js) guarda también el último nodo:

```js
encolar(valor) {
  const nuevo = new Nodo(valor);
  if (this.final) this.final.siguiente = nuevo;
  else this.frente = nuevo;
  this.final = nuevo;
  this.tamano++;
}
```

### Una pila que resuelve algo

¿Están bien cerrados los paréntesis de `(a + [b * c])`? Contarlos no basta: `([)]` tiene la misma cantidad de cada uno y está mal. Con una pila es natural: lo que abre entra, y lo que cierra debe coincidir con lo último que abrió.

```js
function parentesisBalanceados(texto) {
  const pares = { ")": "(", "]": "[", "}": "{" };
  const pila = new Pila();
  for (const caracter of texto) {
    if ("([{".includes(caracter)) pila.apilar(caracter);
    else if (caracter in pares) {
      if (pila.tamano === 0 || pila.desapilar() !== pares[caracter]) return false;
    }
  }
  return pila.tamano === 0;
}
```

Las pilas también están detrás de la recursividad (la siguiente lección) y del botón "deshacer". Las colas aparecen en la búsqueda por niveles de la [lección 09](09-grafos.md).

## Lee el código

1. En `index.html`, baja a "Paréntesis balanceados" y escribe `([)]`. Sigue la función a mano: ¿en qué símbolo falla?
2. ¿Qué devolvería la función sin la última línea, si solo pusiera `return true`? Prueba con `((`.
3. Lee `desencolar`. ¿Por qué pone `this.final = null` cuando la cola queda vacía? Pista: mira la prueba "se puede volver a usar".
4. Lee `ejecutar` en [`js/app.js`](../proyectos/estructuras-lineales-js/js/app.js). ¿Dónde se atrapa el error de sacar de una pila vacía?

## Ejercicios

1. **Básico:** agrega `estaVacia()` a `Pila` y a `Cola`, y úsalo en `parentesisBalanceados`.
2. **Intermedio:** escribe `invertirTexto(texto)` usando solo una pila.
3. **Intermedio:** agrega a la página un botón para ver el tope de la pila sin sacarlo.

## Reto

Implementa una **cola usando dos pilas**, sin tocar la clase `Pila`. Pista: una pila recibe y la otra entrega. ¿Cuánto cuesta `desencolar` si haces muchas operaciones seguidas?

## Repaso

- ¿Qué diferencia hay entre un TDA y su implementación?
- ¿Por qué `([)]` no se detecta contando?
- ¿Qué se rompe si `desencolar` no reinicia `final`?

Siguiente: [Lección 03: recursividad](03-recursividad.md)
