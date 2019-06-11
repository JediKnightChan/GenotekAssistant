from alice import Config, db
from alice.actions.dynamic_actions_tools import dynamic_action
from alice.actions.search_mode_tools import get_specifying_options, filter_paths
import alice.ner.recognition as ner
from alice.model.results_parser import JsonTree
from alice.model.models import SearchRequest
from alice.view.pretty_print import get_keys_in_string, truncate_text, get_specifying_options_text, \
    get_relative_paths_for_options


@dynamic_action
def know_location(**kwargs):
    user = kwargs["user"]
    location = kwargs["location"]

    if location:
        text_location = "/".join(location)
    else:
        text_location = "корне"

    json_tree = JsonTree(user.json_filename)
    sub_nodes = truncate_text(get_keys_in_string(json_tree.get_by_path(location)), Config.SINGLE_NODE_MAX_CHARS)
    return "location", {"result": "success", "location": text_location, "sub_nodes": sub_nodes}


@dynamic_action
def go_into(**kwargs):
    user = kwargs["user"]
    json_tree = kwargs["json_tree"]
    location = kwargs["location"]

    desired_destination = ner.get_desired_destination_from_go_into_request(kwargs["command"])
    available_destinations = json_tree.get_by_path(location).keys()
    old_sub_nodes = truncate_text(get_keys_in_string(json_tree.get_by_path(location)), Config.SINGLE_NODE_MAX_CHARS)

    if desired_destination not in available_destinations or isinstance(old_sub_nodes, dict):
        result = "fail"
    else:
        result = "success"
        location.append(desired_destination)
        user.location = location

    new_sub_nodes = truncate_text(get_keys_in_string(json_tree.get_by_path(location)),
                                  Config.SINGLE_NODE_MAX_CHARS)
    db.session.commit()
    return "go_into", {"result": result, "desired_destination": desired_destination, "new_sub_nodes": new_sub_nodes}


@dynamic_action
def go_back(**kwargs):
    user = kwargs["user"]
    json_tree = kwargs["json_tree"]
    location = kwargs["location"]

    # If user not in root
    if location:
        # Delete last element of location
        location = location[:-1]
        user.location = location
        db.session.commit()
        result = "success"
    else:
        result = "fail"

    if location:
        desired_destination = location[-1]
    else:
        desired_destination = "корень"
    new_sub_nodes = truncate_text(get_keys_in_string(json_tree.get_by_path(location)),
                                  Config.SINGLE_NODE_MAX_CHARS)

    return "go_back", {"result": result, "desired_destination": desired_destination, "new_sub_nodes": new_sub_nodes}


@dynamic_action
def find_node(**kwargs):
    user = kwargs["user"]
    json_tree = kwargs["json_tree"]
    command = kwargs["command"]
    search_request = user.search_request
    option_not_available = False

    # If user just turned search mode on
    if search_request is None:
        desired_node_name = ner.get_desired_node_name_from_start_search_request(command)
        potential_paths = list(json_tree.find_node(desired_node_name))
        search_request = SearchRequest(potential_paths=potential_paths, available_specifying_options=[],
                                       comparison_depth=0, app_user=user)
        db.session.add(search_request)
        db.session.commit()
    else:
        potential_paths = search_request.potential_paths
        comparison_depth = search_request.comparison_depth
        available_specifying_options = search_request.available_specifying_options.copy()
        desired_node_name = ner.get_desired_node_name_from_continue_search_request(command)
        if desired_node_name in available_specifying_options:
            real_desired_node_name = available_specifying_options[desired_node_name]
            potential_paths = filter_paths(potential_paths, comparison_depth, real_desired_node_name)
            search_request.potential_paths = potential_paths
            search_request.comparison_depth = comparison_depth + 1
            db.session.commit()
        else:
            option_not_available = True

    potential_paths = search_request.potential_paths.copy()
    comparison_depth = search_request.comparison_depth

    final_path = ""
    new_sub_nodes = ""
    specifying_options = ""
    if option_not_available:
        result = "fail_wrong_option"
    elif len(potential_paths) == 0:
        result = "fail_no_results"

        db.session.delete(search_request)
        db.session.commit()
    elif len(potential_paths) == 1:
        final_location = potential_paths[0]
        user.location = final_location

        result = "success_end_search"
        final_path = "/".join(final_location)
        new_sub_nodes = truncate_text(get_keys_in_string(json_tree.get_by_path(final_location)),
                                      Config.SINGLE_NODE_MAX_CHARS)

        db.session.delete(search_request)
        db.session.commit()
    else:
        result = "continue_search"
        specifying_options_list = get_specifying_options(potential_paths, comparison_depth)
        while len(specifying_options_list) < 2:
            comparison_depth += 1
            specifying_options_list = get_specifying_options(potential_paths, comparison_depth)

        if len(specifying_options_list) == 2:
            specifying_options_text_list = get_relative_paths_for_options(potential_paths, comparison_depth)
        else:
            specifying_options_text_list = specifying_options_list

        specifying_options = get_specifying_options_text(specifying_options_text_list)

        search_request.available_specifying_options = dict(zip(specifying_options_text_list, specifying_options_list))
        search_request.comparison_depth = comparison_depth
        db.session.commit()

    return "find_node", {"result": result, "final_path": final_path,
                         "new_sub_nodes": new_sub_nodes, "specifying_options": specifying_options}
