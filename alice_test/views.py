from django.shortcuts import render
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
    tokens = yandex_data["request"]["nlu"]["tokens"]
    user_id = yandex_data['session']['user_id']
    if yandex_data['session']['new']:
        coordinates[user_id] = []
        return "Я умею говорить, где вы находитесь в JSON-файле"
    if "где я" in command:
        subnodes = ad.get_keys(ad.get_by_path(ad.json_data, coordinates[user_id]))
        current_node = coordinates[user_id] == [] and "корне" or coordinates[user_id][-1]
        text = "Вы находитесь в {}. Тут есть {}".format(current_node, subnodes)
    elif "перейди в" in command:
        subnodes = ad.get_by_path(ad.json_data, coordinates[user_id])
        requested_subnode = command.replace("перейди в", "").strip()
        if type(subnodes) is not dict:
            return "Туда нельзя перейти"
        if requested_subnode not in subnodes.keys():
            return "Его там нет"
        else:
            coordinates[user_id].append(requested_subnode)
            new_subnodes = ad.get_keys(ad.get_by_path(ad.json_data, coordinates[user_id]))
            text = "Я перешла в {}. Здесь есть {}".format(requested_subnode, new_subnodes)
    else:
        text = "Не умею"
    return text
