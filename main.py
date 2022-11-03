# -*- coding: utf-8 -*-

# =========================================================
#
# Autor: Sergio Arroni del Riego
#
# =========================================================

import argparse
import page_rank


def parse_args() -> argparse.Namespace:
    """Parse_args

        Función que permite usar la consola para añadir parámetros de una forma usable.

    Output: argparse.Namespace
    """

    parser = argparse.ArgumentParser(
        description='Similitud entre hashes, textos cuasi-duplicados, para la asignatura SIW')
    parser.add_argument("--file", help="Fichero donde extraerá el grafo a calcular con PageRank. Default: ./data/graph01.txt",
                        type=str, default="./data/graph01.txt")
    parser.add_argument(
        "--iter", help="El numero de iteraciones que ejecutara PageRank, a no ser que pare antes por el limite. Default: 100", type=int, default=100)
    parser.add_argument(
        "--init", help="El numero con el que inicializar los nodos. Default: 1", type=float, default=1.0)
    parser.add_argument(
        "-d", help="El damping para el salto de PageRank. Default: 0.85", type=float, default=0.85)
    parser.add_argument(
        "-l", help="El limite en el que deja de calcular PageRank. Default: 1.0e-8", type=float, default=1.0e-8)
    args = parser.parse_args()
    return args


def presentacion():
    """Presentación

    Función que muestra una presentación muy bonita

    """

    print("Trabajo de PageRank. Para la asignatura SIW :)\nAñade el argumento \"-h\" a la hora de ejecutar para obtener la ayuda del Script")
    print("Autor: Sergio Arroni del Riego - UO276341\n\n\n")


if __name__ == "__main__":
    """__main__

    Primero imprime la presentación del trabajo y luego el main con la lógica del mismo

    """
    presentacion()

    pg = page_rank.PageRank(parse_args())

    f = open("./docs/page_rank.txt", "a")
    f.write(str(pg))
    f.close()
