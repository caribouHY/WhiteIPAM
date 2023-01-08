from flask import (
    Blueprint, render_template, redirect, url_for, session)
from flask_login import (
    UserMixin, login_required, login_user, logout_user, current_user
)
from werkzeug.security import check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from whiteipam.database import db

bp = Blueprint('root', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('index.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('root.login'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('root.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one_or_none()
        if user is not None and \
                check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('root.index'))
        else:
            session['message'] = 'ユーザ－名またはパスワードが違います'
            return redirect(url_for('root.login'))

    if 'message' in session:
        message = session['message']
        session.pop('message')
        return render_template('login.html', form=form, message=message)
    return render_template('login.html', form=form)


class LoginForm(FlaskForm):
    username = StringField(
        'ユーザー名',
        validators=[DataRequired(), Length(min=4, max=32)])
    password = PasswordField('パスワード', validators=[DataRequired()])
    submit = SubmitField('ログイン')


class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)