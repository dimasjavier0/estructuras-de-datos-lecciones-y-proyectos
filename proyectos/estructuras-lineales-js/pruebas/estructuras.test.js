// Ejecutar desde la carpeta del proyecto: node --test
const test = require("node:test");
const assert = require("node:assert/strict");
const {
  ListaEnlazada, ListaOrdenada, ListaDoble, ListaCircular, Pila, Cola, comparar, parentesisBalanceados,
} = require("../js/estructuras.js");

function llenar(estructura, valores) {
  for (const v of valores) estructura.agregar(v);
  return estructura;
}

test("lista enlazada: agregar, buscar y eliminar en cada posición", () => {
  const lista = llenar(new ListaEnlazada(), ["a", "b", "c", "d"]);
  lista.agregarAlInicio("z");
  assert.deepEqual(lista.aArreglo(), ["z", "a", "b", "c", "d"]);
  assert.equal(lista.buscar("c"), 3);
  assert.equal(lista.buscar("x"), -1);
  assert.equal(lista.eliminar("z"), true);
  assert.equal(lista.eliminar("b"), true);
  assert.equal(lista.eliminar("d"), true);
  assert.equal(lista.eliminar("x"), false);
  assert.deepEqual(lista.aArreglo(), ["a", "c"]);
  assert.equal(lista.tamano, 2);
});

test("lista enlazada: vacía e invertir", () => {
  const lista = new ListaEnlazada();
  assert.equal(lista.eliminar("x"), false);
  assert.equal(lista.buscar("x"), -1);
  lista.invertir();
  assert.deepEqual(lista.aArreglo(), []);
  llenar(lista, [1, 2, 3]).invertir();
  assert.deepEqual(lista.aArreglo(), [3, 2, 1]);
});

test("lista ordenada: números como números y repetidos", () => {
  const lista = llenar(new ListaOrdenada(), ["10", "9", "2", "10", "100"]);
  assert.deepEqual(lista.aArreglo(), ["2", "9", "10", "10", "100"]);
  assert.equal(lista.eliminar("2"), true);
  assert.deepEqual(lista.aArreglo(), ["9", "10", "10", "100"]);
});

test("lista ordenada: texto y mezcla", () => {
  assert.deepEqual(llenar(new ListaOrdenada(), ["pera", "ñame", "uva", "nabo"]).aArreglo(), ["nabo", "ñame", "pera", "uva"]);
  assert.ok(comparar("abc", "5") !== 0);
});

test("lista doble: los enlaces coinciden en los dos sentidos", () => {
  const lista = llenar(new ListaDoble(), [1, 2, 3, 4]);
  assert.deepEqual(lista.aArregloInvertido(), [4, 3, 2, 1]);
  assert.equal(lista.buscar(3), 2);
  lista.eliminar(1);
  lista.eliminar(4);
  lista.eliminar(2);
  assert.equal(lista.eliminar(9), false);
  assert.deepEqual(lista.aArreglo(), [3]);
  assert.deepEqual(lista.aArregloInvertido(), [3]);
  lista.eliminar(3);
  assert.equal(lista.primero, null);
  assert.equal(lista.ultimo, null);
  lista.agregar(7);
  assert.deepEqual(lista.aArregloInvertido(), [7]);
});

test("lista circular: da la vuelta y se puede eliminar en cualquier punto", () => {
  const lista = llenar(new ListaCircular(), ["a", "b", "c"]);
  assert.deepEqual(lista.recorrer(5), ["a", "b", "c", "a", "b"]);
  assert.equal(lista.buscar("c"), 2);
  assert.equal(lista.buscar("x"), -1);
  assert.equal(lista.eliminar("x"), false);
  assert.equal(lista.eliminar("c"), true);
  assert.deepEqual(lista.recorrer(3), ["a", "b", "a"]);
  lista.agregar("d");
  assert.deepEqual(lista.aArreglo(), ["a", "b", "d"]);
  assert.equal(lista.eliminar("a"), true);
  assert.deepEqual(lista.aArreglo(), ["b", "d"]);
  lista.eliminar("b");
  lista.eliminar("d");
  assert.equal(lista.ultimo, null);
  assert.deepEqual(lista.aArreglo(), []);
  assert.equal(lista.eliminar("d"), false);
  assert.equal(lista.buscar("d"), -1);
});

test("pila: último en entrar, primero en salir", () => {
  const pila = new Pila();
  pila.apilar(1);
  pila.apilar(2);
  assert.equal(pila.verTope(), 2);
  assert.deepEqual(pila.aArreglo(), [2, 1]);
  assert.equal(pila.desapilar(), 2);
  assert.equal(pila.desapilar(), 1);
  assert.throws(() => pila.desapilar(), /vacía/);
  assert.throws(() => pila.verTope(), /vacía/);
});

test("cola: primero en entrar, primero en salir, y se puede volver a usar", () => {
  const cola = new Cola();
  cola.encolar(1);
  cola.encolar(2);
  assert.equal(cola.verFrente(), 1);
  assert.equal(cola.desencolar(), 1);
  assert.equal(cola.desencolar(), 2);
  assert.throws(() => cola.desencolar(), /vacía/);
  assert.throws(() => cola.verFrente(), /vacía/);
  cola.encolar(3);
  assert.deepEqual(cola.aArreglo(), [3]);
});

test("paréntesis balanceados", () => {
  for (const bueno of ["", "()", "([]{})", "a(b)c", "((a)[b]){c}"]) assert.equal(parentesisBalanceados(bueno), true, bueno);
  for (const malo of ["(", ")", "(]", "([)]", "((", "())"]) assert.equal(parentesisBalanceados(malo), false, malo);
});
