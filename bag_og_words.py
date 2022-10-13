# -*- coding: utf-8 -*-

# =========================================================
#
# Autor: Sergio Arroni del Riego
#
# =========================================================

from difflib import restore
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob as tb
nltk.download('omw-1.4')


class BagOfWords(object):

    def __init__(self, text=None, values=None, ngramas=0):
        """Constructor

        Si recibe un string mediante el argumento text lo convierte a un
        diccionario. Si recibe un diccionario simplemente lo copia para su
        uso interno.
        """
        self.text = text
        if values is not None:
            self.values = values
        elif type(text) is dict:
            self.values = text
        elif type(text) is str:
            self.values = self.string_to_bag_of_words(text, {})
        elif type(text) is list:
            bag = {}
            for i in text:
                bag = self.string_to_bag_of_words(text, bag)
            self.values = bag
        else:
            self.values = {}

    def __str__(self):
        """Devuelve un string con la representacion del objeto

        El objeto BagOfWords(“A b a”) está representado por el string
        "{‘a’: 2, ‘b’: 1}"
        """
        return str(self.values)

    def string_to_bag_of_words(self, text, bag):
        """Convierte un string a bag of words"""

        tokens = tb(text).words

        stop = set(stopwords.words('english'))

        for token in tokens:
            if token in stop:
                continue

            token = token.lemmatize()

            token = token.lower()

            bag[token] = bag[token] + 1 if token in bag else 1

        return bag
