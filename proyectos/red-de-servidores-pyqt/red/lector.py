"""Convierte el texto que escribe el usuario en una Red.

Una línea por enlace; # inicia un comentario y <-> crea el enlace en los dos sentidos:
    Web -> Datos : distancia=80 capacidad=1000 usuarios=25 trafico=200 medio=fibra
"""
import re

from red.modelo import MEDIOS, Enlace, Red

LINEA = re.compile(r"^(?P<origen>[\w.-]+)\s*(?P<flecha><->|->)\s*(?P<destino>[\w.-]+)\s*:\s*(?P<datos>.+)$")
CAMPOS = {"distancia", "capacidad", "usuarios", "trafico", "medio"}


class ErrorDeFormato(Exception):
    """El texto no se puede leer; el mensaje indica la línea."""


def _leer_datos(texto, numero):
    datos = {}
    for par in texto.split():
        if par.count("=") != 1:
            raise ErrorDeFormato(f"Línea {numero}: se esperaba nombre=valor y llegó «{par}»")
        nombre, valor = par.split("=")
        datos[nombre] = valor

    faltan = CAMPOS - datos.keys()
    if faltan:
        raise ErrorDeFormato(f"Línea {numero}: faltan datos: {', '.join(sorted(faltan))}")
    sobran = datos.keys() - CAMPOS
    if sobran:
        raise ErrorDeFormato(f"Línea {numero}: datos desconocidos: {', '.join(sorted(sobran))}")

    for campo in CAMPOS - {"medio"}:
        if not datos[campo].isdigit():
            raise ErrorDeFormato(f"Línea {numero}: {campo} debe ser un entero no negativo")
        datos[campo] = int(datos[campo])

    if datos["medio"] not in MEDIOS:
        raise ErrorDeFormato(f"Línea {numero}: medio desconocido «{datos['medio']}». Usa: {', '.join(MEDIOS)}")
    if datos["distancia"] == 0 or datos["capacidad"] == 0:
        raise ErrorDeFormato(f"Línea {numero}: la distancia y la capacidad deben ser mayores que 0")
    alcance = MEDIOS[datos["medio"]][1]
    if datos["distancia"] > alcance:
        raise ErrorDeFormato(f"Línea {numero}: {datos['medio']} alcanza {alcance} m como máximo")
    return datos


def leer_red(texto):
    red = Red()
    for numero, cruda in enumerate(texto.splitlines(), start=1):
        linea = cruda.split("#")[0].strip()
        if not linea:
            continue
        coincidencia = LINEA.match(linea)
        if not coincidencia:
            raise ErrorDeFormato(f"Línea {numero}: se esperaba «origen -> destino : datos»")
        origen, destino = coincidencia["origen"], coincidencia["destino"]
        if origen == destino:
            raise ErrorDeFormato(f"Línea {numero}: un servidor no puede enlazarse consigo mismo")
        datos = _leer_datos(coincidencia["datos"], numero)
        sentidos = [(origen, destino)]
        if coincidencia["flecha"] == "<->":
            sentidos.append((destino, origen))
        for desde, hacia in sentidos:
            if not red.agregar_enlace(Enlace(desde, hacia, **datos)):
                raise ErrorDeFormato(f"Línea {numero}: el enlace {desde} -> {hacia} está repetido")
    if not red.servidores():
        raise ErrorDeFormato("No hay ningún enlace")
    return red
