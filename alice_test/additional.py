import json
from functools import reduce
import operator
from testalice.settings import BASE_DIR
from os.path import join as path_join

json_path = path_join(BASE_DIR, "alice_test", "data.json")
en_to_rus = {
    "genealogy": "генеалогия",
    "inheritance": "наследование",
    "traits": "черты",
    "maultifactorial": "мультифакторы",
    "genetic": "генетика",
    "haplotypes": "гаплотипы",
    "genotypes": "генотипы",
}


def get_by_path(root, items):
    """Access a nested object in root by item sequence."""
    return reduce(operator.getitem, items, root)


def set_by_path(root, items, value):
    """Set a value in a nested object in root by item sequence."""
    get_by_path(root, items[:-1])[items[-1]] = value


def get_keys(node):
    if type(node) is dict:
        return ", ".join(node.keys())
    else:
        return node


def dict_to_rus(mydict):
    for key, value in mydict.items():
        if key in en_to_rus:
            new_key = en_to_rus[key]
            mydict[new_key] = mydict.pop(key)
        if isinstance(value, dict):
            dict_to_rus(value)


with open(json_path) as f:
    json_data = json.load(f)
    dict_to_rus(json_data)


