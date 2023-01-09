from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField(
        'ユーザー名',
        validators=[DataRequired(), Length(max=32)])
    password = PasswordField(
        'パスワード',
        validators=[DataRequired(), Length(max=32)])
    submit = SubmitField('ログイン')
