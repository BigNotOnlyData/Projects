import random

from data.config import intent_model, intent_vectorizer, BOT_CONFIG, TOKEN_RE


def text_cleaning(txt):
    """
    Токенизирует текст по словам
    :param txt: исходный текст
    :return: список токенов
    """
    txt = txt.lower()
    all_tokens = TOKEN_RE.findall(txt)
    return ' '.join([token for token in all_tokens])


def get_intent_by_model(text):
    """
    Вычисляет интент по тексту и возвращает его, если вероятность интента больше порогового значения
    :param text: текст
    :return: интент
    """
    prob = intent_model.predict_proba(intent_vectorizer.transform([text]))
    intent = intent_model.classes_[prob.argmax()]
    max_prob = prob.max()
    if max_prob >= 0.35:
        return intent


def get_intent_answer(input_text):
    """
    Возвращает ответ для интента, если он есть
    :param input_text: текст
    :return: ответ
    """
    intent = get_intent_by_model(text_cleaning(input_text))
    if intent:
        return random.choice(BOT_CONFIG['intents'][intent]['responses'])




