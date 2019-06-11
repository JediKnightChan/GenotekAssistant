import alice.actions.static_actions as static_actions
import alice.actions.dynamic_actions as dynamic_actions
import alice.actions.concretized_actions as concretized_actions


intents_to_actions = {
    "hello": static_actions.say_hello,
    "help": static_actions.tell_about,
    "unknown": static_actions.say_unknown,
    "know_location": dynamic_actions.know_location,
    "go_into": dynamic_actions.go_into,
    "go_back": dynamic_actions.go_back,
    "find_node": dynamic_actions.find_node,
    "know_ancestry": concretized_actions.know_ancestry,
    "know_inherited_diseases": concretized_actions.know_inherited_diseases,
}


def execute_action(intent, yandex_id, command):
    return intents_to_actions[intent](yandex_id=yandex_id, command=command)
