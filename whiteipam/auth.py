from flask_login import LoginManager
from .models import User

login_manager = LoginManager()


def init_auth(app):
    login_manager.init_app(app)
    login_manager.login_view = 'root.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
