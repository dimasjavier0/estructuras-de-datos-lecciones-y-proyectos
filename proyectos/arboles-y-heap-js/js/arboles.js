/* Árbol binario de búsqueda, árbol general y montículo (heap), sin bibliotecas. */

class NodoBinario {
  constructor(valor) {
    this.valor = valor;
    this.izquierdo = null;
    this.derecho = null;
  }
}

/* A la izquierda de cada nodo van los menores; a la derecha, los mayores. No guarda repetidos. */
class ArbolBinarioBusqueda {
  constructor() {
    this.raiz = null;
    this.tamano = 0;
  }

  insertar(valor) {
    const nuevo = new NodoBinario(valor);
    if (!this.raiz) {
      this.raiz = nuevo;
      this.tamano++;
      return true;
    }
    let actual = this.raiz;
    while (true) {
      if (valor === actual.valor) return false;
      const lado = valor < actual.valor ? "izquierdo" : "derecho";
      if (!actual[lado]) {
        actual[lado] = nuevo;
        this.tamano++;
        return true;
      }
      actual = actual[lado];
    }
  }

  /* Devuelve el camino recorrido, para ver que solo se visita una rama. */
  buscar(valor) {
    const camino = [];
    let actual = this.raiz;
    while (actual) {
      camino.push(actual.valor);
      if (valor === actual.valor) return { encontrado: true, camino };
      actual = valor < actual.valor ? actual.izquierdo : actual.derecho;
    }
    return { encontrado: false, camino };
  }

  eliminar(valor) {
    const antes = this.tamano;
    this.raiz = this._eliminar(this.raiz, valor);
    return this.tamano < antes;
  }

  _eliminar(nodo, valor) {
    if (!nodo) return null;
    if (valor < nodo.valor) {
      nodo.izquierdo = this._eliminar(nodo.izquierdo, valor);
    } else if (valor > nodo.valor) {
      nodo.derecho = this._eliminar(nodo.derecho, valor);
    } else if (nodo.izquierdo && nodo.derecho) {
      // Dos hijos: lo reemplaza su sucesor, el menor de la rama derecha
      let sucesor = nodo.derecho;
      while (sucesor.izquierdo) sucesor = sucesor.izquierdo;
      nodo.valor = sucesor.valor;
      nodo.derecho = this._eliminar(nodo.derecho, sucesor.valor);
    } else {
      // Cero o un hijo: el hijo ocupa su lugar
      this.tamano--;
      return nodo.izquierdo || nodo.derecho;
    }
    return nodo;
  }

  inorden(nodo = this.raiz, salida = []) {
    if (nodo) {
      this.inorden(nodo.izquierdo, salida);
      salida.push(nodo.valor);
      this.inorden(nodo.derecho, salida);
    }
    return salida;
  }

  preorden(nodo = this.raiz, salida = []) {
    if (nodo) {
      salida.push(nodo.valor);
      this.preorden(nodo.izquierdo, salida);
      this.preorden(nodo.derecho, salida);
    }
    return salida;
  }

  postorden(nodo = this.raiz, salida = []) {
    if (nodo) {
      this.postorden(nodo.izquierdo, salida);
      this.postorden(nodo.derecho, salida);
      salida.push(nodo.valor);
    }
    return salida;
  }

  porNiveles() {
    const salida = [];
    const cola = this.raiz ? [this.raiz] : [];
    for (let i = 0; i < cola.length; i++) {
      salida.push(cola[i].valor);
      if (cola[i].izquierdo) cola.push(cola[i].izquierdo);
      if (cola[i].derecho) cola.push(cola[i].derecho);
    }
    return salida;
  }

  altura(nodo = this.raiz) {
    return nodo ? 1 + Math.max(this.altura(nodo.izquierdo), this.altura(nodo.derecho)) : 0;
  }
}

/* Cada nodo tiene cualquier cantidad de hijos, como las carpetas de una computadora. */
class NodoGeneral {
  constructor(valor) {
    this.valor = valor;
    this.hijos = [];
  }
}

class ArbolGeneral {
  constructor(valorRaiz = "/") {
    this.raiz = new NodoGeneral(valorRaiz);
  }

  buscar(valor, nodo = this.raiz) {
    if (nodo.valor === valor) return nodo;
    for (const hijo of nodo.hijos) {
      const encontrado = this.buscar(valor, hijo);
      if (encontrado) return encontrado;
    }
    return null;
  }

  /* Los valores son únicos en todo el árbol, para poder buscarlos sin ambigüedad. */
  agregar(valor, valorPadre = this.raiz.valor) {
    if (this.buscar(valor)) throw new Error(`«${valor}» ya existe`);
    const padre = this.buscar(valorPadre);
    if (!padre) throw new Error(`No existe el padre «${valorPadre}»`);
    const nuevo = new NodoGeneral(valor);
    padre.hijos.push(nuevo);
    return nuevo;
  }

  /* Camino desde la raíz hasta el valor, o null. */
  camino(valor, nodo = this.raiz) {
    if (nodo.valor === valor) return [nodo.valor];
    for (const hijo of nodo.hijos) {
      const resto = this.camino(valor, hijo);
      if (resto) return [nodo.valor, ...resto];
    }
    return null;
  }

  profundidad(nodo = this.raiz) {
    return 1 + Math.max(0, ...nodo.hijos.map((hijo) => this.profundidad(hijo)));
  }

  /* Una línea por nodo, con sangría según su nivel. */
  aTexto(nodo = this.raiz, nivel = 0) {
    return ["  ".repeat(nivel) + nodo.valor, ...nodo.hijos.flatMap((hijo) => this.aTexto(hijo, nivel + 1))];
  }
}

/* Árbol completo guardado en un arreglo: los hijos de i están en 2i+1 y 2i+2. */
class Monticulo {
  /* tipo "max": la raíz es el mayor; tipo "min": la raíz es el menor. */
  constructor(tipo = "max") {
    this.datos = [];
    this.tipo = tipo;
  }

  _antes(a, b) {
    return this.tipo === "max" ? a > b : a < b;
  }

  _intercambiar(i, j) {
    [this.datos[i], this.datos[j]] = [this.datos[j], this.datos[i]];
  }

  /* O(log n): sube mientras le gane a su padre. */
  insertar(valor) {
    this.datos.push(valor);
    let i = this.datos.length - 1;
    while (i > 0) {
      const padre = Math.floor((i - 1) / 2);
      if (!this._antes(this.datos[i], this.datos[padre])) break;
      this._intercambiar(i, padre);
      i = padre;
    }
  }

  verRaiz() {
    if (this.datos.length === 0) throw new Error("El montículo está vacío");
    return this.datos[0];
  }

  /* O(log n): el último pasa a la raíz y baja hasta su lugar. */
  extraer() {
    if (this.datos.length === 0) throw new Error("El montículo está vacío");
    const raiz = this.datos[0];
    const ultimo = this.datos.pop();
    if (this.datos.length > 0) {
      this.datos[0] = ultimo;
      let i = 0;
      while (true) {
        const izquierdo = 2 * i + 1;
        const derecho = 2 * i + 2;
        let elegido = i;
        if (izquierdo < this.datos.length && this._antes(this.datos[izquierdo], this.datos[elegido])) elegido = izquierdo;
        if (derecho < this.datos.length && this._antes(this.datos[derecho], this.datos[elegido])) elegido = derecho;
        if (elegido === i) break;
        this._intercambiar(i, elegido);
        i = elegido;
      }
    }
    return raiz;
  }

  /* Convierte el arreglo en una matriz por niveles para pintarlo como tabla. */
  aNiveles() {
    const niveles = [];
    for (let inicio = 0, ancho = 1; inicio < this.datos.length; inicio += ancho, ancho *= 2) {
      niveles.push(this.datos.slice(inicio, inicio + ancho));
    }
    return niveles;
  }
}

/* Ordena sin modificar la entrada: O(n log n). */
function ordenarConMonticulo(valores) {
  const monticulo = new Monticulo("min");
  for (const valor of valores) monticulo.insertar(valor);
  const resultado = [];
  while (monticulo.datos.length > 0) resultado.push(monticulo.extraer());
  return resultado;
}

/* Convierte lo que escribe el usuario en un número entero, o devuelve null. */
function leerEntero(texto) {
  const limpio = String(texto).trim();
  return /^-?\d+$/.test(limpio) && Math.abs(Number(limpio)) < 1e9 ? Number(limpio) : null;
}

if (typeof module !== "undefined") {
  module.exports = { ArbolBinarioBusqueda, ArbolGeneral, Monticulo, ordenarConMonticulo, leerEntero };
}
