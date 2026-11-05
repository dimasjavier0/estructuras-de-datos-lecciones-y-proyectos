# Lección 06: archivos y datos

**Aprenderás:** a leer y generar archivos de texto, y a convertir datos en HTML sin abrir un agujero de seguridad.

**Proyectos:** [`datos-y-archivos-python`](../proyectos/datos-y-archivos-python)

## La idea

Los programas se comunican con el mundo mediante texto con una estructura acordada:

| Formato | Forma | Ejemplo |
|---|---|---|
| CSV | Columnas separadas por comas | `lapiz,8,500` |
| TSV | Columnas separadas por tabuladores | `lapiz	8	500` |
| JSON | Objetos y listas anidados | `{"tipo": "texto", "tamano_kb": 34}` |

Leer una tabla es dividir dos veces: en líneas y en columnas. El único cambio entre CSV y TSV es el separador, así que [`leer_tabla`](../proyectos/datos-y-archivos-python/datos.py) lo toma de un diccionario:

```python
separadores = {".csv": ",", ".tsv": "\t"}
```

**Una limitación importante.** `"Pérez, Ana",30` tiene una coma dentro del dato. Un `split` lo rompe. Por eso, en un programa real, se usa el módulo `csv`. Aquí se implementa a mano para entender qué resuelve.

### Datos reproducibles

`generar_csv` recibe una **semilla**. Con la misma semilla salen los mismos números, y por eso se pueden comprobar en una prueba:

```python
azar = random.Random(semilla)
```

### Escapar el HTML

Si un dato contiene `<script>` y lo pegas tal cual en una página, el navegador lo ejecuta. Esto se llama XSS. La defensa es convertir los caracteres especiales con `html.escape`, que `a_lista_html` usa con cada valor.

Es la misma idea de `textContent` en JavaScript, como en [`estructuras-lineales-js/js/app.js`](../proyectos/estructuras-lineales-js/js/app.js).

## Lee el código

1. Corre `python main.py` y mira los archivos de `salida/`. Vuelve a correrlo: ¿cambia `aleatorio.csv`? ¿Por qué no?
2. Abre [`ejemplos/carpetas.json`](../proyectos/datos-y-archivos-python/ejemplos/carpetas.json) y sigue cómo se convierte en la lista de `arbol.html`.
3. En [`main.py`](../proyectos/datos-y-archivos-python/main.py), ¿para qué sirve `CARPETA`? Prueba a correr el programa desde otra carpeta con `python proyectos/datos-y-archivos-python/main.py`.
4. Lee `test_archivo_inexistente_y_vacio`. ¿Qué pasa con un CSV vacío?

## Ejercicios

1. **Básico:** escribe `escribir_tabla(ruta, filas)`, inversa de `leer_tabla`, y prueba que leer lo escrito devuelva lo mismo.
2. **Intermedio:** escribe `tabla_a_html(filas)`, que genere una `<table>` con la primera fila como encabezado, y que escape los datos.
3. **Intermedio:** suma la columna `cantidad` de `productos.csv` y avisa si algún valor no es un número.

## Reto

Mejora `leer_tabla` para que acepte campos entre comillas, como `"Pérez, Ana",30`, recorriendo la línea carácter por carácter. Después compara tu resultado con el módulo `csv` en varios casos difíciles, incluidas las comillas dentro de comillas.

## Repaso

- ¿Por qué `split(",")` no alcanza para un CSV real?
- ¿Qué es una semilla y para qué sirve en una prueba?
- ¿Qué podría pasar si no escapas un dato antes de ponerlo en HTML?

Siguiente: [Lección 07: complejidad y notación Big-O](07-complejidad-big-o.md)
