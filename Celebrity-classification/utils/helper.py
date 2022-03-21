import json
import pickle
from pathlib import Path

import face_recognition
import numpy as np
from PIL import Image

from .config import ALLOWED_EXTENSIONS


def _get_key(dict_labels, values):
    """
    :param dict_labels: словарь {имя актера: код актера}
    :param values: значения кодов актеров
    :return: возвращает имена актеров по их кодам
    """
    inverse_dict = {v: k for k, v in dict_labels.items()}
    return [inverse_dict[key] for key in values]


def _resize_image(image_file, to_size=1024):
    """
    :param image_file: путь к файлу или файловый объект
    :param to_size: Ширина нового изображения
    :return: измененное фото с указанной шириной
    """
    # Загрузим фото
    image = Image.open(image_file)
    # получим его размер
    size = image.size
    # получим коэффициент, на который нужно уменьшить/увеличить
    # изображение по одной из сторон до to_size
    coef = to_size / size[0]
    # изменяем размер изображения
    resized_image = image.resize((int(size[0] * coef), int(size[1] * coef)))
    return resized_image.convert('RGB')


def predict_actors(image_file, model, dict_labels):
    """
    :param image_file: путь к файлу или файловый объект
    :param model: модель классификации
    :param dict_labels: словарь {имя актера: код актера}
    :return: (топ 5 актеров, соответсвующие вероятности)
    """
    # Загрузка фото
    img = _resize_image(image_file)
    face_array = np.asarray(img)
    face_locations = face_recognition.face_locations(face_array)

    if len(face_locations) == 1:
        # Преобразуем фото с лицом в вектор, получаем embedding
        face_enc = face_recognition.face_encodings(face_array, face_locations)[0]
        # Получим вероятность предсказания
        predict_prob = model.predict_proba([face_enc])
        # Топ 5 актеров (индексы актеров)
        top_5 = predict_prob[0].argsort()[::-1][:5]
        # имена актеров
        top_5_actors_name = _get_key(dict_labels, top_5)
        # Вероятности топ 5 актеров
        top_5_prob = predict_prob[0][top_5].tolist()
        return top_5_actors_name, top_5_prob


def loaf_artifacts(folder, model, dict_labels):
    """
    :param folder: папка с файлами
    :param model: файл модели
    :param dict_labels: файл с актерами
    :return:
    """
    with open(Path(folder) / model, 'rb') as f:
        model = pickle.load(f)
    with open(Path(folder) / dict_labels, 'r') as f:
        dict_labels = json.load(f)
    return model, dict_labels


def normalize(probabilities):
    """
    :param probabilities: сырой список вероятностей
    :return: список приведенный к нормальному виду
    """
    sum_ = sum(probabilities)
    return list(map(lambda x: round(x / sum_ * 100, 1), probabilities))


def allowed_file(filename):
    """
    Проверка на валидность расширения файла
    :param filename: имя файла
    :return: bool
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
