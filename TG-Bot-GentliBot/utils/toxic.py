

import pymorphy2

from data.config import toxic_model, toxic_vectorizer, TOKEN_RE
from data.config import STOPWORDS



def tokenize_text(txt, min_lenght_token=2):
    """
    Токенизирует текст по словам
    :param txt: исходный текст
    :param min_lenght_token: минимальная длина токена
    :return: список токенов
    """
    txt = txt.lower()
    all_tokens = TOKEN_RE.findall(txt)
    return [token for token in all_tokens if len(token) >= min_lenght_token]


def remove_stopwords(tokens):
    """
    Удаляет стоп-слова из списка токенов

    :param tokens: список токенов
    :return: список токенов без стоп-слов
    """


    return list(filter(lambda token: token not in STOPWORDS, tokens))


def lemmatizing(tokens):
    """
    Приведение токенов к начальной форме (лемматизация)
    :param tokens: список токенов
    :return: список токенов в начальной форме
    """
    lemmatizer = pymorphy2.MorphAnalyzer()
    return [lemmatizer.parse(token)[0].normal_form for token in tokens]


def text_cleaning(txt):
    """
    Выполненят предобработку текста
    :param txt: исходный текст
    :return: очищенный текст
    """
    tokens = tokenize_text(txt)
    tokens = remove_stopwords(tokens)
    tokens = lemmatizing(tokens)
    return ' '.join(tokens)


def get_probabality_toxic(text):
    """
    Вычисляет вероятность токсичности текста и возвращает ее, если она больша порогового значения
    :param text: текст для оценки токсичности
    :return: вероятность токсичности
    """
    clean_text = text_cleaning(text)
    X_example = toxic_vectorizer.transform([clean_text])
    toxic_probabality = toxic_model.predict_proba(X_example)[0, 1]
    if toxic_probabality >= 0.5:
        return toxic_probabality
