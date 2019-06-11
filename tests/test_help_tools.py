import json


def create_request(command, new_session=False):
    return {
        "meta": {
            "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
            "interfaces": {
                "screen": {}
            },
            "locale": "ru-RU",
            "timezone": "UTC"
        },
        "request": {
            "command": command,
            "nlu": {
                "entities": [],
                "tokens": command.split()
            },
            "original_utterance": command,
            "type": "SimpleUtterance"
        },
        "session": {
            "message_id": 1,
            "new": new_session,
            "session_id": "f39a274b-3e2e5768-52f71510-969e6d62",
            "skill_id": "f8956b2e-8784-45bf-b50f-f11758a6b5ee",
            "user_id": "D316B93FB1C185BC2D2EBCE48A0EEECE677E221EDAD735650D6D2EE447641EF5"
        },
        "version": "1.0"
    }


def assert_alice_says(client, command, expected, new_session=False):
    response = client.post('/alice', data=json.dumps(create_request(command, new_session=new_session)),
                           content_type='application/json')
    assert response.status_code == 200
    response_data = json.loads(response.data)
    alice_response_phrase = response_data['response']['text']
    assert alice_response_phrase == expected
