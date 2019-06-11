from pymystem3 import Mystem

m = Mystem()


def lemmatize_sentence(text):
    """
    Lemmatizes sentence contextually
    :param string text: the text to lemmatize
    :return string: lemmatized sentence
    """
    lemmas = m.lemmatize(text)
    return "".join(lemmas).strip()
