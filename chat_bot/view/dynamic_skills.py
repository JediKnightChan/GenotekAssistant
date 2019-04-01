
def get_location(user_id):
    subnodes = ad.get_keys(ad.get_by_path(ad.json_data, coordinates[user_id]))
    subnodes = truncate_text(str(subnodes), SINGLE_NODE_MAX_CHARS)
    current_node = user_in_root(user_id) and "корне" or coordinates[user_id][-1]
    return "Вы находитесь в {}. Тут есть {}".format(current_node, subnodes)