# Estructuras de datos y algoritmos: lecciones y proyectos

Un curso práctico y gratuito de **estructuras de datos y algoritmos**, en español. Tiene **13 lecciones progresivas** y **8 proyectos completos y probados** en Python y JavaScript, desde una lista enlazada hasta una aplicación con interfaz gráfica que busca la mejor ruta en una red.

La idea es simple: lees una lección corta, ejecutas el proyecto que la acompaña, lees el código que se señala y practicas con ejercicios que modifican ese mismo proyecto.

> Este material nació de un curso universitario de estructuras de datos que tomé. El sistema de archivos parte de mi proyecto de ese curso, terminado y corregido. Los demás proyectos cubren los mismos temas y se escribieron desde cero para este repositorio.

## ¿Para quién es?

- Estudiantes que llevan (o van a llevar) un curso de estructuras de datos y quieren ejemplos completos que sí funcionan.
- Personas que saben lo básico de programación (variables, condicionales, ciclos, funciones y clases) y quieren dar el siguiente paso.

No necesitas saber Python y JavaScript a fondo: el código es directo y las lecciones señalan qué leer.

## Cómo usar este repositorio

1. **Prepara tu computadora** con la [lección 00](lecciones/00-preparar-el-entorno.md).
2. **Haz un fork** (botón *Fork*, arriba a la derecha) y clónalo, para guardar tus cambios en tu propia copia:
   ```
   git clone https://github.com/TU-USUARIO/estructuras-de-datos-lecciones-y-proyectos.git
   ```
3. **Sigue la ruta de estudio** en orden. En cada lección:
   1. Lee la explicación.
   2. Ejecuta el proyecto y úsalo.
   3. Abre los archivos que señala la lección y cambia algo pequeño.
   4. Resuelve los **ejercicios** en una rama propia:
      ```
      git switch -c practica/leccion-03
      ```
   5. Intenta el **reto**, que no trae solución.
   6. Corre las pruebas, para comprobar que no rompiste nada.
4. Si te trabas, mira las diferencias con `git diff main` o vuelve a la versión original con `git switch main`.

Cada lección termina con preguntas de repaso. Si puedes responderlas sin mirar, pasa a la siguiente.

## Ruta de estudio

| # | Lección | Aprendes | Proyecto | Tiempo |
|---|---|---|---|---|
| 00 | [Preparar el entorno](lecciones/00-preparar-el-entorno.md) | Instalar y correr todo | Todos | 30 min |
| 01 | [Listas enlazadas](lecciones/01-listas-enlazadas.md) | Nodos, lista ordenada, doble y circular | `estructuras-lineales-js` | 2 h |
| 02 | [Pilas y colas](lecciones/02-pilas-y-colas.md) | TDA, paréntesis balanceados | `estructuras-lineales-js` | 1.5 h |
| 03 | [Recursividad](lecciones/03-recursividad.md) | Caso base, datos anidados | `datos-y-archivos-python` | 2 h |
| 04 | [Árboles binarios de búsqueda](lecciones/04-arboles-binarios-de-busqueda.md) | Insertar, buscar, eliminar, recorridos | `arboles-y-heap-js` | 2.5 h |
| 05 | [Heap](lecciones/05-heap.md) | Árbol en un arreglo, cola de prioridad | `arboles-y-heap-js` | 1.5 h |
| 06 | [Archivos y datos](lecciones/06-archivos-y-datos.md) | CSV, TSV, JSON, escapar HTML | `datos-y-archivos-python` | 1.5 h |
| 07 | [Complejidad y Big-O](lecciones/07-complejidad-big-o.md) | O, Ω y Θ, contar operaciones | `ordenamiento-y-rendimiento-python` | 2 h |
| 08 | [Ordenamiento](lecciones/08-ordenamiento.md) | Cinco algoritmos, dividir y vencer | `ordenamiento-y-rendimiento-python` | 2.5 h |
| 09 | [Grafos](lecciones/09-grafos.md) | BFS, DFS, retroceso, Dijkstra | `grafos-python` | 3 h |
| 10 | [Bits y cifrado](lecciones/10-bits-y-cifrado.md) | XOR, bytes, UTF-8 | `cifrado-xor-python` | 1.5 h |
| 11 | [Árboles generales y persistencia](lecciones/11-arboles-generales-y-persistencia.md) | Copia profunda, guardar y cargar, PyQt5 | `sistema-de-archivos-pyqt` | 3 h |
| 12 | [Proyecto integrador](lecciones/12-proyecto-integrador.md) | Unir todo, diseñar una métrica | `red-de-servidores-pyqt` | 3 h |

Los tiempos son estimaciones, sin contar los retos.

## Proyectos

| Proyecto | Qué es | Tecnologías | Cómo ejecutarlo |
|---|---|---|---|
| [`estructuras-lineales-js`](proyectos/estructuras-lineales-js) | Listas, pila y cola interactivas | JavaScript | Abrir `index.html` |
| [`arboles-y-heap-js`](proyectos/arboles-y-heap-js) | BST, árbol general y heap, dibujados | JavaScript, SVG | Abrir `index.html` |
| [`datos-y-archivos-python`](proyectos/datos-y-archivos-python) | CSV, TSV y estructuras anidadas | Python | `python main.py` |
| [`ordenamiento-y-rendimiento-python`](proyectos/ordenamiento-y-rendimiento-python) | Cinco algoritmos medidos | Python | `python rendimiento.py` |
| [`grafos-python`](proyectos/grafos-python) | Dos representaciones y cuatro recorridos | Python | `python main.py` |
| [`cifrado-xor-python`](proyectos/cifrado-xor-python) | César y XOR en línea de comandos | Python | `python main.py cesar "Hola" 3` |
| [`sistema-de-archivos-pyqt`](proyectos/sistema-de-archivos-pyqt) | Simulador con dos memorias | Python, PyQt5 | `pip install -r requirements.txt` y `python main.py` |
| [`red-de-servidores-pyqt`](proyectos/red-de-servidores-pyqt) | Rutas, costos y Dijkstra | Python, PyQt5, networkx, matplotlib | `pip install -r requirements.txt` y `python main.py` |

Cada proyecto trae pruebas. Desde su carpeta: `python -m unittest discover -s pruebas -v` o `node --test`.

## Restaurar los datos de ejemplo

El sistema de archivos guarda tus cambios en `Memoria/`. Para volver al inicio:

```
git checkout -- proyectos/sistema-de-archivos-pyqt/Memoria
```

## Estructura

```
lecciones/   13 lecciones en orden
proyectos/   8 proyectos, cada uno con sus pruebas
LICENSE      Licencia MIT
```

## Créditos y avisos

- **Origen:** el sistema de archivos se basa en mi proyecto de un curso universitario de estructuras de datos. Los temas siguen el contenido de ese curso.
- **Datos:** todos los datos de ejemplo son ficticios.
- **Fórmula de costo:** la de `red-de-servidores-pyqt` es un modelo para aprender, no una medida real de redes.
- **Cifrado:** `cifrado-xor-python` es didáctico. No protege datos reales.
- **Iconos de `sistema-de-archivos-pyqt`:** son de terceros, algunos de [icon-icons.com](https://icon-icons.com). Pertenecen a sus autores y no están cubiertos por la licencia de este repositorio.

## Licencia

[MIT](LICENSE). No cubre el material de terceros, como los iconos de `sistema-de-archivos-pyqt`, ni las bibliotecas que se instalan por separado (PyQt5, networkx y matplotlib), que tienen sus propias licencias. PyQt5 usa GPL v3 o una licencia comercial: tenlo en cuenta si distribuyes un programa basado en estos proyectos.
