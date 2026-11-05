"""Lee y genera archivos de texto, y convierte estructuras anidadas en HTML o en texto con sangría."""
import html
import random


def leer_tabla(ruta):
    """Lee un .csv o un .tsv y devuelve una lista de filas. No admite separadores dentro de comillas."""
    separadores = {".csv": ",", ".tsv": "\t"}
    extension = str(ruta)[str(ruta).rfind("."):].lower() if "." in str(ruta) else ""
    if extension not in separadores:
        raise ValueError(f"Extensión no reconocida: «{extension}». Usa .csv o .tsv")
    with open(ruta, encoding="utf-8") as archivo:
        return [linea.split(separadores[extension]) for linea in archivo.read().splitlines() if linea]


def generar_csv(filas, columnas, semilla=None, minimo=0, maximo=100):
    """Devuelve el texto de un CSV de números aleatorios; con la misma semilla sale el mismo archivo."""
    if filas < 1 or columnas < 1:
        raise ValueError("Debe haber al menos una fila y una columna")
    if minimo > maximo:
        raise ValueError("El mínimo no puede ser mayor que el máximo")
    azar = random.Random(semilla)
    return "\n".join(
        ",".join(str(azar.randint(minimo, maximo)) for _ in range(columnas)) for _ in range(filas)
    ) + "\n"


def a_lista_html(elementos):
    """Convierte un arreglo, con arreglos dentro, en listas <ul> anidadas."""
    partes = ["<ul>"]
    for elemento in elementos:
        if isinstance(elemento, (list, tuple)):
            partes.append(f"<li>{a_lista_html(elemento)}</li>")
        else:
            partes.append(f"<li>{html.escape(str(elemento))}</li>")
    partes.append("</ul>")
    return "".join(partes)


def arbol_a_html(arbol):
    """Convierte un diccionario anidado en listas <ul>; las hojas se muestran como clave: valor."""
    partes = ["<ul>"]
    for clave, valor in arbol.items():
        clave = html.escape(str(clave))
        if isinstance(valor, dict):
            partes.append(f"<li>{clave}{arbol_a_html(valor) if valor else ''}</li>")
        else:
            partes.append(f"<li>{clave}: {html.escape(str(valor))}</li>")
    partes.append("</ul>")
    return "".join(partes)


def arbol_a_texto(arbol, nivel=0):
    """Devuelve el diccionario como texto, con una sangría por cada nivel."""
    lineas = []
    for clave, valor in arbol.items():
        if isinstance(valor, dict):
            lineas.append("    " * nivel + str(clave))
            lineas.extend(arbol_a_texto(valor, nivel + 1))
        else:
            lineas.append("    " * nivel + f"{clave}: {valor}")
    return lineas


def contar_hojas(arbol):
    """Cuántos valores finales tiene el árbol; una carpeta vacía no cuenta."""
    return sum(contar_hojas(v) if isinstance(v, dict) else 1 for v in arbol.values())
