"""Cifrados clásicos para aprender operaciones con bits. NO son seguros: no protejas datos reales con ellos."""

MINUSCULAS = "abcdefghijklmnñopqrstuvwxyz"
MAYUSCULAS = MINUSCULAS.upper()


def cesar(texto, desplazamiento):
    """Mueve cada letra dentro del alfabeto español; lo demás no cambia. Se descifra con -desplazamiento."""
    resultado = []
    for letra in texto:
        for alfabeto in (MINUSCULAS, MAYUSCULAS):
            if letra in alfabeto:
                letra = alfabeto[(alfabeto.index(letra) + desplazamiento) % len(alfabeto)]
                break
        resultado.append(letra)
    return "".join(resultado)


def xor_bytes(datos, clave):
    """Combina cada byte con un byte de la clave, que se repite. Aplicarlo dos veces devuelve el original."""
    if not clave:
        raise ValueError("La clave no puede estar vacía")
    return bytes(byte ^ clave[i % len(clave)] for i, byte in enumerate(datos))


def cifrar_texto(texto, clave):
    """Devuelve el texto cifrado en hexadecimal, para que se pueda copiar y pegar."""
    return xor_bytes(texto.encode("utf-8"), clave.encode("utf-8")).hex()


def descifrar_texto(hexadecimal, clave):
    try:
        datos = bytes.fromhex(hexadecimal)
    except ValueError:
        raise ValueError("El texto cifrado no es hexadecimal válido") from None
    try:
        return xor_bytes(datos, clave.encode("utf-8")).decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("La clave es incorrecta o los datos están dañados") from None
