"""
Clasificador interactivo de figuras geometricas.

El programa recorre un arbol de decision guardado en JSON para
identificar una figura a partir de las respuestas del usuario.
"""

import json
from pathlib import Path


RUTA_BASE = Path(__file__).parent
ARCHIVO_ARBOL = RUTA_BASE / "figuras_amarillo.json"
RESPUESTAS_AFIRMATIVAS = {"si", "s", "sí"}


def cargar_modelo(ruta_archivo):
    """Carga el modelo de decision desde un archivo JSON."""
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def obtener_siguiente_destino(transiciones, nodo_actual, respuesta_usuario):
    """Busca el siguiente nodo segun el nodo actual y la respuesta dada."""
    for transicion in transiciones:
        if (
            transicion["desde"] == nodo_actual
            and transicion["respuesta"].lower() == respuesta_usuario.lower()
        ):
            return transicion["hacia"]
    return None


def pedir_opcion(pregunta, opciones):
    """Muestra una pregunta y valida la respuesta del usuario."""
    opciones_texto = " / ".join(opciones)
    while True:
        respuesta = input(f"\n{pregunta}\nOpciones: {opciones_texto}\n> ").strip()
        if respuesta.lower() in {opcion.lower() for opcion in opciones}:
            return respuesta
        print("Respuesta no valida. Intenta de nuevo.")


def recorrer_arbol(modelo):
    """Recorre el arbol hasta llegar a una figura final."""
    preguntas = modelo["preguntas"]
    transiciones = modelo["transiciones"]
    nodo_actual = modelo["inicio"]

    while True:
        nodo = preguntas[nodo_actual]

        if nodo["tipo"] == "resultado":
            return nodo["nombre"]

        respuesta = pedir_opcion(nodo["texto"], nodo["opciones"])
        siguiente_nodo = obtener_siguiente_destino(
            transiciones, nodo_actual, respuesta
        )

        if siguiente_nodo is None:
            print("No existe una transicion para esa respuesta.")
            continue

        nodo_actual = siguiente_nodo


def jugar():
    """Ejecuta el clasificador y permite jugar varias veces."""
    modelo = cargar_modelo(ARCHIVO_ARBOL)

    print("=" * 55)
    print("     CLASIFICADOR DE FIGURAS GEOMETRICAS")
    print("=" * 55)
    print("Piensa en una figura y responde las preguntas.")

    while True:
        figura_encontrada = recorrer_arbol(modelo)
        print(f"\nLa figura identificada es: {figura_encontrada}\n")

        respuesta = input("Deseas intentar con otra figura? (si/no): ").strip().lower()
        if respuesta not in RESPUESTAS_AFIRMATIVAS:
            print("\nPrograma finalizado.")
            break


if __name__ == "__main__":
    jugar()
