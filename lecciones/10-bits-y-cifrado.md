# Lección 10: bits y cifrado

**Aprenderás:** a trabajar con bytes y operaciones binarias, y por qué estos cifrados clásicos no son seguros.

**Proyectos:** [`cifrado-xor-python`](../proyectos/cifrado-xor-python)

> Estos cifrados son para aprender. **Para proteger datos reales usa bibliotecas probadas**, nunca un cifrado propio.

## La idea

### César

Mueve cada letra una cantidad fija: con 3, `a` pasa a `d`. Se descifra moviendo al revés. Con el alfabeto español solo hay 27 claves posibles, así que basta probarlas todas.

### Operaciones binarias

| a | b | a AND b | a OR b | a XOR b |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 | 1 |
| 1 | 0 | 0 | 1 | 1 |
| 1 | 1 | 1 | 1 | 0 |

XOR da 1 cuando los bits son **distintos**, y tiene una propiedad muy útil: aplicar dos veces la misma clave devuelve el original, porque `(a ^ k) ^ k == a`.

```
01100001   'a'
01100010   'b' (la clave)
00000011   cifrado (3)
01100010   'b' otra vez
01100001   'a'
```

Así se aplica en [`cifrado.py`](../proyectos/cifrado-xor-python/cifrado.py), repitiendo la clave con el operador `%`:

```python
def xor_bytes(datos, clave):
    if not clave:
        raise ValueError("La clave no puede estar vacía")
    return bytes(byte ^ clave[i % len(clave)] for i, byte in enumerate(datos))
```

### Texto y bytes

Un carácter no siempre es un byte: en UTF-8, `ñ` ocupa dos. Por eso primero se codifica el texto y luego se opera sobre bytes. Si operaras carácter por carácter, los acentos y los emojis se romperían.

El resultado rara vez es texto imprimible, así que se muestra en **hexadecimal**:

```
cd proyectos/cifrado-xor-python
python main.py cifrar "Hola mundo" mi-clave
```

Debe imprimir `250641024c0c030b0906`.

### Por qué no es seguro

Si conoces parte del mensaje, puedes obtener la clave: `mensaje ^ cifrado = clave`. Y si la clave se repite, también se repiten sus patrones. Compruébalo en el reto.

## Lee el código

1. Descifra el resultado anterior con `python main.py descifrar 250641024c0c030b0906 mi-clave`.
2. Prueba con la clave equivocada. ¿Siempre da error, o a veces devuelve basura? Lee `descifrar_texto` para saber por qué.
3. En [`main.py`](../proyectos/cifrado-xor-python/main.py), ¿qué pasa con el código de salida si hay un error? ¿Para quién es útil eso?
4. Lee `test_archivo_binario_ida_y_vuelta`. ¿Por qué usa todos los valores de 0 a 255?

## Ejercicios

1. **Básico:** escribe `a_binario(texto)`, que muestre los bits de cada byte.
2. **Básico:** escribe `romper_cesar(texto)`, que imprima las 27 posibilidades.
3. **Intermedio:** agrega a `main.py` un comando `descifrar-archivo`, que dé error si la salida ya existe.

## Reto

Cifra con XOR un texto largo en español usando una clave de 4 letras. Sin usar la clave, y sabiendo solo que mide 4 y que el texto tiene muchos espacios, recupérala. Pista: separa los bytes en cuatro grupos, según su posición, y busca el valor más frecuente de cada grupo.

## Repaso

- ¿Por qué XOR se puede usar para cifrar y para descifrar con la misma función?
- ¿Por qué `"ñ"` y `"n"` ocupan distinto en UTF-8?
- ¿Cómo se obtiene la clave si conoces un mensaje y su cifrado?

Siguiente: [Lección 11: árboles generales y persistencia](11-arboles-generales-y-persistencia.md)
