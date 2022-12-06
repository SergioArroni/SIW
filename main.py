# -*- coding: utf-8 -*-

# =========================================================
#
# Autor: Sergio Arroni del Riego
#
# =========================================================

import argparse
import index


def parse_args() -> argparse.Namespace:
    """Parse_args

        Funcion que permite usar la consola para añadir parametros de una forma usable.

    Output: argparse.Namespace
    """

    parser = argparse.ArgumentParser(
        description='Index, para la asignatura SIW')
    parser.add_argument("--file", help="Fichero donde extraera los textos a consultar. Default: ./data/ejemplo.txt",
                        type=str, default="./data/ejemplo.txt")
    parser.add_argument("--query", help="Fichero donde extraera las query a consultar. Default: ./data/ejemplo_q.txt",
                        type=str, default="./data/ejemplo_q.txt")
    parser.add_argument("--index", help="Fichero donde se guardara el index. Default: ./docs/index",
                        type=str, default="./docs/index")
    parser.add_argument("--query_json", help="Fichero donde se guardara la respuesta de la query. Default: ./docs/result",
                        type=str, default="./docs/result")
    parser.add_argument(
        "--bm25", help="Si se quiere usar bm25. Default: False", action="store_true")
    args = parser.parse_args()
    return args


def presentacion():
    """Presentacion

    Funcion que muestra una presentacion muy bonita

    """

    print("Trabajo de Indice y de consulta de dicho indice. Para la asignatura SIW :)\nAñade el argumento \"-h\" a la hora de ejecutar para obtener la ayuda del Script")
    print("Autor: Sergio Arroni del Riego - UO276341\n\n\n")


if __name__ == "__main__":
    """__main__

    Primero imprime la presentacion del trabajo y luego el main con la logica del mismo

    """
    presentacion()

    ind = index.Index(parse_args())
    ind.implementation_inice()

    ind = index.Index(parse_args())
    ind.implementation_query()
