"""Script para generar histogramas a partir de los ficheros de takeout de Youtube."""

import json
from datetime import datetime
import argparse
import pytz

import matplotlib.pyplot as plt


def items_per_hour(input_filename, output_filename, title):
    """
    Lee un fichero JSON con el historico de busquedas o visualizaciones de Youtube y
    crea un histograma de items por hora.

    Args:
      input_filename: La ruta al fichero de entrada en formato JSON.
      output_filename: La ruta al ficher de salida donde se almacenara el histograma.
      title: El titulo del histograma.
    """

    # Primero, abrimos el fichero de entrada y lo procesamos usando la libreria json.
    with open(input_filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Inicializamos la estructura para almacenar las horas de cada visualización.
    items = []
    for item in data:
        # El historial contiene contenido de Youtube Music, por lo que debemos filtrarlo.
        # Para ello unicamente tomaremos en cuenta entradas con header="Youtube".
        if item["header"] != "YouTube":
            continue
        # El campo time es el que contiene la fecha de cada item.
        utc_time = datetime.fromisoformat(item["time"])
        # Los datos se encuentran en UTC, por lo que hay que convertir la zona horaria
        # para facilitar su interpretación.
        cest_timezone = pytz.timezone("Europe/Madrid")
        cest_time = utc_time.astimezone(cest_timezone)
        items.append(cest_time.hour)

    # Creamos el histograma y lo almacenamos en la ruta indicada.
    plt.figure(figsize=(10, 6))
    plt.hist(items, bins=24, range=(0, 24), color="skyblue", edgecolor="black")
    plt.xlabel("Hora del dia")
    plt.ylabel("Numero de ocurrencias")
    plt.xticks(range(24))
    plt.grid(axis="y", alpha=0.75)
    plt.title(title)
    plt.savefig(output_filename)


def main():
    """Genera un histograma a partir de los ficheros de takeout de Youtube."""
    parser = argparse.ArgumentParser(
        description="Generador de histograma de visualizaciones de Youtube."
    )
    parser.add_argument(
        "--input",
        type=str,
        help="El fichero del historial.",
        required=True,
    )
    parser.add_argument(
        "--output",
        type=str,
        help="El fichero del histograma.",
        required=False,
        default="histograma.png",
    )
    parser.add_argument(
        "--title",
        type=str,
        help="El titulo del historgrama.",
        required=False,
        default="Ocurrencias por hora",
    )

    args = parser.parse_args()

    items_per_hour(args.input, args.output, args.title)


if __name__ == "__main__":
    main()
