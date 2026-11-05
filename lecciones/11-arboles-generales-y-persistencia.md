# Lección 11: árboles generales y persistencia

**Aprenderás:** a modelar un sistema de archivos con un árbol, a copiarlo, a guardarlo en un archivo de texto y a conectarlo con una interfaz.

**Proyectos:** [`sistema-de-archivos-pyqt`](../proyectos/sistema-de-archivos-pyqt), [`arboles-y-heap-js`](../proyectos/arboles-y-heap-js)

**Herramienta nueva:** PyQt5. La instalación está en la [lección 00](00-preparar-el-entorno.md).

## La idea

Las carpetas de una computadora forman un árbol en el que cada nodo tiene cualquier cantidad de hijos. Aquí combinas casi todo lo anterior:

| Pieza | Archivo | Lección |
|---|---|---|
| Lista enlazada ordenada de hijos | [`Nucleo/Clases/Lista.py`](../proyectos/sistema-de-archivos-pyqt/Nucleo/Clases/Lista.py) | 01 |
| Comparador con alfabeto propio | [`Nucleo/Clases/comparar.py`](../proyectos/sistema-de-archivos-pyqt/Nucleo/Clases/comparar.py) | 01 |
| Árbol, copia y ruta | [`Nucleo/Clases/GenericTree.py`](../proyectos/sistema-de-archivos-pyqt/Nucleo/Clases/GenericTree.py) | 03 y 04 |
| Guardar y cargar | [`Nucleo/Clases/TXT.py`](../proyectos/sistema-de-archivos-pyqt/Nucleo/Clases/TXT.py) | 06 |
| Ventana | [`main.py`](../proyectos/sistema-de-archivos-pyqt/main.py) | Nueva |

### Copiar de verdad

Para copiar una carpeta a otro árbol no basta con reutilizar el nodo: un nodo solo puede estar en una lista, y ambos árboles compartirían sus cambios. Hay que clonarla, con recursividad:

```python
def clonar(self, nodo):
    copia = Node(nodo.name)
    if nodo.esCarpeta():
        copia.children = List()
        for hijo in nodo.children.toArray():
            copiaHijo = self.clonar(hijo)
            copiaHijo.parent = copia
            copia.children.addNode(copiaHijo)
    return copia
```

### Guardar un árbol en texto

Cada línea es un nodo, y los tabuladores indican su nivel:

```
root/
	Documentos/
		notas.txt
	leeme.txt
```

Guardar es recorrer el árbol con recursividad. Cargar es lo interesante: `GestionTree.textoATree` lleva una lista `padres`, donde `padres[n]` es la última carpeta vista en el nivel `n`.

También valida. Un archivo dañado no debe cerrar el programa **ni perderse**: `Panel.cargar` lo conserva como `.danado` y empieza vacío.

Además, guarda primero en un archivo temporal y luego lo reemplaza con `os.replace`. Si el programa falla a la mitad, el archivo anterior sigue intacto.

### La interfaz

El diseño está en `Nucleo/GUI/*.ui`, y `uic.loadUi` lo carga. Cada botón se **conecta** a una función, que modifica el árbol y vuelve a pintar la lista. El árbol es la fuente de la verdad: la lista visible solo lo muestra.

## Lee el código

1. Corre `python main.py` y crea una carpeta. Abre `Memoria/Tree-A.mem` con un editor. Para restaurar los datos: `git checkout -- Memoria`.
2. Lee `addNode` en `Lista.py`. ¿Cómo evita los repetidos sin recorrer la lista dos veces?
3. Lee `Copy` en `GenericTree.py`. ¿Qué caso evita `esDescendiente`?
4. Lee `textoATree` en `TXT.py` y síguelo a mano con el ejemplo de arriba. ¿Qué hace `del padres[nivel:]`?
5. Rompe `Tree-A.mem` a propósito, quitando un tabulador, y abre el programa.

## Ejercicios

1. **Básico:** agrega `contarArchivos(nodo)` a `Tree`, con recursividad, y muestra el total en la barra de estado.
2. **Intermedio:** agrega `tamano(nodo)`: guarda un tamaño ficticio para cada archivo en el `.mem` y súmalo en cada carpeta.
3. **Intermedio:** agrega un botón para renombrar. Cuidado: la lista debe seguir ordenada y sin repetidos.

## Reto

Agrega **mover**: copiar y eliminar del origen, también dentro del mismo árbol. Debe impedir mover una carpeta dentro de sí misma, y dejar todo intacto si falla. Agrega pruebas para esos casos.

## Repaso

- ¿Por qué una copia profunda necesita recursividad?
- ¿Para qué sirve la lista `padres` al cargar?
- ¿Por qué guardar en un archivo temporal antes de reemplazar?
- ¿Qué significa que el árbol es la "fuente de la verdad"?

Siguiente: [Lección 12: proyecto integrador](12-proyecto-integrador.md)
