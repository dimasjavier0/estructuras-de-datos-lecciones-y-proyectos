# -*- encoding: utf8 -*-
from Nucleo.Clases.GenericNode import Node


class Compare:
    """Compara dos nombres con un alfabeto propio; se usa para mantener ordenadas las listas."""

    alphabet = "._-,@#$%&()=!¡?¿[];:~0123456789abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ/"

    def compare(self, ob1, ob2):
        """Devuelve -1 si ob1 va antes, 0 si son iguales y 1 si va después."""
        texto1 = self.aTexto(ob1)
        texto2 = self.aTexto(ob2)

        if texto1 == texto2:
            return 0

        for letra1, letra2 in zip(texto1, texto2):
            posicion1 = self.posicion(letra1)
            posicion2 = self.posicion(letra2)
            if posicion1 < posicion2:
                return -1
            if posicion1 > posicion2:
                return 1

        # Una cadena es el inicio de la otra: la más corta va antes ("Hola" antes que "HolaMundo")
        return -1 if len(texto1) < len(texto2) else 1

    def aTexto(self, ob):
        if isinstance(ob, Node):
            ob = ob.name
        return ("%s" % ob).rstrip(" ")

    def posicion(self, letra):
        # Las letras fuera del alfabeto (acentos, espacios) van después, ordenadas por su código
        indice = self.alphabet.find(letra)
        return indice if indice >= 0 else len(self.alphabet) + ord(letra)
