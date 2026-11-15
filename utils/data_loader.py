"""Lectura de datos de prueba desde archivos externos (CSV y JSON)."""

import csv
import json
from pathlib import Path

CARPETA_DATOS = Path(__file__).resolve().parent.parent / "data"


def leer_csv(nombre_archivo):
    """Devuelve una lista de diccionarios, uno por fila del CSV."""
    with open(CARPETA_DATOS / nombre_archivo, newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def leer_json(nombre_archivo):
    with open(CARPETA_DATOS / nombre_archivo, encoding="utf-8") as archivo:
        return json.load(archivo)
