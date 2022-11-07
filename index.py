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
        self.query = args.query
        self.index = {}
        self.index_total = []
        self.id_bag = {}
        self.train_list = {}
        self.n_total = 0
        self.path_indice = args.index
        self.path_query = args.query_json

    def load_data(self, name:str) -> dict:
        """load_data

            Funcion que carga los datos de un fichero

        Parameters:
            None
        Output: 
            dict
        """

        texts = list(open(name, "r"))
        texts_list = [line.rstrip('\n') for line in texts]

        self.train_list = {text.split("\t")[0].rstrip(): text.split("\t")[
            1].rstrip() for text in texts_list}

        self.n_total = len(self.train_list.keys())

    def implementation_query(self) -> dict:
        """implementation

            Funcion que carga los datos, los tokeniza y los procesa con el algoritmo SimHash,
            devolviendo un diccionario con los resultados 

        Parameters:

        Output: dict
        """
        print("Query")
        self.load_data(self.query)


        self.list_Id = []

        for k, v in self.train_list.items():
            bag = bag_w.BagOfWords(text=v, enable_stop=False)
            self.id_bag[k] = bag
            self.list_Id.append(k)

        self.save_json(self.path_query)
        
        print("----------------------------------------------")
        
        # Tu, me tengo que ir , para las querys el TF es el numero de documentos en los que sale y el IDF es 1 partido del total de palabras
        
        self.index_json = json.load(open(self.path_indice + ".json", "r"))
        
        self.query_json = json.load(open(self.path_query + ".json", "r"))
        for ele in self.query_json:
            for ele2 in self.index_json:
                print (ele2)


    def cos(self, num, den1, den2):
        return num / (math.sqrt(den1) * math.sqrt(den2))

    def implementation_inice(self) -> dict:
        """implementation

            Funcion que carga los datos, los tokeniza y los procesa con el algoritmo SimHash,
            devolviendo un diccionario con los resultados 

        Parameters:

        Output: dict
        """
        print("Index")
        self.load_data(self.filename)

        for k, v in self.train_list.items():
            bag = bag_w.BagOfWords(text=v, enable_stop=False)
            self.id_bag[k] = bag

        self.save_json(self.path_indice)

        print("----------------------------------------------")

    def to_dict(self):
        docs_aux = {}
        TF = {}

        for k, v in self.id_bag.items():
            for k_2, v_2 in v.values.items():
                if k_2 in self.index:
                    self.index[k_2] += 1
                else:
                    self.index[k_2] = 1

                TF[k_2] = v_2 / v.value_sum()
            docs_aux[k] = TF

        for k, v in self.index.items():
            self.index[k] = math.fabs(math.log(v / self.n_total))

        for k, v in self.index.items():
            if v == 0:
                self.index_total.append(({k: v}, []))
                continue
            for k_2, v_2 in docs_aux.items():
                if k in v_2:
                    self.index_total.append(
                        ({k: v}, {k_2: [v_2[k], v_2[k] * v]}))

        return self.index_total

    def save_json(self, name: str):
        f = open(name + ".json", "w")
        f.write(json.dumps(self.to_dict()))
        f.close()

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

    def load_data_2(self) -> dict:
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
        self.n_total = len(self.train_list.keys())

    '''
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
    '''