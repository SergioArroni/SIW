import json
import math
import operator
import bag_og_words as bag_w
import argparse


class Index:

    def __init__(self, args: argparse.Namespace) -> None:
        self.filename = args.file
        self.query = args.query
        self.index = {}
        self.index_total = {}
        self.id_bag = {}
        self.train_list = {}
        self.n_total = 0
        self.path_indice = args.index
        self.path_query = args.query_json
        self.path_docs = "./docs/docs"

    def load_data(self, name: str) -> dict:
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

        for k, v in self.train_list.items():
            bag = bag_w.BagOfWords(text=v, enable_stop=False)
            self.id_bag[k] = bag

        print("----------------------------------------------")

        self.index_json = json.load(open(self.path_indice + ".json", "r"))

        self.docs_json = json.load(open(self.path_docs + ".json", "r"))

        self.save_json(self.path_query, self.cos())

    def cos(self):
        total_result = {}
        list_id = {}

        for k, v in self.id_bag.items():
            for k_2, _ in v.values.items():
                if k_2 in self.index_json and self.index_json[k_2][0]["idf"] != 0:
                    if k in list_id:
                        for ele in self.index_json[k_2][1]["textos"]:
                            if not (ele in list_id[k]):
                                list_id[k].append(ele)
                    else:
                        list_id[k] = self.index_json[k_2][1]["textos"]

        for k, v in self.id_bag.items():
            mod_query = 0
            mod_doc = 0
            mod_doc_pow = 0
            mod_query_list = []
            num_dict = {}
            num_dict_aux = {}
            mod_doc_dict_pow = {}
            result = {}

            for k_2, v_2 in v.values.items():
                if k_2 in self.index_json:
                    value = self.index_json[k_2][0]["idf"] * \
                        (v_2 / v.value_sum())
                    mod_query += math.pow(value, 2)
                    mod_query_list.append(value)
                    num_dict[k_2] = value

            for ele in list_id[k]:
                for k_2, _ in ele.items():
                    mod_doc_pow = 0
                    mod_doc = 0
                    if k_2 in self.docs_json:
                        for k_3, v_3 in self.docs_json[k_2].items():
                            mod_doc_pow += math.pow(v_3, 2)
                            if k_3 in v.values.keys():
                                mod_doc += v_3
                                if k_2 in num_dict_aux:
                                    num_dict_aux[k_2] += num_dict[k_3] * mod_doc
                                else:
                                    num_dict_aux[k_2] = num_dict[k_3] * mod_doc
                            mod_doc_dict_pow[k_2] = mod_doc_pow

                    result[k_2] = num_dict_aux[k_2] / \
                        (math.sqrt(mod_doc_dict_pow[k_2])
                         * math.sqrt(mod_query))

            total_result[k] = sorted(
                result.items(), key=operator.itemgetter(1), reverse=True)

        return total_result

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

        self.save_json(self.path_indice, self.to_dict())

        print("----------------------------------------------")

    def to_dict(self):
        docs_aux = {}
        TF = {}
        docs_aux_to_json = {}

        for k, v in self.id_bag.items():
            TF = {}
            for k_2, v_2 in v.values.items():
                if k_2 in self.index:
                    self.index[k_2] += 1
                else:
                    self.index[k_2] = 1

                TF[k_2] = v_2 / v.value_sum()
            docs_aux[k] = TF

        for k, v in self.index.items():
            self.index[k] = math.fabs(math.log10(self.n_total / v))

        for k, v in self.index.items():
            if v == 0:
                self.index_total[k] = [{"idf": v}]
                continue
            for k_2, v_2 in docs_aux.items():
                if k in v_2:
                    if k in self.index_total and self.index_total[k] != None:
                        self.index_total[k][1]["textos"].append(
                            {k_2: [v_2[k], v_2[k] * v, math.pow(v_2[k] * v, 2)]})
                    else:
                        self.index_total[k] = [{"idf": v}, {
                            "textos": [{k_2: [v_2[k], v_2[k] * v, math.pow(v_2[k] * v, 2)]}]}]

        for k, v in docs_aux.items():
            for k_2, v_2 in self.index.items():
                if v_2 == 0:
                    continue
                if k_2 in v:
                    if k in docs_aux_to_json:
                        docs_aux_to_json[k].append(
                            {k_2: v[k_2] * v_2})
                    else:
                        docs_aux_to_json[k] = [{k_2: v[k_2] * v_2}]
        self.save_docs(docs_aux_to_json)
        return self.index_total

    def save_docs(self, docs: dict) -> None:
        """implementation

            Funcion que carga los datos, los tokeniza y los procesa con el algoritmo SimHash,
            devolviendo un diccionario con los resultados 

        Parameters:

        Output: dict
        """
        f = open(self.path_docs + ".json", "w")
        f.write(json.dumps(docs))
        f.close()

    def save_json(self, name: str, data: dict):
        f = open(name + ".json", "w")
        f.write(json.dumps(data))
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
