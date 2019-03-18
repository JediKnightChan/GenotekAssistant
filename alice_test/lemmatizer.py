import pymorphy2
morph = pymorphy2.MorphAnalyzer()


def lemmatize_word(word):
    lemm_word = morph.parse(word)[0]
    return lemm_word.normal_form


def tokenize(utterance):
    return utterance.split()


def lemmatize(utterance):
    tokens = tokenize(utterance)
    tokens = list(map(lemmatize_word, tokens))
    return " ".join(tokens)


if __name__ == '__main__':
    print(lemmatize("найди глаза"))

