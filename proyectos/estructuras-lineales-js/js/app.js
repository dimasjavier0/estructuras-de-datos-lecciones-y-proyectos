/* Conecta las estructuras con la página. Los valores siempre se muestran con textContent. */

const OPCIONES = {
  enlazada: {
    titulo: "Lista enlazada",
    crear: () => new ListaEnlazada(),
    idea: "Cada nodo apunta al siguiente. Agregar al final recorre toda la lista: O(n).",
    conector: "→",
    fin: "null",
    acciones: ["agregar", "alInicio", "eliminar", "buscar", "invertir"],
  },
  ordenada: {
    titulo: "Lista ordenada",
    crear: () => new ListaOrdenada(),
    idea: "Cada valor se inserta en su lugar, así que la lista nunca se desordena.",
    conector: "→",
    fin: "null",
    acciones: ["agregar", "eliminar", "buscar"],
  },
  doble: {
    titulo: "Lista doble",
    crear: () => new ListaDoble(),
    idea: "Cada nodo conoce al siguiente y al anterior. Como guarda el último, agregar es O(1).",
    conector: "⇄",
    fin: "null",
    acciones: ["agregar", "eliminar", "buscar"],
  },
  circular: {
    titulo: "Lista circular",
    crear: () => new ListaCircular(),
    idea: "El último nodo apunta al primero: no hay null al final.",
    conector: "→",
    fin: "↺ vuelve al primero",
    acciones: ["agregar", "eliminar", "buscar"],
  },
  pila: {
    titulo: "Pila",
    crear: () => new Pila(),
    idea: "El último en entrar es el primero en salir, como una pila de platos.",
    conector: "→",
    fin: "null",
    acciones: ["apilar", "desapilar"],
  },
  cola: {
    titulo: "Cola",
    crear: () => new Cola(),
    idea: "El primero en entrar es el primero en salir, como una fila en el banco.",
    conector: "→",
    fin: "null",
    acciones: ["encolar", "desencolar"],
  },
};

const ETIQUETAS = {
  agregar: "Agregar",
  alInicio: "Agregar al inicio",
  eliminar: "Eliminar",
  buscar: "Buscar",
  invertir: "Invertir",
  apilar: "Apilar",
  desapilar: "Desapilar",
  encolar: "Encolar",
  desencolar: "Desencolar",
};
const SIN_VALOR = new Set(["invertir", "desapilar", "desencolar"]);

const elementos = {
  selector: document.querySelector("#selector"),
  idea: document.querySelector("#idea"),
  formulario: document.querySelector("#formulario"),
  valor: document.querySelector("#valor"),
  acciones: document.querySelector("#acciones"),
  vista: document.querySelector("#vista"),
  mensaje: document.querySelector("#mensaje"),
  tamano: document.querySelector("#tamano"),
  limpiar: document.querySelector("#limpiar"),
  textoBalance: document.querySelector("#texto-balance"),
  resultadoBalance: document.querySelector("#resultado-balance"),
};

let actual = "enlazada";
const estructuras = {};
for (const clave of Object.keys(OPCIONES)) estructuras[clave] = OPCIONES[clave].crear();

function mostrarMensaje(texto, tipo = "") {
  elementos.mensaje.textContent = texto;
  elementos.mensaje.className = tipo;
}

function dibujar(resaltado = -1) {
  const opcion = OPCIONES[actual];
  const estructura = estructuras[actual];
  const valores = estructura.aArreglo();
  elementos.vista.replaceChildren();

  if (valores.length === 0) {
    const vacio = document.createElement("p");
    vacio.className = "vacio";
    vacio.textContent = "Vacía. Agrega un valor para empezar.";
    elementos.vista.append(vacio);
  }
  valores.forEach((valor, indice) => {
    const nodo = document.createElement("div");
    nodo.className = indice === resaltado ? "nodo resaltado" : "nodo";
    nodo.textContent = valor;
    elementos.vista.append(nodo);
    const conector = document.createElement("span");
    conector.className = "conector";
    conector.textContent = indice === valores.length - 1 ? `→ ${opcion.fin}` : opcion.conector;
    elementos.vista.append(conector);
  });
  elementos.tamano.textContent = `Elementos: ${estructura.tamano}`;
}

function cambiarEstructura(clave) {
  actual = clave;
  const opcion = OPCIONES[clave];
  elementos.idea.textContent = opcion.idea;
  elementos.acciones.replaceChildren();
  for (const accion of opcion.acciones) {
    const boton = document.createElement("button");
    boton.type = "button";
    boton.textContent = ETIQUETAS[accion];
    boton.dataset.accion = accion;
    elementos.acciones.append(boton);
  }
  for (const pestana of elementos.selector.querySelectorAll("button")) {
    pestana.setAttribute("aria-pressed", String(pestana.dataset.clave === clave));
  }
  mostrarMensaje("");
  dibujar();
}

function ejecutar(accion) {
  const estructura = estructuras[actual];
  const valor = elementos.valor.value.trim();

  if (!SIN_VALOR.has(accion) && valor === "") {
    mostrarMensaje("Escribe un valor primero.", "error");
    elementos.valor.focus();
    return;
  }

  try {
    switch (accion) {
      case "agregar": estructura.agregar(valor); mostrarMensaje(`Se agregó «${valor}».`); break;
      case "alInicio": estructura.agregarAlInicio(valor); mostrarMensaje(`«${valor}» quedó de primero.`); break;
      case "apilar": estructura.apilar(valor); mostrarMensaje(`«${valor}» quedó en el tope.`); break;
      case "encolar": estructura.encolar(valor); mostrarMensaje(`«${valor}» entró al final de la cola.`); break;
      case "desapilar": mostrarMensaje(`Salió «${estructura.desapilar()}».`); break;
      case "desencolar": mostrarMensaje(`Salió «${estructura.desencolar()}».`); break;
      case "invertir":
        estructura.invertir();
        mostrarMensaje(estructura.tamano ? "La lista quedó invertida." : "La lista está vacía.");
        break;
      case "eliminar":
        if (estructura.eliminar(valor)) mostrarMensaje(`Se eliminó «${valor}».`);
        else mostrarMensaje(`«${valor}» no está en la lista.`, "error");
        break;
      case "buscar": {
        const posicion = estructura.buscar(valor);
        if (posicion >= 0) mostrarMensaje(`«${valor}» está en la posición ${posicion}.`);
        else mostrarMensaje(`«${valor}» no está en la lista.`, "error");
        dibujar(posicion);
        return;
      }
    }
  } catch (error) {
    mostrarMensaje(error.message, "error");
  }

  if (!SIN_VALOR.has(accion)) {
    elementos.valor.value = "";
    elementos.valor.focus();
  }
  dibujar();
}

for (const clave of Object.keys(OPCIONES)) {
  const pestana = document.createElement("button");
  pestana.type = "button";
  pestana.textContent = OPCIONES[clave].titulo;
  pestana.dataset.clave = clave;
  elementos.selector.append(pestana);
}

elementos.selector.addEventListener("click", (evento) => {
  const clave = evento.target.dataset.clave;
  if (clave) cambiarEstructura(clave);
});
elementos.acciones.addEventListener("click", (evento) => {
  const accion = evento.target.dataset.accion;
  if (accion) ejecutar(accion);
});
elementos.formulario.addEventListener("submit", (evento) => {
  evento.preventDefault();
  ejecutar(OPCIONES[actual].acciones[0]);
});
elementos.limpiar.addEventListener("click", () => {
  estructuras[actual] = OPCIONES[actual].crear();
  mostrarMensaje("Se vació la estructura.");
  dibujar();
});
elementos.textoBalance.addEventListener("input", () => {
  const texto = elementos.textoBalance.value;
  const balanceado = parentesisBalanceados(texto);
  elementos.resultadoBalance.textContent = texto === "" ? "" : balanceado ? "Balanceado ✓" : "No balanceado ✗";
  elementos.resultadoBalance.className = texto !== "" && !balanceado ? "error" : "";
});

cambiarEstructura("enlazada");
