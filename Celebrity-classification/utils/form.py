from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed

from utils import ALLOWED_EXTENSIONS

error = f"Неверный формат файла. Валидные форматы: ({', '.join(ALLOWED_EXTENSIONS)})"


class DownloadFrom(FlaskForm):
    image_file = FileField("Загрузи фото с одним лицом",
                           validators=[FileRequired(), FileAllowed(ALLOWED_EXTENSIONS, error)]
                           )

