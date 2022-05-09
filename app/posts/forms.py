from wtforms import Form, StringField, TextAreaField, SubmitField, EmailField, PasswordField, BooleanField
from wtforms.validators import DataRequired


class PostForm(Form):
    title = StringField('Заголовок')
    body = TextAreaField('Содержание')
    submit = SubmitField('Создать')


class SearchForm(Form):
    text = StringField("Введите текст")
    submit = SubmitField("Поиск")
