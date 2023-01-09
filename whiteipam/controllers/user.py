from werkzeug.security import check_password_hash
from whiteipam.models import User


def authentication(username: str, password: str) -> User:
    """ユーザー名とパスワードが一致するUserを返す。
    該当するユーザーが存在しない場合はNoneを返す。
    """
    user = User.query.filter_by(username=username).one_or_none()
    if user is not None:
        if check_password_hash(user.password, password):
            return user
    return None
