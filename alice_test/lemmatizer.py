import pymorphy2
morph = pymorphy2.MorphAnalyzer()


def tokenize(utterance):
    return utterance.split()


def lemmatize(utterance):
    tokens = tokenize(utterance)
    tokens = list(map(lambda word: morph.parse(word)[0].normal_form, tokens))
    return " ".join(tokens)


if __name__ == '__main__':
    print(lemmatize("что ты умеешь"))

