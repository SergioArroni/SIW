# -*- coding: utf-8 -*-

# =========================================================
#
# Autor: Sergio Arroni del Riego
#
# =========================================================

import nltk
from nltk.corpus import stopwords
from textblob import TextBlob as tb
nltk.download('omw-1.4')


class BagOfWords(object):

    def __init__(self, text: str = None, ngramas: int = 1):
        """Constructor

            Constructor de la clase BagOfWords
            
        Parameters:
            text: str (default None)
            ngramas: int (default 1)
            
        Output: None
        """
        self.text: str = text
        self.ngramas: int = ngramas

        if type(text) is str:
            self.values = self.string_to_bag_of_words(text)
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
        tokens = tb(text).ngrams(n=self.ngramas)
        # tokens= tb(text).words

        stop = set(stopwords.words('english'))
        signos_puntuacion = ["?", "¿", "¡", "!", " ", ",", ".", ";",
                             ":", "(", ")", "[", "]", "{", "}", "-", "_", "—", "'"]

        for token in tokens:
            while len(token) > 0:
                token_real = tb(token.pop()).words[0]
                if token_real in stop and token_real in signos_puntuacion:
                    continue

                token_real = token_real.lemmatize()

                token_real = token_real.lower()

                if token_real in stop:
                    continue

                bag[token_real] = bag[token_real] + \
                    1 if token_real in bag else 1
            tokens = tokens[1:]

        return bag

    # Override
    def __str__(self) -> str:
        """__str__

            Devuelve un string con la representacion del objeto

        Parameters:

        Output: str
        """
        return str(self.values)
