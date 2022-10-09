# -*- coding: utf-8 -*-

# =========================================================
#
# Autor: Sergio Arroni del Riego
#
# =========================================================

from difflib import restore
from io import TextIOWrapper
import math
import nltk
import argparse
from nltk.corpus import stopwords
from textblob import TextBlob as tb
nltk.download('omw-1.4')


def main(args: argparse.Namespace):
    """main

        Contiene toda la logica del Sistema

        Params:
            args, todos los argumentos dados por consola
    """
    bag_query = process_file(args)

    bag_text = process_file(args, False)

    f = open("./docs/resultados.txt", "a")

    for q in bag_query:
        process_metodo(f, q, bag_query, bag_text, cos, "coseno", args)
        process_metodo(f, q, bag_query, bag_text, jac, "jaccard", args)

    f.close()

def process_metodo(f: TextIOWrapper, q: str, bag_query, bag_text, metodo, metodo_name, args) -> None:
    """process_metodo

        Funcion que procesa los documentos y haya la similitud dependiendo del metodo dado

        Params:
            f, documento donde guardar los resultados
            q, identificador de la query
            bag_query, dict con las querys tokenizadas
            bag_text, dict con los textos tokenizados
            metodo, funcion que haya el coeficiente de similitud
            metodo_name, nombre del metodo a usar para hayar el coeficiente de similitud
            args, todos los argumentos dados por consola
    """
    best_text, best_text_result = find_best_text(
        bag_query[q], bag_text, metodo)

    print_sim_q_text(f, q, best_text, best_text_result, metodo_name, args)


def process_file(args, query=True):
    """process_file

        Funcion que procesa los documentos pasados por parametro y los transforma en un dict para poder tokenizarlos

        Params:
            args, todos los argumentos dados por consola
            query, bool que elige entre si se esta procesando las querys o el texto, por defecto True
    """
    texts = list(
        open(args.qfile, "r")) if query else list(
        open(args.file, "r"))

    texts_list = [line.rstrip('\n') for line in texts]

    final = {text.split("\t")[0]: text.split("\t")[1] for text in texts_list}

    return token_dict(args, final)


def token_dict(args, dict_all):
    """token_dict

        Funcion que tokeniza un dict

        Params:
            args, todos los argumentos dados por consola
            dict_all, dict que contiene el docuemnto separado entre id y texto
    """
    return {k: string_to_bag_of_words(
        tb(v), args.l, args.s, args.stop) for k, v in dict_all.items()}


def find_best_text(q, bag_text, metodo):
    """find_best_text

        Funcion que mediante un metodo de calculo similitud encuentra el mejor texto dado una query

        Params:
            q, dict de una query tokenizada
            bag_text, dict de una texto tokenizado
            metodo, funcion que realiza el calculo del coeficiente de similitud
    """
    text_correct = {k: metodo(q, v) for k, v in bag_text.items()}

    return max(text_correct, key=text_correct.get), max(text_correct.values())


def print_sim_q_text(f, q, text, result, metodo, args):
    """print_sim_q_text

        Funcion que imprime en un fichero los resultados del mejor coeficiente de similitud entre una query y un texto

        Params:
            f, documento donde guardar los resultados
            q, identificador de la query
            text, identificador del texto
            result, mejor coeficiente resultado de calcular la similitud entre la query y el texto dados
            metodo, nombre del metodo a usar para hayar el coeficiente de similitud
            args, todos los argumentos dados por consola
    """
    f.write(
        f"\n-------------------------------------------------------------- Para la query q: {q} -------------------------------------------------------\n")
    f.write(f"El mejor texto es el {text} con un resultado de: {result}\nPara el metodo: {metodo}\nCon un valor de lematizacion de: {args.l}, de stematizacion de: {args.s} y un StopWords de NLTK de: {args.stop}\n")


def string_to_bag_of_words(text, lema=False, stema=False, stop=False):
    """string_to_bag_of_words

        Funcion que tokeniza un texto dado

        Params:
            text, dict con todos los textos (v) y sus ids (k)
            lema, bool que decide si se aplica lematiacion o no
            stema, bool que decide si se aplica stematizacion o no
            stop, bool que decide si se aplica stop words o no
    """

    tokens = text.words
    bag = {}

    stops = set(stopwords.words('english')) if stop else {}

    for token in tokens:
        if token in stops:
            continue

        token = token.lemmatize() if lema else token

        token = token.stem() if stema else token

        bag[token] = bag[token] + 1 if token in bag else 1

    return bag


def cos(x, y):
    """cos

        Funcion que haya el coeficiente de similituz de coseno entre la query y el texto

        Params:
            x, dict de la query tokenizada
            y, dict de la texto tokenizado
    """
    return inter(x, y) / math.sqrt(mul(x, y))


def jac(x, y):
    """jac

        Funcion que haya el coeficiente de similituz de jaccard entre la query y el texto

        Params:
            x, dict de la query tokenizada
            y, dict de la texto tokenizado
    """
    return inter(x, y) / union(x, y)


def inter(x, y):
    """inter

        Funcion que realiza la interseccion de los modulos de la query y el texto

        Params:
            x, dict de la query tokenizada
            y, dict de la texto tokenizado
    """
    return sum(dict(x.items() & y.items()).values())


def union(x, y):
    """union

        Funcion que realiza la union de los modulos de la query y el texto

        Params:
            x, dict de la query tokenizada
            y, dict de la texto tokenizado
    """
    return sum(dict(x.items() | y.items()).values())


def mul(x, y):
    """mul

        Funcion que realiza la multiplicacion de los modulos de la query y el texto

        Params:
            x, dict de la query tokenizada
            y, dict de la texto tokenizado
    """
    return sum(x.values()) * sum(y.values())


def presentacion():
    """Presentacion

    Funcion que muestra una presentacion en ASCII muy bonita

    """

    print("Trabajo de similitud entre textos para la asignatura SIW :)\nAñade el argumento \"-h\" a la hora de ejecutar para optener la ayuda del Script")
    print("Autor: Sergio Arroni del Riego - UO276341\n\n\n")


def parse_args() -> argparse.Namespace:
    """Parse_args

    Funcion que permite usar la consola para añadir parametros de una forma usable.

    """

    parser = argparse.ArgumentParser(
        description='Similitud entre textos para la asignatura SIW')
    parser.add_argument("--file", help="Fichero donde extraera los textos a consultar. Default: ./data/cran-1400.txt",
                        type=str, default="./data/cran-1400.txt")
    parser.add_argument("--qfile", help="Fichero donde extraera las consultas. Default: ./data/cran-queries.txt",
                        type=str, default="./data/cran-queries.txt")
    parser.add_argument(
        "-l", help="Si se quiere lematizar los textos a consultar. Default: false", action="store_true")
    parser.add_argument(
        "-s", help="Si se quiere stematizar los textos a consultar. Default: false", action="store_true")
    parser.add_argument(
        "-stop", help="Si no se quiere usar un fichero de stop words. Default: false", action="store_true")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    """__main__

    Primero imprime la presentacion del trabajo y luego el main con la logica del mismo

    """

    presentacion()
    main(parse_args())
