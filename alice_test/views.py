import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import alice_test.additional as ad

coordinates = {}


@csrf_exempt
def alice_test(request):
    yandex_data = json.loads(request.body)
    user_id = yandex_data['session']['user_id']
    text = handle_dialog(yandex_data)

    response = {
        "response": {
            "text": str(text),
            "end_session": False,
        },
        "session": {
            "session_id": yandex_data['session']['session_id'],
            "message_id": yandex_data['session']['message_id'],
            "user_id": user_id,
        },
        "version": yandex_data['version']
    }
    return JsonResponse(response)


def handle_dialog(yandex_data):
    command = yandex_data["request"]["command"].lower()
    user_id = yandex_data['session']['user_id']
    if yandex_data['session']['new'] or user_id not in coordinates:
        coordinates[user_id] = []
        return say_about()
    if "где я" in command:
        text = get_location(user_id)
    elif "перейди назад" in command:
        text = go_back(user_id)
    elif "перейди в" in command:
        text = go_to_subnode(user_id, command)
    elif "найди" in command:
        text = search_for_node(user_id, command)
    else:
        text = "Не умею"
    return text


def user_in_root(user_id):
    return coordinates[user_id] == []


def say_about():
    return "Я умею говорить, где вы находитесь в JSON-файле"


def get_location(user_id):
    subnodes = ad.get_keys(ad.get_by_path(ad.json_data, coordinates[user_id]))
    current_node = user_in_root(user_id) and "корне" or coordinates[user_id][-1]
    return "Вы находитесь в {}. Тут есть {}".format(current_node, subnodes)


def go_back(user_id):
    if user_in_root(user_id):
        return "Вы находитесь в корне"
    else:
        prev_node = coordinates[user_id].pop()
        current_node = user_in_root(user_id) and "корень" or coordinates[user_id][-1]
        return "Вы перешли из {} на уровень вверх и вернулись в {}".format(prev_node, current_node)


def go_to_subnode(user_id, command):
    subnodes = ad.get_by_path(ad.json_data, coordinates[user_id])
    requested_subnode = command.replace("перейди в", "").strip()
    if type(subnodes) is not dict:
        return "Туда нельзя перейти"
    if requested_subnode not in subnodes.keys():
        return "Его там нет"
    else:
        coordinates[user_id].append(requested_subnode)
        new_subnodes = ad.get_keys(ad.get_by_path(ad.json_data, coordinates[user_id]))
        return "Я перешла в {}. Здесь есть {}".format(requested_subnode, new_subnodes)


def search_for_node(user_id, command):
    node_name = command.split()[-1]
    if "глобально" in command:
        search_scope = ad.get_by_path(ad.json_data, coordinates[user_id])
    else:
        search_scope = ad.json_data
    result = ad.find_node(search_scope, node_name)
    return "В узле {} есть вот что:\n{}".format(node_name, str(result))
