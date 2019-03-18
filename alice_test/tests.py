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


def test_alice(test_obj, command, expected, new_session=False):
    response = test_obj.client.post('/alice/', json.dumps(create_request(command, new_session=new_session)),
                                    content_type="application/json")
    test_obj.assertEqual(response.status_code, 200)
    response_data = json.loads(response.content)
    text_response = response_data['response']['text']
    test_obj.assertEqual(text_response, expected)


class MyTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_go_to(self):
        test_alice(self, "", "Это приватный навык. Я умею говорить, где вы находитесь в JSON-файле", new_session=True)
        test_alice(self, "Алиса, скажи пожалуйста, где я?", "Вы находитесь в корне. Тут есть inheritance, "
                                  "генеалогия, черты, мультифакторы, генетика")
        test_alice(self, "Перейди в генеалогия", "Я перешла в генеалогия. Здесь есть материнская линия, "
                                                "отцовская линия, происхождение, доля неандертальца")

    def test_go_back(self):
        test_alice(self, "", "Это приватный навык. Я умею говорить, где вы находитесь в JSON-файле", new_session=True)
        test_alice(self, "Перейди назад", "Вы находитесь в корне")
        test_alice(self, "Перейди в генеалогия", "Я перешла в генеалогия. Здесь есть материнская линия, "
                                                "отцовская линия, происхождение, доля неандертальца")
        test_alice(self, "Перейди назад", "Вы перешли из генеалогия на уровень вверх и вернулись в корень")

    def test_find(self):
        test_alice(self, "", "Это приватный навык. Я умею говорить, где вы находитесь в JSON-файле", new_session=True)
        test_alice(self, "Найди абракадабра", "Ничего не найдено")
        test_alice(self, "Найди eyes", "Вы имеете в виду eyes или child/eyes?")
        test_alice(self, "eyes", "Я перешла в черты/appearance/data/eyes. Здесь есть Snps, Probabilities, Predictions")
        test_alice(self, "Где я?", "Вы находитесь в eyes. Тут есть Snps, Probabilities, Predictions")

    def test_get_ancestry(self):
        test_alice(self, "", "Это приватный навык. Я умею говорить, где вы находитесь в JSON-файле", new_session=True)
        test_alice(self, "Какое у меня происхождение", "Я перешла в ваше происхождение. Здесь есть Jewish, Africa, "
                                                       "Africa, Northern, Arabia, South Caucasus, North Caucasus, "
                                                       "Central Asia, East Asia, Western Europe, Eastern Europe, "
                                                       "Middle East, Siberia, South Asia (Pakistan), South Asia (India)"
                                                       ", Undefined")
    