import argparse
from flask import Flask
import index

app = Flask(__name__)


def parse_args() -> argparse.Namespace:
    """Parse_args

        Funcion que permite usar la consola para añadir parametros de una forma usable.

    Output: argparse.Namespace
    """

    parser = argparse.ArgumentParser(
        description='Index, para la asignatura SIW')
    parser.add_argument("--file", help="Fichero donde extraera los textos a consultar. Default: ./data/cran-1400.txt",
                        type=str, default="./data/cran-1400_plus.txt")
    parser.add_argument("--query", help="Fichero donde extraera las query a consultar. Default: ./data/cran-queries.txt",
                        type=str, default="./data/cran-queries_plus.txt")
    parser.add_argument("--index", help="Fichero donde se guardara el index. Default: ./docs/index",
                        type=str, default="./docs/index")
    parser.add_argument("--query_json", help="Fichero donde se guardara la respuesta de la query. Default: ./docs/result",
                        type=str, default="./docs/result")
    args = parser.parse_args()
    return args


param = ["./data/cran-1400_plus.txt",
         "./data/cran-queries_plus.txt", "./docs/index", "./docs/result", True]


@app.route('/')
def main():
    return "Autor: Sergio Arroni del Riego - UO276341\n\n\n"


@app.route('/index')
def load_index():
    ind = index.Index(param)
    return ind.implementation_inice()


@app.route('/query')
def load_query():
    ind = index.Index(param)
    ind.implementation_query()
    return ind.print_json(param[3])
