"""
Functions to extract named entities (such as node names)
"""


def get_desired_destination_from_go_into_request(command):
    words = command.split()
    if "в" in words:
        return words[words.index("в")+1]
    return ""


def get_desired_node_name_from_start_search_request(command):
    return command.replace("находить", "").strip()


def get_desired_node_name_from_continue_search_request(command):
    return command.replace("я иметь в виду", "").strip()
