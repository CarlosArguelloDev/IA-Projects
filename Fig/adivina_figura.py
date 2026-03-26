# Razonamiento Monótono con grafos.
# EQUIPO AMARILLO

import sys
import yaml
from pathlib import Path

RUTA_FIGURAS = Path(__file__).parent / "datos" / "figuras.yaml"


def cargar_grafo(ruta: Path) -> tuple[dict, dict]:
    # R004: Carga preguntas y transiciones {(origen, respuesta): destino}
    if not ruta.exists(): sys.exit(f"[Error] No existe '{ruta}'")

    with open(ruta, "r", encoding="utf-8") as f:
        datos = yaml.safe_load(f)

    trans = {(str(o), str(r)): str(d) for o, r, d in datos["transiciones"]}
    return datos["preguntas"], trans


def pedir_respuesta(opciones: list) -> str:
    # Solicita respuesta valida
    mapa = {o.lower(): o for o in opciones}
    while True:
        resp = input(f"  Opciones: {' | '.join(opciones)}\n  > ").strip().lower()
        if resp in mapa: return mapa[resp]
        print(f"  Elige entre: {opciones}")


def recorrer_grafo(preguntas: dict, tabla: dict) -> str:
    # R005: Navega el grafo usando el dict (sin if-else)
    nodo = "A"
    while True:
        ops = [r for (o, r) in tabla if o == nodo]
        if not ops: return preguntas[nodo] # Hoja encontrada

        print(f"\n  {preguntas[nodo]}")
        nodo = tabla[(nodo, pedir_respuesta(ops))]


def main() -> None:
    pregs, tabla = cargar_grafo(RUTA_FIGURAS)
    print("=" * 60 + "\n  RM_GRAPH - Figuras Geometricas\n" + "=" * 60)

    while True:
        res = recorrer_grafo(pregs, tabla)
        print(f"\n  La figura es: ** {res} **\n" + "=" * 60)
        if input("¿Otra vez? [s/n] ").lower() not in {"s", "si"}: break


if __name__ == "__main__":
    main()
