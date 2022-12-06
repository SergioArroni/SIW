import json
import math
import operator
import bag_og_words as bag_w
import argparse


class Index:

    def __init__(self, args: argparse.Namespace) -> None:
        '''__init__
            Funcion que inicializa la clase Index

        Parameters:
            args: argparse.Namespace
        Output:
            None
        '''
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
        self.bm25 = args.bm25
    '''
    def __init__(self, args: list) -> None:
        __init__
            Funcion que inicializa la clase Index

        Parameters:
            args: argparse.Namespace
        Output:
            None
        
        self.filename = args[0]
        self.query = args[1]
        self.index = {}
        self.index_total = {}
        self.id_bag = {}
        self.train_list = {}
        self.n_total = 0
        self.path_indice = args[2]
        self.path_query = args[3]
        self.path_docs = "./docs/docs"
        self.bm25 = args[4]
    '''

    def load_data(self, name: str) -> dict:
        """load_data

            Funcion que carga los datos de un fichero

        Parameters:
            name: str
        Output: 
            dict
        """

        texts = list(open(name, "r"))
        texts_list = [line.rstrip('\n') for line in texts]

        self.train_list = {text.split("\t")[0].rstrip(): text.split("\t")[
            1].rstrip() for text in texts_list}

        self.n_total = len(self.train_list.keys())

    def implementation_query(self) -> dict:
        """implementation_query

            Funcion que carga los datos, los tokeniza, los procesa en el las query y los guarda en un fichero json

        Parameters:
            None
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

        self.save_json(self.path_query, self.cos()) if not self.bm25 else self.save_json(
            self.path_query, self.bm())

        return "OK"

    def cos(self) -> dict:
        '''cos
            Funcion que calcula el coseno de los documentos. De una forma muy poco optima

        Parameters:
            None
        Output:
            dict
        '''
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
                        for pal in self.docs_json[k_2]:
                            for k_3, v_3 in pal.items():
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

    def bm(self) -> None:
        self.avgdl = math.fsum(
            [len(v) for _, v in self.docs_json.items()]) / self.n_total
        total = {}
        total_ordenado = {}
        list_id = {}
        k1 = 1.5
        b = 0.75

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
            mod_query_list = []
            num_dict = {}

            for k_2, v_2 in v.values.items():
                if k_2 in self.index_json:
                    value = self.index_json[k_2][0]["idf"] * \
                        (v_2 / v.value_sum())
                    mod_query += math.pow(value, 2)
                    mod_query_list.append(value)
                    num_dict[k_2] = value

        for k, v in self.id_bag.items():
            for ele in list_id[k]:
                for k_1, _ in ele.items():
                    total_par = {}
                    for k_2, v_2 in v.values.items():
                        if k_2 in self.index_json and self.index_json[k_2][0]["idf"] != 0:
                            f = (v_2 / v.value_sum())
                            num = self.index_json[k_2][0]["idf"] * f * (k1 + 1)
                            dem = f + k1 * \
                                (1 - b + b * (v.value_sum() / self.avgdl))
                            total_par[k_1] = total_par[k_1] + \
                                (num / dem) if k_1 in total_par else num / dem
                    if k in total:
                        total[k].append(total_par)
                    else:
                        total[k] = [total_par]

        return total

    def implementation_inice(self) -> str:
        """implementation

            Funcion que carga los datos, los tokeniza, los procesa en el indice y los guarda en un fichero json

        Parameters:
            None
        Output:
            str
        """
        print("Index")
        self.load_data(self.filename)

        for k, v in self.train_list.items():
            bag = bag_w.BagOfWords(text=v, enable_stop=False)
            self.id_bag[k] = bag

        self.save_json(self.path_indice, self.to_dict())

        print("----------------------------------------------")
        return "OK"

    def to_dict(self) -> dict:
        '''to_dict
            Funcion que crea el indice

        Parameters:
            None
        Output:
            dict
        '''
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
        """save_docs

            Funcion que guarda los documentos en un fichero json

        Parameters:
            docs (dict): Diccionario con los documentos
        Output:
            None
        """
        f = open(self.path_docs + ".json", "w")
        f.write(json.dumps(docs))
        f.close()

    def save_json(self, name: str, data: dict) -> None:
        """save_docs

            Funcion que guarda los documentos en un fichero json

        Parameters:
            name (str): Nombre del fichero
            data (dict): Diccionario con los datos
        Output:
            None
        """
        f = open(name + ".json", "w")
        f.write(json.dumps(data))
        f.close()

    def print_json(self, name) -> json:
        with open(name + ".json", 'r') as json_file:
            json_object = json.load(json_file)
        print(json_object)
        return json_object
