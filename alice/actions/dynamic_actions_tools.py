from alice import db
from alice.model.models import AppUser
from alice.model.results_parser import JsonTree


def dynamic_action(function):
    def wrapper(**kwargs):
        user = db.session.query(AppUser).get(kwargs["yandex_id"])
        json_tree = JsonTree(user.json_filename)
        location = user.location.copy()
        return function(user=user, json_tree=json_tree, location=location, **kwargs)
    return wrapper
