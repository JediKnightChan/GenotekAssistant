from alice import db
from alice.actions.dynamic_actions_tools import dynamic_action
from alice.view.pretty_print import get_race_to_percent_text


command_to_location = {
    "know_ancestry": ["генеалогия", "происхождение", "data"],
    "know_inherited_diseases": ["inheritance", "inheritance_carrier", "data"],
}


@dynamic_action
def know_ancestry(**kwargs):
    user = kwargs["user"]
    json_tree = kwargs["json_tree"]

    ancestry_location = command_to_location["know_ancestry"]
    user.location = ancestry_location
    db.session.commit()

    race_to_percent = json_tree.get_by_path(ancestry_location)
    races_and_percents = []
    for race in race_to_percent:
        percent = race_to_percent[race]["percent"]
        if percent:
            races_and_percents.append((race, percent))

    ancestry = get_race_to_percent_text(races_and_percents)
    return "know_ancestry", {"result": "success", "ancestry": ancestry}


@dynamic_action
def know_inherited_diseases(**kwargs):
    user = kwargs["user"]
    json_tree = kwargs["json_tree"]

    inherited_diseases_location = command_to_location["know_inherited_diseases"]
    user.location = inherited_diseases_location
    db.session.commit()

    list_of_deseases = json_tree.get_by_path(inherited_diseases_location)
    if list_of_deseases:
        result = "success"
    else:
        result = "fail_list_empty"

    return "know_inherited_diseases", {"result": result}
