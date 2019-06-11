"""
The functions to prettify or truncate text
"""


def get_keys_in_string(node):
    if isinstance(node, dict):
        return ", ".join(node.keys())
    else:
        return node


def truncate_text(text, max_chars):
    if len(text) > max_chars:
        text = "".join([text[:max_chars - 3], "..."])
    return text


def get_specifying_options_text(specifying_options):
    return "{0} или {1}".format(", ".join(specifying_options[:-1]),
                                specifying_options[-1])


def get_relative_paths_for_options(paths, depth):
    return list(map(lambda path: "/".join(path[depth:]), paths))


def get_race_to_percent_text(races_and_percents):
    return ', '.join(['на {percent}% - {race}'.format(race=race, percent=percent)
                      for [race, percent] in races_and_percents])
