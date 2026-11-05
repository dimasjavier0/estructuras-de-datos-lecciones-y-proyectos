"""Demostración: lee ejemplos, genera un CSV y crea salida/arbol.html. Ejecutar con: python main.py"""
import json
from pathlib import Path

from datos import a_lista_html, arbol_a_html, arbol_a_texto, contar_hojas, generar_csv, leer_tabla

CARPETA = Path(__file__).resolve().parent
EJEMPLOS = CARPETA / "ejemplos"
SALIDA = CARPETA / "salida"


def main():
    for nombre in ("productos.csv", "productos.tsv"):
        print(f"{nombre}:")
        for fila in leer_tabla(EJEMPLOS / nombre):
            print("  ", fila)

    SALIDA.mkdir(exist_ok=True)
    (SALIDA / "aleatorio.csv").write_text(generar_csv(3, 5, semilla=42), encoding="utf-8")
    print("\nCSV aleatorio (semilla 42):")
    print((SALIDA / "aleatorio.csv").read_text(encoding="utf-8"))

    carpetas = json.loads((EJEMPLOS / "carpetas.json").read_text(encoding="utf-8"))
    print("carpetas.json como árbol:")
    print("\n".join(arbol_a_texto(carpetas)))
    print(f"\nValores finales: {contar_hojas(carpetas)}")

    pagina = (
        '<!doctype html><html lang="es"><meta charset="utf-8"><title>Árbol</title>'
        f"<h1>Carpetas</h1>{arbol_a_html(carpetas)}"
        f"<h1>Arreglo anidado</h1>{a_lista_html([1, 2, [3, 4, [5, 6]], 7])}</html>"
    )
    (SALIDA / "arbol.html").write_text(pagina, encoding="utf-8")
    print("Creado: salida/arbol.html")


if __name__ == "__main__":
    main()
