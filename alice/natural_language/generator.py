token_to_text = {
    "hello": {
        "success": "Здравствуйте, {username}. Это приватный навык. Я умею говорить, где вы находитесь в JSON-файле"
    },
    "telling_about": {"success":
                          "Я помогу вам узнать результаты генетического теста, представленные в виде древовидной "
                          "структуры.\n "
                          "Команды:\n"
                          "Где я? - Рассказывает, где вы находитесь в дереве и показывает подузлы, куда вы можете "
                          "перейти\n"
                          "Перейди в <узел> - Перемещает вас в узел и показывает его подузлы\n"
                          "Перейди назад - Перемещает вас на уровень вверх\n"
                          "Найди <узел> - Показывает узлы с таким именем и их содержимое\n",
                      },
    "unknown": {"success": "Я не умею это делать"},
    "location": {"success": "Вы находитесь в {location}. Здесь есть {sub_nodes}."},
    "go_into": {
        "success": "Вы перешли в {desired_destination}. Здесь есть {new_sub_nodes}.",
        "fail": "Вы не можете перейти в {desired_destination}.",
    },
    "go_back": {
        "success": "Вы перешли назад в {desired_destination}. Здесь есть {new_sub_nodes}.",
        "fail": "Вы находитесь в корне и не можете перейти назад.",
    },
    "find_node": {
        "fail_no_results": "Ничего не найдено.",
        "fail_wrong_option": "Пожалуйста, выберите один из вариантов",
        "success_end_search": "Вы успешно перешли в {final_path}. Здесь есть {new_sub_nodes}.",
        "continue_search": "Вы имеете в виду {specifying_options}?",
    },
    "know_ancestry": {
        "success": "Вы {ancestry}.",
    },
    "know_inherited_diseases": {
        "success": "У вас есть наследственные заболевания.",
        "fail_list_empty": "У вас нет наследственных заболеваний."
    }
}


def generate_text(token, nl_entities):
    """
    :param string token: the action that should be performed (or was performed - now we just need to respond)
    :param dict nl_entities: the data we should insert into response
    :return string: the final text of the response
    """
    result = nl_entities["result"]
    text = token_to_text[token][result]
    return text.format(**nl_entities)
