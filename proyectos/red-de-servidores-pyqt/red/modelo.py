"""Modelo de la red: servidores (vértices) unidos por enlaces (aristas dirigidas con datos)."""
from dataclasses import dataclass

# medio: (confiabilidad de 0 a 1, alcance máximo en metros)
MEDIOS = {
    "fibra": (0.99, 40000),
    "cat6": (0.97, 100),
    "cat5": (0.95, 100),
    "coaxial": (0.92, 500),
    "wifi": (0.80, 100),
}


@dataclass(frozen=True)
class Enlace:
    origen: str
    destino: str
    distancia: int   # metros
    capacidad: int   # Mbps
    usuarios: int
    trafico: int     # Mbps en uso
    medio: str

    @property
    def costo(self):
        """Cuánto cuesta usar el enlace; a menor costo, mejor. Nunca es negativo."""
        ocupacion = self.trafico / self.capacidad
        confiabilidad = MEDIOS[self.medio][0]
        return round(self.distancia / 100 + 10 * ocupacion + 20 * (1 - confiabilidad) + self.usuarios / 100, 2)

    @property
    def disponible(self):
        return max(0, self.capacidad - self.trafico)


class Red:
    """Grafo dirigido guardado como lista de adyacencia: {servidor: {vecino: Enlace}}."""

    def __init__(self):
        self.adyacencia = {}

    def agregar_servidor(self, nombre):
        self.adyacencia.setdefault(nombre, {})

    def agregar_enlace(self, enlace):
        """Devuelve False si ese enlace ya existía."""
        self.agregar_servidor(enlace.origen)
        self.agregar_servidor(enlace.destino)
        if enlace.destino in self.adyacencia[enlace.origen]:
            return False
        self.adyacencia[enlace.origen][enlace.destino] = enlace
        return True

    def servidores(self):
        return sorted(self.adyacencia)

    def enlaces(self):
        return [e for vecinos in self.adyacencia.values() for e in vecinos.values()]

    def vecinos(self, servidor):
        return sorted(self.adyacencia.get(servidor, {}))

    def enlace(self, origen, destino):
        return self.adyacencia[origen][destino]

    def __contains__(self, servidor):
        return servidor in self.adyacencia
