"""Algoritmos de ordenamiento. Cada uno devuelve una lista nueva y cuenta sus comparaciones."""


class Contador:
    """Comparaciones realizadas: el conteo no depende de qué tan rápida sea la computadora."""

    def __init__(self):
        self.comparaciones = 0

    def mayor(self, a, b):
        self.comparaciones += 1
        return a > b


def burbuja(datos, contador=None):
    """O(n²); O(n) si ya está ordenada, porque se detiene cuando una pasada no intercambia nada."""
    contador = contador or Contador()
    lista = list(datos)
    for fin in range(len(lista) - 1, 0, -1):
        hubo_cambio = False
        for i in range(fin):
            if contador.mayor(lista[i], lista[i + 1]):
                lista[i], lista[i + 1] = lista[i + 1], lista[i]
                hubo_cambio = True
        if not hubo_cambio:
            break
    return lista


def insercion(datos, contador=None):
    """O(n²); O(n) si ya está ordenada."""
    contador = contador or Contador()
    lista = list(datos)
    for i in range(1, len(lista)):
        actual = lista[i]
        j = i
        while j > 0 and contador.mayor(lista[j - 1], actual):
            lista[j] = lista[j - 1]
            j -= 1
        lista[j] = actual
    return lista


def seleccion(datos, contador=None):
    """Siempre O(n²): recorre todo lo pendiente aunque ya esté ordenado."""
    contador = contador or Contador()
    lista = list(datos)
    for i in range(len(lista) - 1):
        menor = i
        for j in range(i + 1, len(lista)):
            if contador.mayor(lista[menor], lista[j]):
                menor = j
        lista[i], lista[menor] = lista[menor], lista[i]
    return lista


def quicksort(datos, contador=None):
    """O(n log n) en promedio; O(n²) si los pivotes quedan muy mal. Usa el elemento del medio como pivote."""
    contador = contador or Contador()
    lista = list(datos)

    def ordenar(inicio, fin):
        if inicio >= fin:
            return
        pivote = lista[(inicio + fin) // 2]
        i, j = inicio, fin
        while i <= j:
            while contador.mayor(pivote, lista[i]):
                i += 1
            while contador.mayor(lista[j], pivote):
                j -= 1
            if i <= j:
                lista[i], lista[j] = lista[j], lista[i]
                i += 1
                j -= 1
        ordenar(inicio, j)
        ordenar(i, fin)

    ordenar(0, len(lista) - 1)
    return lista


def mezcla(datos, contador=None):
    """Siempre O(n log n), a cambio de usar memoria adicional."""
    contador = contador or Contador()

    def ordenar(lista):
        if len(lista) <= 1:
            return list(lista)
        medio = len(lista) // 2
        izquierda, derecha = ordenar(lista[:medio]), ordenar(lista[medio:])
        resultado = []
        i = j = 0
        while i < len(izquierda) and j < len(derecha):
            if contador.mayor(izquierda[i], derecha[j]):
                resultado.append(derecha[j])
                j += 1
            else:
                resultado.append(izquierda[i])
                i += 1
        return resultado + izquierda[i:] + derecha[j:]

    return ordenar(list(datos))


ALGORITMOS = {
    "burbuja": burbuja,
    "inserción": insercion,
    "selección": seleccion,
    "quicksort": quicksort,
    "mezcla": mezcla,
}
