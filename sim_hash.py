# -*- coding: utf-8 -*-

# =========================================================
#
# Autor: Sergio Arroni del Riego
#
# =========================================================
import argparse
import hashlib
import bag_og_words as bag_words


class SimHash():

    def __init__(self, parse_args: argparse.Namespace) -> None:
        """Constructor

            Constructor de la clase SimHash

        Parameters:
            parse_args: argparse.Namespace

        Output: None
        """
        arg = parse_args
        self.restrictiveness: int = arg.r
        self.ngramas: int = arg.n
        self.pathFile: str = arg.file
        self.values = self.implementation()
        self.score = self.score_simhash(self.values)

    def score_simhash(self, simhash: int) -> str:
        """score_simhash

            Funcion que calcula que textos son similares medainte su simhash

        Parameters: simhash: int

        Output: str
        """

        rev_dict = {}

        {rev_dict.setdefault(value, set()).add(key)
         for key, value in simhash.items()}

        val = {k: v for k, v in rev_dict.items() if len(v) > 1}.values()
        show = ""

        for x in val:
            show += list(x)[0]
            show += "\t"
            show += list(x)[1]
            show += "\n"
        show += "Ngramas: " + str(self.ngramas)
        show += "\nRestrictiveness: " + str(self.restrictiveness)
        return show

    def implementation(self) -> dict:
        """implementation

            Funcion que carga los datos, los tokeniza y los procesa con el algoritmo SimHash,
            devolviendo un diccionario con los resultados 

        Parameters:

        Output: dict
        """
        print("SimHash")

        text = self.load_data()

        return {k: self.SimHashMethod(
            bag_words.BagOfWords(text=v, ngramas=self.ngramas)) for k, v in text.items()}

    def load_data(self) -> dict:
        """load_data

            Funcion que carga los datos de un fichero

        Parameters:

        Output: dict
        """
        train = open(self.pathFile, "r")
        train_list = [line.rstrip('\n') for line in train]
        return {t.split("\t")[0]: t.split("\t")[1] for t in train_list}

    def SimHashMethod(self, item: bag_words.BagOfWords) -> int:
        """SimHashMethod

            Funcion que implementa el algoritmo SimHash

        Parameters: item: BagOfWords

        Output: int
        """
        q = []

        [q.append(int(hashlib.sha256(
            i.encode('utf-8')).hexdigest(), 16)) for i in item.values]

        simhash = 0
        q.sort()

        for i in range(self.restrictiveness):
            simhash ^= q.pop(0)

        return simhash

    def __str__(self):
        """__str__

            Devuelve un string con la representacion del objeto

        Parameters:

        Output: str
        """
        return str(self.values)
