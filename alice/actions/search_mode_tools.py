
def get_specifying_options(paths, comparison_depth):
    """
    Gets options to specify user request (What nodes user could desire)
    :param list paths: paths (lists of string nodes) to get options from
    :param comparison_depth: the index where we should get options (string nodes)
    :return list of strings: options user could desire
    """
    specifying_options = []
    for path in paths:
        # Skip paths with elements number less than comparison_depth
        if comparison_depth < len(path):
            option = path[comparison_depth]
            if option not in specifying_options:
                specifying_options.append(option)
    return specifying_options


def filter_paths(paths, comparison_depth, desired_node):
    """
    Filters paths to get ones with desired node. It's used for specification of user request ("Did you mean X or Y?")
    :param list paths: paths (lists of string nodes) to filter
    :param int comparison_depth: the index where the desired node should be found
    :param string desired_node: the node to compare with
    :return list: filtered paths (lists of string nodes)
    """
    filtered_paths = []
    for path in paths:
        # Skip paths with elements number less than comparison_depth
        if comparison_depth < len(path):
            node_to_compare = path[comparison_depth]
            if node_to_compare == desired_node:
                filtered_paths.append(path)
    return filtered_paths

