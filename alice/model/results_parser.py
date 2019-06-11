import json
from functools import reduce
import operator
from os.path import join as path_join
from alice import Config


results_dir = path_join(Config.BASE_DIR, "alice", "model", "results")
with open(path_join(Config.BASE_DIR, "alice", "model", "result_translation.json")) as translation_file:
    en_to_rus = json.load(translation_file)


class JsonTree:
    def __init__(self, filename):
        self.filename = filename
        with open(path_join(results_dir, self.filename)) as stream:
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
        """
        Translates keys in the dict from English into Russian
        :param mydict: the dict that should be translated
        :return: None
        """
        for key, value in mydict.items():
            if key in en_to_rus:
                new_key = en_to_rus[key]
                mydict[new_key] = mydict.pop(key)
            if isinstance(value, dict):
                self.translate_dict(value)

    def find_node(self, node_name):
        """
        Finds paths in genetical_data (self.json_dict) containing <node_name>
        :param string node_name: name of the node we want to find
        :return list: paths (lists of string nodes) containing node_name
        """
        return self._json_search.search_node(self.json_dict, node_name, [])


class JsonSearch:
    def __init__(self, json_tree):
        self.json_tree = json_tree
        self.json_dict = self.json_tree.json_dict

    def _get_values_from_list(self, mylist, node_name, path):
        """
        Finds paths of the keys in nested list (tree structure) that are equal to node_name
        :param list mylist: The list where the search will be performed
        :param string node_name: The node we want to find (keys of the dict)
        :param list path: As it's recursive function, we should save the path we are iterating right now
        :return list: paths (lists of string nodes) we were looking for
        """
        for i, value in enumerate(mylist):
            temp_path = path.copy()
            temp_path.append(i)
            if isinstance(value, dict):
                yield from self.search_node(value, node_name, temp_path)
            elif isinstance(value, list):
                yield from self._get_values_from_list(value, node_name, temp_path)

    def search_node(self, mydict, node_name, path):
        """
        Finds paths of the keys in nested dict that are equal to node_name
        :param dict mydict: The dictionary where the search will be performed
        :param string node_name: The node we want to find (keys of the dict)
        :param list path: As it's recursive function, we should save the path we are iterating right now
        :return list: paths (lists of string nodes) we were looking for
        """
        for key, value in mydict.items():
            temp_path = path.copy()
            temp_path.append(key)
            if key == node_name:
                yield temp_path
            if isinstance(value, dict):
                yield from self.search_node(value, node_name, temp_path)
            elif isinstance(value, list):
                yield from self._get_values_from_list(value, node_name, temp_path)
