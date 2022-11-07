# -*- coding: utf-8 -*-

# =========================================================
#
# Autor: Sergio Arroni del Riego
#
# =========================================================

from functools import reduce
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob as tb
nltk.download('omw-1.4')


class BagOfWords(object):

    def __init__(self, enable_stop: bool, text: str = None):
        """Constructor

            Constructor de la clase BagOfWords

        Parameters:
            text: str (default None)

        Output: None
        """
        self.text: str = text.rstrip()
        self.enable_stop = enable_stop

        if type(text) is str:
            self.values = self.string_to_bag_of_words(self.text)
        else:
            self.values = {}

    def string_to_bag_of_words(self, text: str) -> dict:
        """string_to_bag_of_words

            Funcion que convierte un string en un diccionario de palabras tokenizadas ( bag of words )
            con lematizacion, sin stopwords y sin signos de puntuacion y en minusculas

        Parameters:
            text: str

        Outpup: dict
        """
        bag = {}
        tokens= tb(text).words

        stop = set(stopwords.words('english')) if self.enable_stop else set()
        signos_puntuacion = ["?", "¿", "¡", "!", " ", ",", ".", ";",
                             ":", "(", ")", "[", "]", "{", "}", "-", "_", "—", "'"]

        for token in tokens:

            if token in stop and token in signos_puntuacion:
                continue

            token = token.lemmatize()

            token = token.lower()

            if token in stop:
                continue

            bag[token] = bag[token] + 1 if token in bag else 1


        return bag
    
    def value_sum(self):
        return reduce((lambda x, value: x + value), self.values.values(), 0)


    # Override
    def __str__(self) -> str:
        """__str__

            Devuelve un string con la representacion del objeto

        Parameters:

        Output: str
        """
        return str(self.values)
