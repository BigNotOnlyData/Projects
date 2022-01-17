import speech_recognition as sr


def text_from_audio(audio):
    """
    Распознает текст из аудио файла

    :param audio : file (.wav)
    :return: text
    """
    try:
        r = sr.Recognizer()
        voice_file = sr.AudioFile(audio)
        with voice_file as audio_file:
            r.adjust_for_ambient_noise(audio_file)
            content = r.record(audio_file)

        text = r.recognize_google(content, language="ru-RU")
        return text
    except sr.UnknownValueError as e:
        return "Не сумел распознать"
    except sr.RequestError as e:
        return "Проблемы с запросом к Google"
