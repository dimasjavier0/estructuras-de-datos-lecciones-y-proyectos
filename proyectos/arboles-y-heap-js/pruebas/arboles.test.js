// Ejecutar desde la carpeta del proyecto: node --test
const test = require("node:test");
const assert = require("node:assert/strict");
const { ArbolBinarioBusqueda, ArbolGeneral, Monticulo, ordenarConMonticulo, leerEntero } = require("../js/arboles.js");

function arbolDe(valores) {
  const arbol = new ArbolBinarioBusqueda();
  for (const v of valores) arbol.insertar(v);
  return arbol;
}

test("BST: insertar sin repetir y recorridos", () => {
  const arbol = arbolDe([50, 30, 70, 20, 40]);
  assert.equal(arbol.insertar(30), false);
  assert.equal(arbol.tamano, 5);
  assert.deepEqual(arbol.inorden(), [20, 30, 40, 50, 70]);
  assert.deepEqual(arbol.preorden(), [50, 30, 20, 40, 70]);
  assert.deepEqual(arbol.postorden(), [20, 40, 30, 70, 50]);
  assert.deepEqual(arbol.porNiveles(), [50, 30, 70, 20, 40]);
  assert.equal(arbol.altura(), 3);
});

test("BST: buscar devuelve el camino visitado", () => {
  const arbol = arbolDe([50, 30, 70, 20]);
  assert.deepEqual(arbol.buscar(20), { encontrado: true, camino: [50, 30, 20] });
  assert.deepEqual(arbol.buscar(99), { encontrado: false, camino: [50, 70] });
  assert.deepEqual(new ArbolBinarioBusqueda().buscar(1), { encontrado: false, camino: [] });
});

test("BST: eliminar hoja, nodo con un hijo, con dos hijos y la raíz", () => {
  const arbol = arbolDe([50, 30, 70, 20, 40, 60, 80, 35]);
  assert.equal(arbol.eliminar(99), false);
  assert.equal(arbol.eliminar(20), true);  // hoja
  assert.equal(arbol.eliminar(40), true);  // un hijo (35)
  assert.equal(arbol.eliminar(70), true);  // dos hijos
  assert.equal(arbol.eliminar(50), true);  // raíz con dos hijos
  assert.deepEqual(arbol.inorden(), [30, 35, 60, 80]);
  assert.equal(arbol.tamano, 4);
  for (const v of [30, 35, 60, 80]) arbol.eliminar(v);
  assert.equal(arbol.raiz, null);
  assert.equal(arbol.altura(), 0);
  assert.equal(arbol.eliminar(1), false);
});

test("BST: el inorden siempre queda ordenado tras operaciones al azar", () => {
  let semilla = 12345;
  const azar = (n) => (semilla = (semilla * 1103515245 + 12345) % 2147483648) % n;
  const arbol = new ArbolBinarioBusqueda();
  const conjunto = new Set();
  for (let i = 0; i < 2000; i++) {
    const v = azar(200);
    if (azar(3) === 0) {
      assert.equal(arbol.eliminar(v), conjunto.delete(v));
    } else {
      assert.equal(arbol.insertar(v), !conjunto.has(v));
      conjunto.add(v);
    }
  }
  assert.deepEqual(arbol.inorden(), [...conjunto].sort((a, b) => a - b));
  assert.equal(arbol.tamano, conjunto.size);
});

test("árbol general: agregar, buscar, camino y errores", () => {
  const arbol = new ArbolGeneral("raiz");
  arbol.agregar("a");
  arbol.agregar("b");
  arbol.agregar("a1", "a");
  arbol.agregar("a2", "a1");
  assert.equal(arbol.buscar("a2").valor, "a2");
  assert.equal(arbol.buscar("x"), null);
  assert.deepEqual(arbol.camino("a2"), ["raiz", "a", "a1", "a2"]);
  assert.equal(arbol.camino("x"), null);
  assert.equal(arbol.profundidad(), 4);
  assert.deepEqual(arbol.aTexto(), ["raiz", "  a", "    a1", "      a2", "  b"]);
  assert.throws(() => arbol.agregar("a"), /ya existe/);
  assert.throws(() => arbol.agregar("z", "x"), /No existe/);
});

test("montículo: la raíz siempre es el mayor o el menor", () => {
  const maximo = new Monticulo("max");
  const minimo = new Monticulo("min");
  for (const v of [5, 1, 9, 3, 7]) {
    maximo.insertar(v);
    minimo.insertar(v);
  }
  assert.equal(maximo.verRaiz(), 9);
  assert.equal(minimo.verRaiz(), 1);
  assert.deepEqual([maximo.extraer(), maximo.extraer(), maximo.extraer()], [9, 7, 5]);
  assert.deepEqual([minimo.extraer(), minimo.extraer()], [1, 3]);
});

test("montículo: propiedad del padre y niveles", () => {
  const m = new Monticulo("max");
  for (const v of [12, 40, 7, 25, 3, 18, 40]) m.insertar(v);
  for (let i = 1; i < m.datos.length; i++) {
    assert.ok(m.datos[Math.floor((i - 1) / 2)] >= m.datos[i]);
  }
  assert.deepEqual(m.aNiveles().map((n) => n.length), [1, 2, 4]);
});

test("montículo vacío", () => {
  const m = new Monticulo();
  assert.throws(() => m.extraer(), /vacío/);
  assert.throws(() => m.verRaiz(), /vacío/);
  assert.deepEqual(m.aNiveles(), []);
  m.insertar(1);
  assert.equal(m.extraer(), 1);
  assert.deepEqual(m.datos, []);
});

test("ordenar con montículo", () => {
  const entrada = [5, -2, 9, 0, 5, 3];
  assert.deepEqual(ordenarConMonticulo(entrada), [-2, 0, 3, 5, 5, 9]);
  assert.deepEqual(entrada, [5, -2, 9, 0, 5, 3]);
  assert.deepEqual(ordenarConMonticulo([]), []);
});

test("leer enteros", () => {
  assert.equal(leerEntero(" 12 "), 12);
  assert.equal(leerEntero("-3"), -3);
  for (const malo of ["", "abc", "1.5", "1e3", "99999999999", " "]) assert.equal(leerEntero(malo), null, malo);
});
