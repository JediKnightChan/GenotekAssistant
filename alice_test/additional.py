import json
from functools import reduce
import operator
from testalice.settings import BASE_DIR
from os.path import join as path_join
from nested_lookup import nested_lookup

json_path = path_join(BASE_DIR, "alice_test", "data.json")
en_to_rus = {
    "genealogy": "генеалогия",
    "inheritance": "наследование",
    "traits": "черты",
    "multifactorial": "мультифакторы",
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


def get_leaves_from_list(mylist, node_name, path):
    for i, el in enumerate(mylist):
        temp_path = path.copy()
        temp_path.append(i)
        if isinstance(el, dict):
            yield from _search_node(el, node_name, temp_path)
        elif isinstance(el, list):
            yield from get_leaves_from_list(el, node_name, temp_path)


def _search_node(mydict, node_name, path):
    for k, v in mydict.items():
        temp_path = path.copy()
        temp_path.append(k)
        if k == node_name:
            yield temp_path
        if isinstance(v, dict):
            yield from _search_node(v, node_name, temp_path)
        elif isinstance(v, list):
            yield from get_leaves_from_list(v, node_name, temp_path)


def find_node(mydict, node_name):
    return _search_node(mydict, node_name, [])


def get_options(paths, i):
    options = []
    for path in paths:
        if i < len(path):
            el = path[i]
            if el not in options:
                options.append(el)
    return options


def filter_paths(paths, i, selected_value):
    filtered = []
    for path in paths:
        if i < len(path):
            el = path[i]
            if el == selected_value:
                filtered.append(path)
    return filtered


def choose_option(user_find_resulsts, user_id):
    paths, i, user_options = user_find_resulsts[user_id]
    print(paths, i)
    options = get_options(paths, i)
    if len(options) == 0:
        return True, paths[0]
    elif len(options) == 1:
        key = options[0]
        new_paths = filter_paths(paths, i, key)
        user_find_resulsts[user_id] = new_paths, i+1, {}
        return choose_option(user_find_resulsts, user_id)
    else:
        if len(options) == 2:
            rel_paths_for_options = list(map(lambda path: "/".join(path[i:]), paths))
            text_options = rel_paths_for_options
            new_user_options = dict(zip(rel_paths_for_options, options))
        else:
            text_options = options
            new_user_options = dict(zip(options, options))
        user_find_resulsts[user_id] = paths, i, new_user_options
        return False, "Вы имеете в виду {0} или {1}?".format(", ".join(text_options[:-1]),
                                                             text_options[-1])


with open(json_path) as f:
    json_data = json.load(f)
    dict_to_rus(json_data)


if __name__ == '__main__':
    gen = get_by_path(json_data, [])
    n = find_node(gen, "eyes")
    for _ in n:
        print(_)

