/* Dibuja las estructuras en la página. Todo el texto entra con textContent. */

const SVG = "http://www.w3.org/2000/svg";
const $ = (selector) => document.querySelector(selector);

function crearSvg(nombre, atributos, texto) {
  const elemento = document.createElementNS(SVG, nombre);
  for (const [clave, valor] of Object.entries(atributos)) elemento.setAttribute(clave, valor);
  if (texto !== undefined) elemento.textContent = texto;
  return elemento;
}

function avisar(salida, texto, esError = false) {
  salida.textContent = texto;
  salida.classList.toggle("error", esError);
}

/* --- Árbol binario --- */
const bst = new ArbolBinarioBusqueda();
for (const valor of [50, 30, 70, 20, 40, 60, 80]) bst.insertar(valor);

function dibujarBinario(resaltados = []) {
  const lienzo = $("#lienzo-bst");
  lienzo.replaceChildren();
  const separacionX = 54;
  const separacionY = 70;
  const posiciones = new Map();
  let columna = 0;
  // El recorrido inorden da la columna de cada nodo, así nunca se enciman
  (function ubicar(nodo, nivel) {
    if (!nodo) return;
    ubicar(nodo.izquierdo, nivel + 1);
    posiciones.set(nodo, { x: 30 + columna * separacionX, y: 30 + nivel * separacionY });
    columna++;
    ubicar(nodo.derecho, nivel + 1);
  })(bst.raiz, 0);

  lienzo.setAttribute("viewBox", `0 0 ${Math.max(60, columna * separacionX + 6)} ${Math.max(60, bst.altura() * separacionY)}`);
  for (const [nodo, punto] of posiciones) {
    for (const hijo of [nodo.izquierdo, nodo.derecho]) {
      if (hijo) {
        const destino = posiciones.get(hijo);
        lienzo.append(crearSvg("line", { x1: punto.x, y1: punto.y, x2: destino.x, y2: destino.y, class: "arista" }));
      }
    }
  }
  for (const [nodo, punto] of posiciones) {
    const clase = resaltados.includes(nodo.valor) ? "vertice resaltado" : "vertice";
    lienzo.append(crearSvg("circle", { cx: punto.x, cy: punto.y, r: 22, class: clase }));
    lienzo.append(crearSvg("text", { x: punto.x, y: punto.y + 5, class: "etiqueta" }, nodo.valor));
  }
  $("#recorridos").replaceChildren();
  const filas = [
    ["Inorden (siempre ordenado)", bst.inorden()],
    ["Preorden", bst.preorden()],
    ["Postorden", bst.postorden()],
    ["Por niveles", bst.porNiveles()],
  ];
  for (const [nombre, valores] of filas) {
    const fila = document.createElement("tr");
    const titulo = document.createElement("th");
    titulo.scope = "row";
    titulo.textContent = nombre;
    const dato = document.createElement("td");
    dato.textContent = valores.join(", ") || "—";
    fila.append(titulo, dato);
    $("#recorridos").append(fila);
  }
  $("#datos-bst").textContent = `Nodos: ${bst.tamano} · Altura: ${bst.altura()}`;
}

function operarBinario(operacion) {
  const salida = $("#mensaje-bst");
  const valor = leerEntero($("#valor-bst").value);
  if (valor === null) {
    avisar(salida, "Escribe un número entero.", true);
    return;
  }
  let resaltados = [];
  if (operacion === "insertar") {
    if (bst.insertar(valor)) avisar(salida, `Se insertó ${valor}.`);
    else avisar(salida, `${valor} ya está en el árbol.`, true);
  } else if (operacion === "eliminar") {
    if (bst.eliminar(valor)) avisar(salida, `Se eliminó ${valor}.`);
    else avisar(salida, `${valor} no está en el árbol.`, true);
  } else {
    const { encontrado, camino } = bst.buscar(valor);
    resaltados = camino;
    const recorrido = camino.join(" → ") || "árbol vacío";
    avisar(salida, `${encontrado ? "Encontrado" : "No está"}. Se visitó: ${recorrido}.`, !encontrado);
  }
  dibujarBinario(resaltados);
}

$("#form-bst").addEventListener("submit", (evento) => {
  evento.preventDefault();
  operarBinario("insertar");
});
$("#buscar-bst").addEventListener("click", () => operarBinario("buscar"));
$("#eliminar-bst").addEventListener("click", () => operarBinario("eliminar"));

/* --- Árbol general --- */
const general = new ArbolGeneral("raiz");
general.agregar("documentos");
general.agregar("fotos");
general.agregar("informes", "documentos");
general.agregar("plan.txt", "informes");
general.agregar("viaje.png", "fotos");

function pintarRama(nodo) {
  const elemento = document.createElement("li");
  elemento.textContent = nodo.valor;
  if (nodo.hijos.length > 0) {
    const lista = document.createElement("ul");
    for (const hijo of nodo.hijos) lista.append(pintarRama(hijo));
    elemento.append(lista);
  }
  return elemento;
}

function dibujarGeneral() {
  const lista = document.createElement("ul");
  lista.append(pintarRama(general.raiz));
  $("#vista-general").replaceChildren(lista);
  const selector = $("#padre-general");
  const elegido = selector.value;
  selector.replaceChildren();
  (function agregarOpciones(nodo) {
    selector.append(new Option(nodo.valor, nodo.valor));
    nodo.hijos.forEach(agregarOpciones);
  })(general.raiz);
  if (elegido) selector.value = elegido;
  $("#datos-general").textContent = `Profundidad: ${general.profundidad()}`;
}

$("#form-general").addEventListener("submit", (evento) => {
  evento.preventDefault();
  const salida = $("#mensaje-general");
  const valor = $("#valor-general").value.trim();
  if (!valor) {
    avisar(salida, "Escribe un nombre.", true);
    return;
  }
  try {
    general.agregar(valor, $("#padre-general").value);
    avisar(salida, `Camino: ${general.camino(valor).join(" / ")}`);
    $("#valor-general").value = "";
    dibujarGeneral();
  } catch (error) {
    avisar(salida, error.message, true);
  }
});

/* --- Montículo --- */
let monticulo = new Monticulo("max");
for (const valor of [12, 40, 7, 25, 3, 18]) monticulo.insertar(valor);

function dibujarMonticulo() {
  const tabla = $("#tabla-monticulo");
  tabla.replaceChildren();
  const niveles = monticulo.aNiveles();
  const columnas = 2 ** niveles.length - 1;
  niveles.forEach((nivel, n) => {
    const fila = document.createElement("tr");
    const ancho = 2 ** (niveles.length - n);
    const hueco = (ancho / 2) - 1;
    let usadas = 0;
    const agregarVacia = (cuantas) => {
      if (cuantas > 0) {
        const vacia = document.createElement("td");
        vacia.colSpan = cuantas;
        vacia.className = "hueco";
        fila.append(vacia);
        usadas += cuantas;
      }
    };
    nivel.forEach((valor, i) => {
      agregarVacia(i === 0 ? hueco : ancho - 1);
      const celda = document.createElement("td");
      celda.textContent = valor;
      fila.append(celda);
      usadas++;
    });
    agregarVacia(columnas - usadas);
    tabla.append(fila);
  });
  $("#arreglo-monticulo").textContent = monticulo.datos.length ? `Arreglo: [${monticulo.datos.join(", ")}]` : "Arreglo vacío";
}

$("#form-monticulo").addEventListener("submit", (evento) => {
  evento.preventDefault();
  const salida = $("#mensaje-monticulo");
  const valor = leerEntero($("#valor-monticulo").value);
  if (valor === null) {
    avisar(salida, "Escribe un número entero.", true);
    return;
  }
  monticulo.insertar(valor);
  avisar(salida, `Se insertó ${valor}; la raíz es ${monticulo.verRaiz()}.`);
  $("#valor-monticulo").value = "";
  dibujarMonticulo();
});
$("#extraer-monticulo").addEventListener("click", () => {
  const salida = $("#mensaje-monticulo");
  try {
    avisar(salida, `Salió ${monticulo.extraer()}.`);
  } catch (error) {
    avisar(salida, error.message, true);
  }
  dibujarMonticulo();
});
$("#tipo-monticulo").addEventListener("change", (evento) => {
  const anterior = monticulo.datos;
  monticulo = new Monticulo(evento.target.value);
  for (const valor of anterior) monticulo.insertar(valor);
  avisar($("#mensaje-monticulo"), `Se reconstruyó como montículo de ${evento.target.value === "max" ? "máximos" : "mínimos"}.`);
  dibujarMonticulo();
});

dibujarBinario();
dibujarGeneral();
dibujarMonticulo();
