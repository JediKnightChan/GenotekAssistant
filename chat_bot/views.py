import json
from os.path import join as path_join
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from YandexAlice.settings import TEXT_MAX_CHARS, SINGLE_NODE_MAX_CHARS, BASE_DIR
from chat_bot.nlp import test_bot
from chat_bot.lemmatizer import lemmatize

from chat_bot.view.pretty_print import truncate_text, get_keys_str
from chat_bot.model.json_parser import JsonTree
import chat_bot.controller.search_specifier as search_specifier

coordinates = {}
user_find_resulsts = {}
json_path = path_join(BASE_DIR, "chat_bot", "data.json")
genetic_data = JsonTree(json_path)


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
    command = lemmatize(yandex_data["request"]["command"].lower())
    user_id = yandex_data['session']['user_id']
    if yandex_data['session']['new'] or user_id not in coordinates:
        coordinates[user_id] = []
        user_find_resulsts.pop(user_id, None)
        return say_about()

    if user_id in user_find_resulsts:
        return handle_find_dialogue(user_id, command)
    if test_bot([command]) == ["help"]:
        text = app_help()
    elif test_bot([command]) == ["where"]:
        text = get_location(user_id)
    elif test_bot([command]) == ["go_back"]:
        text = go_back(user_id)
    elif "перейти в" in command:
        text = go_to_subnode(user_id, command)
    elif "найти" in command:
        text = search_for_node(user_id, command)
    elif "происхождение" in command:
        text = know_ancestry(user_id)
    else:
        text = "Не умею"
    text = truncate_text(text, TEXT_MAX_CHARS)
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
    subnodes = genetic_data.get_by_path(coordinates[user_id])
    subnodes_str = truncate_text(get_keys_str(subnodes), SINGLE_NODE_MAX_CHARS)
    current_node = user_in_root(user_id) and "корне" or coordinates[user_id][-1]
    return "Вы находитесь в {}. Тут есть {}".format(current_node, subnodes_str)


def go_back(user_id):
    if user_in_root(user_id):
        return "Вы находитесь в корне"
    else:
        prev_node = coordinates[user_id].pop()
        current_node = user_in_root(user_id) and "корень" or coordinates[user_id][-1]
        return "Вы перешли из {} на уровень вверх и вернулись в {}".format(prev_node, current_node)


def get_subnodes_text(destination, user_id):
    subnodes = genetic_data.get_by_path(coordinates[user_id])
    subnodes_str = truncate_text(get_keys_str(subnodes), SINGLE_NODE_MAX_CHARS)
    return "Я перешла в {}. Здесь есть {}".format(destination, subnodes_str)


def go_to_subnode(user_id, command):
    subnodes = genetic_data.get_by_path(coordinates[user_id])
    requested_subnode = command.replace("перейти в", "").strip()
    if type(subnodes) is not dict:
        return "Туда нельзя перейти"
    if requested_subnode not in subnodes.keys():
        return "Его там нет"
    else:
        coordinates[user_id].append(requested_subnode)
        return get_subnodes_text(requested_subnode, user_id)


def search_for_node(user_id, command):
    node_name = command.split()[-1]
    option_paths = list(genetic_data.find_node(node_name))
    if len(option_paths) == 0:
        return "Ничего не найдено"
    elif len(option_paths) == 1:
        coordinates[user_id] = option_paths[0]
        destination = "/".join(option_paths[0])
        return get_subnodes_text(destination, user_id)
    else:
        user_find_resulsts[user_id] = option_paths, 0, {}
        return handle_find_dialogue(user_id, None)


def handle_find_dialogue(user_id, command):
    if command:
        user_key = command.replace("я имею в виду", "").strip()
        paths, i, user_options = user_find_resulsts[user_id]
        if user_key not in user_options:
            return "Пожалуйста, выберите один из вариантов"
        else:
            real_key = user_options[user_key]
            user_find_resulsts[user_id] = search_specifier.filter_paths(paths, i, real_key), i+1, {}
    end_find_dialogue, result = search_specifier.choose_option(user_find_resulsts, user_id)
    if end_find_dialogue:
        user_find_resulsts.pop(user_id)
        coordinates[user_id] = result
        destination = "/".join(result)
        return get_subnodes_text(destination, user_id)
    else:
        return result


def know_ancestry(user_id):
    coordinates[user_id] = ["генеалогия", "происхождение", "data"]
    race_to_percent = genetic_data.get_by_path(coordinates[user_id])
    races_and_percents = []
    for race in race_to_percent:
        percent = race_to_percent[race]["percent"]
        if percent:
            races_and_percents.append((percent, race))

    result = "Вы {}.".format(', '.join(['на {}% - {}'.format(race, percent) for race, percent in races_and_percents]))
    return result
