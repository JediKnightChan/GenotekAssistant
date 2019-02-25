import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import alice_test.additional as ad

coordinates = {}
user_find_resulsts = {}
LOOP_NODE_MAX_CHARS = 40
SINGLE_NODE_MAX_CHARS = 100
TEXT_MAX_CHARS = 1000


@csrf_exempt
def alice_test(request):
    yandex_data = json.loads(request.body)
    user_id = yandex_data['session']['user_id']
    text = handle_dialog(yandex_data)

    response = {
        "response": {
            "text": text,
            "tts": text,
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

    if user_id in user_find_resulsts:
        return handle_find_dialogue(user_id, command)

    if "помощь" in command or "что ты умеешь" in command:
        text = app_help()
    elif "где я" in command:
        text = get_location(user_id)
    elif "перейди назад" in command:
        text = go_back(user_id)
    elif "перейди в" in command:
        text = go_to_subnode(user_id, command)
    elif "найди" in command:
        text = search_for_node(user_id, command)
    else:
        text = "Не умею"
    text = truncate_text(text, TEXT_MAX_CHARS)
    return text


def truncate_text(text, max_chars):
    if len(text) > TEXT_MAX_CHARS:
        text = "".join([text[:max_chars-3], "..."])
    return text


def user_in_root(user_id):
    return coordinates[user_id] == []


def say_about():
    return "Это приватный навык. Я умею говорить, где вы находитесь в JSON-файле"


def app_help():
    return "Я помогу вам узнать результаты генетического теста, представленные в виде древовидной структуры.\n" \
           "Команды:\n" \
           "Где я? - Рассказывает, где вы находитесь в дереве и показывает подузлы, куда вы можете перейди\n" \
           "Перейди в <узел> - Перемещает вас в узел и показывает его подузлы\n" \
           "Перейди назад - Перемещает вас на уровень вверх\n" \
           "Найди <узел> - Показывает узлы с таким именем и их содержимое\n"


def get_location(user_id):
    subnodes = ad.get_keys(ad.get_by_path(ad.json_data, coordinates[user_id]))
    subnodes = truncate_text(str(subnodes), SINGLE_NODE_MAX_CHARS)
    current_node = user_in_root(user_id) and "корне" or coordinates[user_id][-1]
    return "Вы находитесь в {}. Тут есть {}".format(current_node, subnodes)


def go_back(user_id):
    if user_in_root(user_id):
        return "Вы находитесь в корне"
    else:
        prev_node = coordinates[user_id].pop()
        current_node = user_in_root(user_id) and "корень" or coordinates[user_id][-1]
        return "Вы перешли из {} на уровень вверх и вернулись в {}".format(prev_node, current_node)


def get_subnodes_text(destination, user_id):
    subnodes = ad.get_keys(ad.get_by_path(ad.json_data, coordinates[user_id]))
    subnodes = truncate_text(str(subnodes), SINGLE_NODE_MAX_CHARS)
    return "Я перешла в {}. Здесь есть {}".format(destination, subnodes)


def go_to_subnode(user_id, command):
    subnodes = ad.get_by_path(ad.json_data, coordinates[user_id])
    requested_subnode = command.replace("перейди в", "").strip()
    if type(subnodes) is not dict:
        return "Туда нельзя перейти"
    if requested_subnode not in subnodes.keys():
        return "Его там нет"
    else:
        coordinates[user_id].append(requested_subnode)
        return get_subnodes_text(requested_subnode, user_id)


def search_for_node(user_id, command):
    node_name = command.split()[-1]
    if "глобально" in command:
        search_scope = ad.json_data
    else:
        search_scope = ad.get_by_path(ad.json_data, coordinates[user_id])
    option_paths = list(ad.find_node(search_scope, node_name))
    if len(option_paths) == 0:
        return "Ничего не найдено"
    elif len(option_paths) == 1:
        coordinates[user_id] = option_paths[0]
        destination = "/".join(option_paths[0])
        return get_subnodes_text(destination, user_id)
    else:
        user_find_resulsts[user_id] = option_paths, 0
        return handle_find_dialogue(user_id, None)


def handle_find_dialogue(user_id, command):
    if command:
        key = command.replace("я имею в виду", "").strip()
        paths, i = user_find_resulsts[user_id]
        options = ad.get_options(paths, i)
        if key not in options:
            return "Пожалуйста, выберите один из вариантов"
        else:
            user_find_resulsts[user_id] = ad.filter_paths(paths, i, key), i+1
    end_find_dialogue, result = ad.choose_option(user_find_resulsts, user_id)
    if end_find_dialogue:
        user_find_resulsts[user_id].pop(user_id)
        coordinates[user_id] = result
        destination = "/".join(result)
        return get_subnodes_text(destination, user_id)
    else:
        return result
