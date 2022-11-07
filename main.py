# -*- coding: utf-8 -*-

# =========================================================
#
# Autor: Sergio Arroni del Riego
#
# =========================================================

import json
import bag_og_words as bag
import argparse
import index
import argparse
import io
import gzip


def parse_args() -> argparse.Namespace:
    """Parse_args

        Funcion que permite usar la consola para añadir parametros de una forma usable.

    Output: argparse.Namespace
    """

    parser = argparse.ArgumentParser(
        description='Similitud entre hashes, textos cuasi-duplicados, para la asignatura SIW')
    parser.add_argument("--file", help="Fichero donde extraera los textos a consultar. Default: ./data/cran-1400.txt",
                        type=str, default="./data/cran-1400.txt")
    parser.add_argument("--query", help="Fichero donde extraera las query a consultar. Default: ./data/cran-queries.txt",
                        type=str, default="./data/cran-queries_plus.txt")
    parser.add_argument("--index", help="Fichero donde se guardara el index. Default: ./docs/index",
                        type=str, default="./docs/index")
    parser.add_argument("--query_json", help="Fichero donde se guardara la respuesta de la query. Default: ./docs/result",
                        type=str, default="./docs/result")
    parser.add_argument(
        "--zip", help="Si comprimir o no el indice. Default: False", type=bool, default=False)
    parser.add_argument(
        "--nb", help="Si comprimir o no el indice. Default: False", type=bool, default=False)
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
    # bag.bag_of_words()
    '''
    indice = index
    args = parse_args()

    with io.open(args.texts, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            bag_w = bag(line, enable_stop=False)
            indexer.index(bag_w)
    open_func = gzip.open if args.zip else io.open
    index_ext = ".json.gz" if args.zip else ".json"
    f = open(args.index + index_ext, "wb")
    f.write(json.dumps(indice))
    f.close()
    '''
        
    ind = index.Index(parse_args())
    #ind.implementation_inice()
    ind.implementation_query()

