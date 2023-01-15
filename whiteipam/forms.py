from ipaddress import AddressValueError, IPv4Network, NetmaskValueError
from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField,
    PasswordField, SubmitField, HiddenField,
    ValidationError
)
from wtforms.validators import (
    DataRequired, Optional,
    NumberRange, Length,
    IPAddress
)


def ipv4cidr_private_check(form, field):
    try:
        v4net = IPv4Network(field.data, False)
        if v4net.is_private is False:
            raise ValidationError('Addrress is not private.')
    except AddressValueError:
        raise ValidationError('Addrress is invailed.')
    except NetmaskValueError:
        raise ValidationError('Netmask is invailed.')


def id_check(form, field):
    if int(field.data) < 1:
        raise ValidationError('Value is ivailed.')


class LoginForm(FlaskForm):
    username = StringField(
        'ユーザー名',
        validators=[DataRequired(), Length(max=32)])
    password = PasswordField(
        'パスワード',
        validators=[DataRequired(), Length(max=32)])
    submit = SubmitField('ログイン')


class SubnetRegisterForm(FlaskForm):
    name = StringField(
        '名前',
        validators=[Optional(), Length(max=32)]
    )
    vid = IntegerField(
        'VLAN ID',
        validators=[Optional(), NumberRange(min=0, max=4096)]
    )
    ipv4 = StringField(
        'IPv4 (CIDR)',
        validators=[DataRequired(),
                    ipv4cidr_private_check]
    )
    note = StringField(
        'メモ',
        validators=[Optional(), Length(max=64)]
    )
    submit = SubmitField('登録')


class HostRegisterForm(FlaskForm):
    network_id = HiddenField(
        validators=[DataRequired(), id_check]
    )
    hostname = StringField(
        'ホスト名',
        validators=[Optional(), Length(max=63)]
    )
    ipv4_address = StringField(
        'IPv4アドレス',
        validators=[DataRequired(), IPAddress(ipv4=True, ipv6=False)]
    )
    note = StringField(
        'メモ',
        validators=[Optional(), Length(max=64)]
    )
    submit = SubmitField('作成')
