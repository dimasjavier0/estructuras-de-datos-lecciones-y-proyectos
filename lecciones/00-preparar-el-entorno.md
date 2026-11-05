# Lección 00: preparar el entorno

**Aprenderás:** a dejar lista tu computadora y a correr un proyecto de cada tipo.

**Proyectos:** todos, en [`../proyectos`](../proyectos)

## Qué necesitas

| Herramienta | Para qué | Cómo comprobarla |
|---|---|---|
| Un navegador | Proyectos de JavaScript | |
| Un editor (por ejemplo, VS Code) | Leer y cambiar el código | |
| [Python 3.10 o más nuevo](https://www.python.org/downloads/) | Proyectos de Python | `python --version` |
| [Git](https://git-scm.com/) | Guardar tu práctica en ramas | `git --version` |
| [Node.js 20 o más nuevo](https://nodejs.org/) | Solo para las pruebas de JavaScript | `node --version` |

## Obtener el código

Haz un *fork* en GitHub y clona tu copia:

```
git clone https://github.com/TU-USUARIO/estructuras-de-datos-lecciones-y-proyectos.git
cd estructuras-de-datos-lecciones-y-proyectos
```

## Correr un proyecto de cada tipo

**JavaScript:** abre `proyectos/estructuras-lineales-js/index.html` con doble clic. No hay nada que instalar.

**Python sin dependencias:**

```
cd proyectos/grafos-python
python main.py
```

Debe terminar con `BFS desde la Biblioteca: Biblioteca → Museo → Parque → Teatro → Estadio`.

**Python con interfaz gráfica:** los proyectos con PyQt5 necesitan bibliotecas. Instálalas en un entorno virtual, para no mezclarlas con tu Python:

```
cd proyectos/red-de-servidores-pyqt
python -m venv .venv
.venv\Scripts\activate          (en Windows)
source .venv/bin/activate       (en macOS o Linux)
pip install -r requirements.txt
python main.py
```

Si pip falla con un error de certificado (`CERTIFICATE_VERIFY_FAILED`), suele ser por la red de una empresa o universidad. Prueba `pip install --use-feature=truststore -r requirements.txt`, que usa los certificados de tu sistema. Evita `--trusted-host`, porque desactiva la verificación.

## Correr las pruebas

Cada proyecto trae pruebas automáticas. Sirven para comprobar que todo funciona y para ver cómo se usa cada función. Desde la carpeta del proyecto:

```
python -m unittest discover -s pruebas -v     (Python)
node --test                                   (JavaScript)
```

## Ejercicios

1. Corre las pruebas de `grafos-python` y de `estructuras-lineales-js`.
2. Cambia una distancia en `construir_mapa()` de `grafos-python/main.py` y vuelve a correr las pruebas. ¿Cuál falla, y por qué?
3. Crea una rama para tu práctica y deshaz el cambio: `git switch -c practica/leccion-00`, y luego `git checkout -- .`

## Repaso

- ¿Para qué sirve un entorno virtual?
- ¿Por qué conviene practicar en una rama propia?

Siguiente: [Lección 01: listas enlazadas](01-listas-enlazadas.md)
