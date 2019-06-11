import requests
import json


def get_rasa_server_intent(utterance, port=5005):
    """
    :param utterance: the original utterance from the the user request
    :param port: port where RASA server is working
    :return: intent or None

    Classifies intent of the utterance by asking Rasa server
    """
    try:
        r = requests.post("http://127.0.0.1:{}/model/parse".format(port), data=json.dumps({"text": utterance})).json()
    except requests.exceptions.ConnectionError:
        r = None
    if r:
        return r["intent"]["name"]


intents_to_phrase_lists = {
    "hello": ["привет"],
    "help": ["помощь", "что ты уметь"],
    "know_location": ["где я"],
    "go_back": ["назад"],
    "go_into": ["переходить в"],
    "find_node": ["находить"],
}


def classify_intent(original_utterance, command, session_is_new, user_search_request):
    """
    Classifies intent of the phrase user said to Alice, which was processed
    :param string original_utterance: original user utterance
    :param string command: lowered processed user utterance
    :param boolean session_is_new: True if user just started the dialog
    :param db.SearchRequest user_search_request: None if search mode off, else instance of the model
    :return string intent: intent of the user utterance
    """
    if session_is_new:
        return "hello"
    if user_search_request:
        return "find_node"
    for intent, phrases in intents_to_phrase_lists.items():
        for phrase in phrases:
            if phrase in command:
                return intent

    # It wasn't a fixed command, we should predict it
    possible_intent = get_rasa_server_intent(original_utterance)
    if possible_intent:
        return possible_intent
    return "unknown"
