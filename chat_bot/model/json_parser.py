import json
from functools import reduce
import operator
from YandexAlice.settings import BASE_DIR
from os.path import join as path_join


json_path = path_join(BASE_DIR, "chat_bot", "data.json")
en_to_rus = {
    "genealogy": "генеалогия",
    "inheritance": "наследование",
    "traits": "черты",
    "multifactorial": "мультифакторы",
    "genetic": "генетика",
    "haplotypes": "гаплотипы",
    "genotypes": "генотипы",
    "y_chr_haplogroup": "материнская линия",
    "mt_dna_haplogroup": "отцовская линия",
    "ancestry_decomposition": "происхождение",
    "neanderthal": "доля неандертальца"
}


class JsonTree:
    def __init__(self, filename):
        self.filename = filename
        with open(self.filename) as stream:
            self.json_dict = json.load(stream)
            self.translate_dict(self.json_dict)
        self._json_search = JsonSearch(self)

    def get_by_path(self, items):
        """Access a nested object in root by item sequence."""
        return reduce(operator.getitem, items, self.json_dict)

    def set_by_path(self, items, value):
        """Set a value in a nested object in root by item sequence."""
        self.get_by_path(items[:-1])[items[-1]] = value

    def translate_dict(self, mydict):
        for key, value in mydict.items():
            if key in en_to_rus:
                new_key = en_to_rus[key]
                mydict[new_key] = mydict.pop(key)
            if isinstance(value, dict):
                self.translate_dict(value)

    def find_node(self, node_name):
        return self._json_search._search_node(self.json_dict, node_name, [])


class JsonSearch:
    def __init__(self, json_tree):
        self.json_tree = json_tree
        self.json_dict = self.json_tree.json_dict

    def _get_leaves_from_list(self, mylist, node_name, path):
        for i, el in enumerate(mylist):
            temp_path = path.copy()
            temp_path.append(i)
            if isinstance(el, dict):
                yield from self._search_node(el, node_name, temp_path)
            elif isinstance(el, list):
                yield from self._get_leaves_from_list(el, node_name, temp_path)

    def _search_node(self, mydict, node_name, path):
        for k, v in mydict.items():
            temp_path = path.copy()
            temp_path.append(k)
            if k == node_name:
                yield temp_path
            if isinstance(v, dict):
                yield from self._search_node(v, node_name, temp_path)
            elif isinstance(v, list):
                yield from self._get_leaves_from_list(v, node_name, temp_path)
