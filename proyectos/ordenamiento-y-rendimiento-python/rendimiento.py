"""Mide tiempo y comparaciones para ver en la práctica lo que predice la notación O."""
import argparse
import random
import time

from ordenamientos import ALGORITMOS, Contador

CASOS = {
    "aleatorio": lambda n, azar: [azar.randrange(n * 10) for _ in range(n)],
    "ordenado": lambda n, azar: list(range(n)),
    "invertido": lambda n, azar: list(range(n, 0, -1)),
}


def medir(algoritmo, datos):
    """Devuelve (milisegundos, comparaciones). Falla si el resultado no está ordenado."""
    contador = Contador()
    inicio = time.perf_counter()
    resultado = algoritmo(datos, contador)
    milisegundos = (time.perf_counter() - inicio) * 1000
    if resultado != sorted(datos):
        raise AssertionError(f"{algoritmo.__name__} no ordenó correctamente")
    return milisegundos, contador.comparaciones


def tamanos_validos(texto):
    valor = int(texto)
    if valor < 1:
        raise argparse.ArgumentTypeError("los tamaños deben ser mayores que 0")
    return valor


def tabla(tamanos, caso, semilla):
    azar = random.Random(semilla)
    filas = []
    for n in tamanos:
        datos = CASOS[caso](n, azar)
        for nombre, algoritmo in ALGORITMOS.items():
            milisegundos, comparaciones = medir(algoritmo, datos)
            filas.append((nombre, n, comparaciones, milisegundos))
    return filas


def main(argumentos=None):
    analizador = argparse.ArgumentParser(description="Compara algoritmos de ordenamiento")
    analizador.add_argument("--tamanos", nargs="+", type=tamanos_validos, default=[100, 1000, 3000])
    analizador.add_argument("--caso", choices=CASOS, default="aleatorio")
    analizador.add_argument("--semilla", type=int, default=2019)
    opciones = analizador.parse_args(argumentos)

    print(f"Caso: {opciones.caso}\n")
    print(f"{'Algoritmo':<11}{'n':>7}{'Comparaciones':>15}{'Tiempo (ms)':>13}")
    print("-" * 46)
    for nombre, n, comparaciones, milisegundos in tabla(opciones.tamanos, opciones.caso, opciones.semilla):
        print(f"{nombre:<11}{n:>7}{comparaciones:>15}{milisegundos:>13.2f}")


if __name__ == "__main__":
    main()
