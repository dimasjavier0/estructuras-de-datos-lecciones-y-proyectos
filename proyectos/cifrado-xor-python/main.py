"""Línea de comandos para los cifrados. Ejemplos:
    python main.py cesar "Hola mundo" 3
    python main.py cifrar "Hola mundo" mi-clave
    python main.py descifrar 25061f13... mi-clave
    python main.py archivo entrada.txt salida.bin mi-clave
"""
import argparse
import sys
from pathlib import Path

from cifrado import cesar, cifrar_texto, descifrar_texto, xor_bytes


def main(argumentos=None):
    analizador = argparse.ArgumentParser(description="Cifrado César y XOR (solo para aprender)")
    comandos = analizador.add_subparsers(dest="comando", required=True)

    uno = comandos.add_parser("cesar", help="mueve las letras en el alfabeto")
    uno.add_argument("texto")
    uno.add_argument("desplazamiento", type=int)

    for nombre in ("cifrar", "descifrar"):
        otro = comandos.add_parser(nombre, help=f"{nombre} texto con XOR")
        otro.add_argument("texto")
        otro.add_argument("clave")

    archivo = comandos.add_parser("archivo", help="aplica XOR a un archivo (cifra y descifra)")
    archivo.add_argument("entrada", type=Path)
    archivo.add_argument("salida", type=Path)
    archivo.add_argument("clave")

    opciones = analizador.parse_args(argumentos)
    try:
        if opciones.comando == "cesar":
            print(cesar(opciones.texto, opciones.desplazamiento))
        elif opciones.comando == "cifrar":
            print(cifrar_texto(opciones.texto, opciones.clave))
        elif opciones.comando == "descifrar":
            print(descifrar_texto(opciones.texto, opciones.clave))
        else:
            opciones.salida.write_bytes(xor_bytes(opciones.entrada.read_bytes(), opciones.clave.encode("utf-8")))
            print(f"Escrito: {opciones.salida}")
    except (ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
