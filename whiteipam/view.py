from ipaddress import ip_network
from flask import (
    Blueprint, render_template, redirect, url_for,
    session, request, current_app
)
from flask_login import (
    login_required, login_user, logout_user, current_user
)
from .forms import LoginForm, SubnetRegisterForm, HostRegisterForm
from .controllers import (
    authentication,
    create_network, get_network, get_network_list,
    create_host,
    NotExistError, AlreadyExistError, NetworkRangeError
)

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


@bp.route('/network/', methods=['GET'])
@login_required
def network():
    networks = get_network_list()
    return render_template('network_list.html', netwroks=networks)


@bp.route('/network/<int:id>/')
@login_required
def network_item(id):
    net = get_network(id)
    if net is not None:
        host_form = HostRegisterForm()
        message = session.pop('message', False)
        return render_template('network_item.html',
                               network=net,
                               host_form=host_form,
                               message=message)
    return redirect(url_for('root.network'))


@bp.route('/network/add/', methods=['GET', 'POST'])
@login_required
def add_network():
    form = SubnetRegisterForm()
    if form.validate_on_submit():
        net = create_network(
            ipv4=form.ipv4.data,
            name=form.name.data,
            vid=form.vid.data,
            note=form.note.data
        )
        if net is not None:
            return redirect(url_for('root.network_item', id=net.id))
        else:
            message = str(ip_network(form.ipv4.data, False)) + \
                'は既存のネットワークと重複しています。'
            return render_template('network_register.html',
                                   form=form, message=message)
    return render_template('network_register.html', form=form)


@bp.route('/host/add/', methods=['GET', 'POST'])
@login_required
def add_host():
    form = HostRegisterForm()
    if form.validate_on_submit():
        try:
            create_host(
                network_id=form.network_id.data,
                ipv4_address=form.ipv4_address.data,
                hostname=form.hostname.data,
                note=form.note.data
            )
        except (NotExistError, AlreadyExistError, NetworkRangeError) as e:
            session['message'] = str(e)
        return redirect(url_for('root.network_item', id=int(form.network_id.data)))
    return redirect(url_for('root.network'))
