import bag_og_words as bag_words


class SimHash():

    def __init__(self) -> None:
        self.values = self.implementation()

    def implementation(self):
        print("SimHash")

        text = self.load_data()

        restrictiveness = 3

        return {k: self.SimHashMethod(
            bag_words.BagOfWords(text=v), restrictiveness) for k, v in text.items()}

    def load_data(self):
        train = open("./data/articles_1000.train", "r")
        train_list = [line.rstrip('\n') for line in train]
        return {t.split("\t")[0]: t.split("\t")[1] for t in train_list}

    # Función hash

    def Hash_func(self, value):
        key = 0
        for i in range(0, len(value)):
            key += ord(value[i])
        return key % 127

    def SimHashMethod(self, item, restrictiveness):

        queue = []
        for x in item.values:
            queue.append(self.Hash_func(x))
        simhash = 0
        for x in [0, restrictiveness]:
            min_index = queue.index(min(queue))
            simhash ^= queue.pop(min_index)
        return simhash

    def __str__(self):
        """Devuelve un string con la representacion del objeto

        El objeto BagOfWords(“A b a”) está representado por el string
        "{‘a’: 2, ‘b’: 1}"
        """
        return str(self.values)
