from test_help_tools import assert_alice_says


def test_index(client):
    rv = client.get('/')
    assert rv.data == b'Hello World!'


def test_bot(client):
    assert_alice_says(client, "", "Здравствуйте, Карабас. Это приватный навык. "
                                  "Я умею говорить, где вы находитесь в JSON-файле", new_session=True)
    assert_alice_says(client, "Где я?", "Вы находитесь в корне. Здесь есть inheritance, генеалогия, "
                                        "черты, мультифакторы, генетика.")
    assert_alice_says(client, "Перейди в генеалогия", "Вы перешли в генеалогия. Здесь есть материнская линия, "
                                                      "отцовская линия, происхождение, доля неандертальца.")
    assert_alice_says(client, "Где я?", "Вы находитесь в генеалогия. Здесь есть материнская линия, "
                                        "отцовская линия, происхождение, доля неандертальца.")
    assert_alice_says(client, "Перейти назад", "Вы перешли назад в корень. Здесь есть inheritance, генеалогия, "
                                               "черты, мультифакторы, генетика.")
    assert_alice_says(client, "Кто я?", "Вы на 5.3% - North Caucasus, на 94.2% - Eastern Europe, на 0.5% - Undefined.")


def test_search(client):
    assert_alice_says(client, "", "Здравствуйте, Карабас. Это приватный навык. "
                                  "Я умею говорить, где вы находитесь в JSON-файле", new_session=True)
    assert_alice_says(client, "Найти data", "Вы имеете в виду inheritance, генеалогия, "
                                            "черты, мультифакторы или генетика?")
    assert_alice_says(client, "Генеалогия", "Вы имеете в виду материнская линия, отцовская линия, "
                                            "происхождение или доля неандертальца?")
    assert_alice_says(client, "Доля неандертальца", "Вы успешно перешли в генеалогия/доля неандертальца/data. "
                                                    "Здесь есть number_of_neanderthal_alleles, "
                                                    "number_of_studied_neanderthal_alleles, procentile.")


def test_search2(client):
    assert_alice_says(client, "", "Здравствуйте, Карабас. Это приватный навык. "
                                  "Я умею говорить, где вы находитесь в JSON-файле", new_session=True)
    assert_alice_says(client, "Найти eyes", "Вы имеете в виду eyes или child/eyes?")
    assert_alice_says(client, "Child/eyes", "Вы успешно перешли в черты/appearance/data/child/eyes. "
                                            "Здесь есть probabilities, quantilies, sd.")


def test_deseases(client):
    assert_alice_says(client, "", "Здравствуйте, Карабас. Это приватный навык. "
                                  "Я умею говорить, где вы находитесь в JSON-файле", new_session=True)
    assert_alice_says(client, "Какие у меня наследственные заболевания", "У вас нет наследственных заболеваний.")
