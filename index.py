import json
import math
import pickle
from re import I
from typing import Counter
import bag_og_words as bag_w
import argparse


class Index:

    def __init__(self, args: argparse.Namespace) -> None:
        self.filename = args.file
        self.index = {}
        self.load_data()
        self.n_total = 0

    def load_data(self) -> dict:

        """load_data

            Funcion que carga los datos de un fichero

        Parameters:
            None
        Output: 
            dict
        """
        text_aux = ""
        self.train_list = {}
        train = open(self.filename, "r")
        for i in train:
            i = i.replace('\n', "")
            i = i.replace('\t', "")
            if i.isdigit():
                num = i
            elif "/" in i:
                self.train_list[num] = text_aux
            else:
                text_aux += " " + i
        f = open("train_list.txt", "w")
        f.write(json.dumps(self.train_list))
        f.close()
        self.n_total = len(self.train_list.keys())

    def implementation(self) -> dict:
        """implementation

            Funcion que carga los datos, los tokeniza y los procesa con el algoritmo SimHash,
            devolviendo un diccionario con los resultados 

        Parameters:

        Output: dict
        """
        print("Index")

        # Aqui tengo {pal : idf} : {ID_Doc : tf}
        self.id_pal_cont = {self.TFMethod(
            bag_w.BagOfWords(text=v)): {k: self.pal_tf} for k, v in self.train_list.items()}

        print("a")

    def count(self, pal) -> dict:
        cnt = Counter()
        for _, v in self.train_list.items():
            if pal in v:
                cnt[pal] += 1

        return cnt

    def IDFMethod(self) -> int:

        pal_key = self.id_pal_cont.keys()

        pal_value = self.id_pal_cont.values()

        pal_idf = {k: math.log(self.n_total / self.count(v))
                   for k, v in pal_key.items()}
        
        self.index = {pal_idf : pal_value}


    def TFMethod(self, item: bag_w.BagOfWords) -> int:
        # Aqui tengo palabra : TF
        denominador = sum(item.values())
        self.pal_tf = [v/denominador for _, v in item.items()]
        return {k: 0 for k, _ in item.items()}

    def load(self):
        try:
            self.index = pickle.load(open(self.filename, 'rb'))
        except:
            pass

    def save(self):
        pickle.dump(self.index, open(self.filename, 'wb'))

    def add(self, key, value):
        if key in self.index:
            self.index[key].append(value)
        else:
            self.index[key] = [value]

    def get(self, key):
        if key in self.index:
            return self.index[key]
        else:
            return []

    def __str__(self):
        return str(self.index)

    def __repr__(self):
        return str(self.index)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.add(key, value)

    def __contains__(self, key):
        return key in self.index

    def __len__(self):
        return len(self.index)

    def __iter__(self):
        return iter(self.index)
