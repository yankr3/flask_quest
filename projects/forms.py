from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, SelectField, StringField
from wtforms.validators import InputRequired, Length


# Задаем секретный ключ
class BaseConfig:
    SECRET_KEY = "sdfksdfh6lks2jklb3nksd"
    BOOTSTRAP_SERVE_LOCAL = True
    DEBUG = False

# Форма приветствия
class StartForm(FlaskForm):
    gamer_name = StringField("Имя игрока", validators=[
        InputRequired(), Length(
            min=2,
            message="Хм, имя должно состоять хотя бы из 2х букв.")]
                             )
    start_button = SubmitField("Играем!")


# Финишная форма
class FinishForm(FlaskForm):
    finish_button = SubmitField("Вернуться на главную")


# Форма игры
class GameForm(FlaskForm):
    direction = SelectField(
        'Выберете направление для движения',
        coerce=int,
        choices=[
            (0, 'Север'),
            (1, 'Восток'),
            (2, 'ЮГ'),
            (3, 'Запад')
        ],
        render_kw={"class": "form-control"}
    )
    moves = IntegerField("Количество передвижений", render_kw={"class": "form-control"}, validators=[InputRequired()])
    move_button = SubmitField("Идти")