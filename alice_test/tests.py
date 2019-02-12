from django.test import Client, TestCase
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


def test_alice(self, command, expected, new_session=False):
    response = self.client.post('/alice/', json.dumps(create_request(command, new_session=new_session)),
                                content_type="application/json")
    self.assertEqual(response.status_code, 200)
    response_data = json.loads(response.content)
    text_response = response_data['response']['text']
    self.assertEqual(text_response, expected)


class MyTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_alice_dialogue1(self):
        test_alice(self, "", "Я умею говорить, где вы находитесь в JSON-файле", new_session=True)
        test_alice(self, "Где я?", "Вы находитесь в корне. Тут есть inheritance, "
                                  "генеалогия, черты, мультифакторы, генетика")
        test_alice(self, "Перейди в генеалогия", "Я перешла в генеалогия. Здесь есть y_chr_haplogroup, "
                                                "mt_dna_haplogroup, ancestry_decomposition, neanderthal")
