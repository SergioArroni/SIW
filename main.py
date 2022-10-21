# -*- coding: utf-8 -*-

# =========================================================
#
# Autor: Sergio Arroni del Riego
#
# =========================================================

import bag_og_words as bag
import sim_hash as simhash
import argparse
import index


def parse_args() -> argparse.Namespace:
    """Parse_args

        Funcion que permite usar la consola para añadir parametros de una forma usable.

    Output: argparse.Namespace
    """

    parser = argparse.ArgumentParser(
        description='Similitud entre hashes, textos cuasi-duplicados, para la asignatura SIW')
    parser.add_argument("--file", help="Fichero donde extraera los textos a consultar. Default: ./data/doc-text",
                        type=str, default="./data/doc-text")
    parser.add_argument(
        "-r", help="El numero de restrictiveness que se quiera aplicar. Default: 10", type=int, default=10)
    parser.add_argument(
        "-n", help="El numero de ngramas que se quiera aplicar. Default: 1", type=int, default=1)
    args = parser.parse_args()
    return args


def presentacion():
    """Presentacion

    Funcion que muestra una presentacion muy bonita

    """

    print("Trabajo de similitud entre textos, para detetectar cuasi-duplicados. Para la asignatura SIW :)\nAñade el argumento \"-h\" a la hora de ejecutar para optener la ayuda del Script")
    print("Autor: Sergio Arroni del Riego - UO276341\n\n\n")


if __name__ == "__main__":
    """__main__

    Primero imprime la presentacion del trabajo y luego el main con la logica del mismo

    """
    presentacion()
    # bag.bag_of_words()
    ind = index.Index(parse_args())
    ind.implementation()
    ind.IDFMethod()
    
