
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
