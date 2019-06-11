
def say_hello(**kwargs):
    username = "Карабас"
    return "hello", {"result": "success", "username": username}


def tell_about(**kwargs):
    return "telling_about", {"result": "success"}


def say_unknown(**kwargs):
    return "unknown", {"result": "success"}

