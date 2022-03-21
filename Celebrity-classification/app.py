# flask туториалы
# https://flask-russian-docs.readthedocs.io/ru/latest/quickstart.html
# https://pythonru.com/uroki/11-rabota-s-formami-vo-flask
# Загрузка файлов: https://flask-russian-docs.readthedocs.io/ru/latest/patterns/fileuploads.html
# Формы: https://flask-wtf.readthedocs.io/en/0.15.x/form/
# Сессия: https://russianblogs.com/article/8457990186/
# Шаблонизатор: https://jinja.palletsprojects.com/en/2.10.x/templates/#sort
# Фронт: https://getbootstrap.com/


from flask import Flask, render_template
from utils import predict_actors, loaf_artifacts, normalize, \
    ARTIFACTS_FOLDER, ACTORS, MODEL, SECRET_KEY, DownloadFrom


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

model, dict_labels = loaf_artifacts(ARTIFACTS_FOLDER, MODEL, ACTORS)

# главная страница
@app.route('/home/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    fail = None
    form = DownloadFrom()
    if form.validate_on_submit():
        file = form.image_file.data
        res = predict_actors(file.stream, model, dict_labels)
        if res:
            predict = list(zip(res[0], normalize(res[1])))
            return render_template("base.html", form=form, predict=predict)
        else:
            fail = 'Лицо не было распознано'

    return render_template("base.html", form=form, fail=fail)


# Инфо
@app.route('/info/')
def info():
    return render_template("info.html")


if __name__ == "__main__":
    app.run()
