
def get_keys_str(node):
    if type(node) is dict:
        return ", ".join(node.keys())
    else:
        return node


def truncate_text(text, max_chars):
    if len(text) > max_chars:
        text = "".join([text[:max_chars-3], "..."])
    return text
