/* Estructuras lineales hechas a mano. No usan arreglos para guardar los datos: solo nodos enlazados. */

class Nodo {
  constructor(valor) {
    this.valor = valor;
    this.siguiente = null;
  }
}

class NodoDoble extends Nodo {
  constructor(valor) {
    super(valor);
    this.anterior = null;
  }
}

/* Compara números como números y todo lo demás como texto, para que "10" vaya después de "9". */
function comparar(a, b) {
  const numeroA = Number(a);
  const numeroB = Number(b);
  if (a !== "" && b !== "" && !Number.isNaN(numeroA) && !Number.isNaN(numeroB)) {
    return numeroA - numeroB;
  }
  return String(a).localeCompare(String(b), "es");
}

class ListaEnlazada {
  constructor() {
    this.primero = null;
    this.tamano = 0;
  }

  /* O(n): hay que caminar hasta el último nodo. */
  agregar(valor) {
    const nuevo = new Nodo(valor);
    if (!this.primero) {
      this.primero = nuevo;
    } else {
      let actual = this.primero;
      while (actual.siguiente) actual = actual.siguiente;
      actual.siguiente = nuevo;
    }
    this.tamano++;
  }

  /* O(1): no importa cuántos elementos haya. */
  agregarAlInicio(valor) {
    const nuevo = new Nodo(valor);
    nuevo.siguiente = this.primero;
    this.primero = nuevo;
    this.tamano++;
  }

  buscar(valor) {
    let posicion = 0;
    for (let actual = this.primero; actual; actual = actual.siguiente, posicion++) {
      if (actual.valor === valor) return posicion;
    }
    return -1;
  }

  eliminar(valor) {
    let anterior = null;
    for (let actual = this.primero; actual; anterior = actual, actual = actual.siguiente) {
      if (actual.valor === valor) {
        if (anterior) anterior.siguiente = actual.siguiente;
        else this.primero = actual.siguiente;
        this.tamano--;
        return true;
      }
    }
    return false;
  }

  /* Cambia el sentido de cada enlace, sin crear nodos nuevos. */
  invertir() {
    let anterior = null;
    let actual = this.primero;
    while (actual) {
      const siguiente = actual.siguiente;
      actual.siguiente = anterior;
      anterior = actual;
      actual = siguiente;
    }
    this.primero = anterior;
  }

  aArreglo() {
    const valores = [];
    for (let actual = this.primero; actual; actual = actual.siguiente) valores.push(actual.valor);
    return valores;
  }
}

/* Siempre ordenada: cada elemento se inserta en su lugar. */
class ListaOrdenada extends ListaEnlazada {
  agregar(valor) {
    const nuevo = new Nodo(valor);
    if (!this.primero || comparar(valor, this.primero.valor) < 0) {
      nuevo.siguiente = this.primero;
      this.primero = nuevo;
    } else {
      let actual = this.primero;
      while (actual.siguiente && comparar(actual.siguiente.valor, valor) <= 0) actual = actual.siguiente;
      nuevo.siguiente = actual.siguiente;
      actual.siguiente = nuevo;
    }
    this.tamano++;
  }
}

/* Cada nodo conoce también al anterior, así que se puede recorrer en los dos sentidos. */
class ListaDoble {
  constructor() {
    this.primero = null;
    this.ultimo = null;
    this.tamano = 0;
  }

  /* O(1): se conoce el último nodo. */
  agregar(valor) {
    const nuevo = new NodoDoble(valor);
    if (!this.primero) {
      this.primero = nuevo;
    } else {
      nuevo.anterior = this.ultimo;
      this.ultimo.siguiente = nuevo;
    }
    this.ultimo = nuevo;
    this.tamano++;
  }

  buscar(valor) {
    let posicion = 0;
    for (let actual = this.primero; actual; actual = actual.siguiente, posicion++) {
      if (actual.valor === valor) return posicion;
    }
    return -1;
  }

  eliminar(valor) {
    for (let actual = this.primero; actual; actual = actual.siguiente) {
      if (actual.valor === valor) {
        if (actual.anterior) actual.anterior.siguiente = actual.siguiente;
        else this.primero = actual.siguiente;
        if (actual.siguiente) actual.siguiente.anterior = actual.anterior;
        else this.ultimo = actual.anterior;
        this.tamano--;
        return true;
      }
    }
    return false;
  }

  aArreglo() {
    const valores = [];
    for (let actual = this.primero; actual; actual = actual.siguiente) valores.push(actual.valor);
    return valores;
  }

  aArregloInvertido() {
    const valores = [];
    for (let actual = this.ultimo; actual; actual = actual.anterior) valores.push(actual.valor);
    return valores;
  }
}

/* El último nodo apunta al primero: se recorre con cuidado para no dar vueltas para siempre. */
class ListaCircular {
  constructor() {
    this.ultimo = null;
    this.tamano = 0;
  }

  agregar(valor) {
    const nuevo = new Nodo(valor);
    if (!this.ultimo) {
      nuevo.siguiente = nuevo;
    } else {
      nuevo.siguiente = this.ultimo.siguiente;
      this.ultimo.siguiente = nuevo;
    }
    this.ultimo = nuevo;
    this.tamano++;
  }

  buscar(valor) {
    if (!this.ultimo) return -1;
    let actual = this.ultimo.siguiente;
    for (let posicion = 0; posicion < this.tamano; posicion++, actual = actual.siguiente) {
      if (actual.valor === valor) return posicion;
    }
    return -1;
  }

  eliminar(valor) {
    if (!this.ultimo) return false;
    let anterior = this.ultimo;
    for (let i = 0; i < this.tamano; i++, anterior = anterior.siguiente) {
      const actual = anterior.siguiente;
      if (actual.valor === valor) {
        if (this.tamano === 1) this.ultimo = null;
        else {
          anterior.siguiente = actual.siguiente;
          if (actual === this.ultimo) this.ultimo = anterior;
        }
        this.tamano--;
        return true;
      }
    }
    return false;
  }

  /* Devuelve n valores siguiendo los enlaces; sirve para ver que la lista da la vuelta. */
  recorrer(n) {
    const valores = [];
    if (!this.ultimo) return valores;
    let actual = this.ultimo.siguiente;
    for (let i = 0; i < n; i++, actual = actual.siguiente) valores.push(actual.valor);
    return valores;
  }

  aArreglo() {
    return this.recorrer(this.tamano);
  }
}

/* Último en entrar, primero en salir. Todas sus operaciones son O(1). */
class Pila {
  constructor() {
    this.tope = null;
    this.tamano = 0;
  }

  apilar(valor) {
    const nuevo = new Nodo(valor);
    nuevo.siguiente = this.tope;
    this.tope = nuevo;
    this.tamano++;
  }

  desapilar() {
    if (!this.tope) throw new Error("La pila está vacía");
    const valor = this.tope.valor;
    this.tope = this.tope.siguiente;
    this.tamano--;
    return valor;
  }

  verTope() {
    if (!this.tope) throw new Error("La pila está vacía");
    return this.tope.valor;
  }

  aArreglo() {
    const valores = [];
    for (let actual = this.tope; actual; actual = actual.siguiente) valores.push(actual.valor);
    return valores;
  }
}

/* Primero en entrar, primero en salir. Guarda el último nodo para que encolar sea O(1). */
class Cola {
  constructor() {
    this.frente = null;
    this.final = null;
    this.tamano = 0;
  }

  encolar(valor) {
    const nuevo = new Nodo(valor);
    if (this.final) this.final.siguiente = nuevo;
    else this.frente = nuevo;
    this.final = nuevo;
    this.tamano++;
  }

  desencolar() {
    if (!this.frente) throw new Error("La cola está vacía");
    const valor = this.frente.valor;
    this.frente = this.frente.siguiente;
    if (!this.frente) this.final = null;
    this.tamano--;
    return valor;
  }

  verFrente() {
    if (!this.frente) throw new Error("La cola está vacía");
    return this.frente.valor;
  }

  aArreglo() {
    const valores = [];
    for (let actual = this.frente; actual; actual = actual.siguiente) valores.push(actual.valor);
    return valores;
  }
}

/* Uso clásico de una pila: revisa que paréntesis, corchetes y llaves cierren en orden. */
function parentesisBalanceados(texto) {
  const pares = { ")": "(", "]": "[", "}": "{" };
  const pila = new Pila();
  for (const caracter of texto) {
    if ("([{".includes(caracter)) pila.apilar(caracter);
    else if (caracter in pares) {
      if (pila.tamano === 0 || pila.desapilar() !== pares[caracter]) return false;
    }
  }
  return pila.tamano === 0;
}

if (typeof module !== "undefined") {
  module.exports = {
    Nodo, ListaEnlazada, ListaOrdenada, ListaDoble, ListaCircular, Pila, Cola, comparar, parentesisBalanceados,
  };
}
