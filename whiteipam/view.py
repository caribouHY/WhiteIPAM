from flask import (
    Blueprint, render_template, redirect, url_for,
    session, request, current_app
)
from flask_login import (
    login_required, login_user, logout_user, current_user
)
from .forms import LoginForm
from .controllers import authentication

bp = Blueprint('root', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('index.html')


@bp.route('/logout')
@login_required
def logout():
    username = current_user.username
    logout_user()
    current_app.logger.info('User "{}" logout.'.format(username))
    return redirect(url_for('root.login'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('root.index'))

    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = authentication(form.username.data, form.password.data)
            if user is not None:
                login_user(user)
                current_app.logger.info(
                    'User "{}" login success.'.format(user.username))
                return redirect(url_for('root.index'))
        current_app.logger.info('login failure.')
        session['message'] = 'ユーザ－名またはパスワードが違います'
        return redirect(url_for('root.login'))

    message = session.pop('message', None)
    return render_template('login.html', form=form, message=message)
