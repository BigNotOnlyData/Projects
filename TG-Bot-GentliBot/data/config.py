import json
import pickle
import re
import warnings
from pathlib import Path

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords


# версия библиотеки sklearn на которой обучалась модель - 0.24.2, в боте версия 1.0.2
warnings.filterwarnings('ignore')

# Константы путей
DIR_DATA = Path('data')
DIR_MODELS = Path('models')
DIR_INTENTS = Path('intents')
DIR_SOUNDS = Path('sounds')

VOICE_FILE_PATH = DIR_DATA / DIR_SOUNDS / 'voice.ogg'
AUDIO_FILE_PATH = DIR_DATA / DIR_SOUNDS / 'voice.wav'


################## Загрузка моделей ####################

with open(DIR_DATA / DIR_MODELS / 'intent_vectorizer.pkl', 'rb') as f:
    intent_vectorizer = pickle.load(f)

with open(DIR_DATA / DIR_MODELS / 'intent_model.pkl', 'rb') as f:
    intent_model = pickle.load(f)

with open(DIR_DATA / DIR_MODELS / 'toxic_vectorizer.pkl', 'rb') as f:
    toxic_vectorizer = pickle.load(f)

with open(DIR_DATA / DIR_MODELS / 'toxic_model.pkl', 'rb') as f:
    toxic_model = pickle.load(f)

with open(DIR_DATA / DIR_INTENTS / 'BOT_CONFIG_INTENTS.json', encoding='utf-8') as f:
    BOT_CONFIG = json.load(f)


################## Определение важных переменных ####################

BOT_TOKEN = ''
TOKEN_RE = re.compile(r'[а-яё]+')
STOPWORDS = stopwords.words("russian")

