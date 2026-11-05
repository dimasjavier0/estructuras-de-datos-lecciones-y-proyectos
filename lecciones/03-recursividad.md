# Lección 03: recursividad

**Aprenderás:** a resolver problemas con forma de árbol mediante funciones que se llaman a sí mismas.

**Proyectos:** [`datos-y-archivos-python`](../proyectos/datos-y-archivos-python)

**Herramienta nueva:** a partir de aquí también se usa Python.

## La idea

Una función recursiva tiene dos partes: un **caso base**, que se responde directo, y un **caso recursivo**, que reduce el problema y se llama de nuevo.

Es la forma natural de recorrer datos anidados, porque no sabes de antemano cuántos niveles hay. Con ciclos necesitarías uno por nivel. Mira [`a_lista_html`](../proyectos/datos-y-archivos-python/datos.py):

```python
def a_lista_html(elementos):
    partes = ["<ul>"]
    for elemento in elementos:
        if isinstance(elemento, (list, tuple)):
            partes.append(f"<li>{a_lista_html(elemento)}</li>")   # caso recursivo
        else:
            partes.append(f"<li>{html.escape(str(elemento))}</li>")   # caso base
    partes.append("</ul>")
    return "".join(partes)
```

Con `[1, [2]]`, las llamadas se apilan y se resuelven de adentro hacia afuera:

```
a_lista_html([1, [2]])
  a_lista_html([2])        → "<ul><li>2</li></ul>"
                           → "<ul><li>1</li><li><ul><li>2</li></ul></li></ul>"
```

Cada llamada queda en espera en la **pila de llamadas**, la misma estructura de la lección anterior. Si olvidas el caso base, la pila se llena y Python lanza `RecursionError`.

### Devolver el resultado

Un error muy común es llamar a la función sin usar lo que devuelve:

```python
def buscar(nodo, valor):
    if nodo is None:
        return False
    if nodo.valor == valor:
        return True
    buscar(nodo.siguiente, valor)   # ¡el resultado se pierde y devuelve None!
```

La última línea debe ser `return buscar(nodo.siguiente, valor)`.

## Lee el código

1. Corre `python main.py` en `proyectos/datos-y-archivos-python` y abre `salida/arbol.html`.
2. Lee `arbol_a_texto` en [`datos.py`](../proyectos/datos-y-archivos-python/datos.py). ¿Cuál es el caso base? ¿Qué parámetro cambia en cada llamada?
3. Lee `contar_hojas`, en una sola línea. Escribe a mano qué devuelve para `{"a": {"b": 1}, "c": 2}`.
4. En [`pruebas/test_datos.py`](../proyectos/datos-y-archivos-python/pruebas/test_datos.py), busca la prueba que intenta inyectar `<script>`. ¿Qué función lo impide?

## Ejercicios

1. **Básico:** escribe `profundidad(arbol)`, que diga cuántos niveles tiene un diccionario.
2. **Básico:** escribe `aplanar(lista)`, que convierta `[1, [2, [3]]]` en `[1, 2, 3]`.
3. **Intermedio:** escribe `buscar_ruta(arbol, clave)`, que devuelva la lista de claves hasta llegar a `clave`, o `None`.

## Reto

Escribe una versión de `contar_hojas` **sin recursividad**, usando tu propia pila. Luego explica qué hace Python por ti en la versión recursiva.

## Repaso

- ¿Qué pasa si falta el caso base?
- ¿Por qué un ciclo no alcanza para recorrer niveles desconocidos?
- ¿Qué devuelve una función de Python que termina sin `return`?

Siguiente: [Lección 04: árboles binarios de búsqueda](04-arboles-binarios-de-busqueda.md)
