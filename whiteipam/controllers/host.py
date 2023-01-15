from flask import current_app
from whiteipam.database import db
from whiteipam.models import Host
import ipaddress
from .network import get_network
from .error import NotExistError, AlreadyExistError


def create_host(network_id: int, ipv4_address: str,
                hostname: str = None, note: str = None) -> Host:
    network = get_network(network_id)
    if network is None:
        current_app.logger.warning(
            'Network(id:{}) is not exists.'.format(network_id))
        raise NotExistError('指定されたネットワークが存在しません。')

    net = ipaddress.IPv4Network(network.get_ipv4cidr())
    ip = ipaddress.IPv4Network(ipv4_address + '/32', False)

    if ip.subnet_of(net) is False:
        current_app.logger.warning(
            '{} is out of range for {}.'.format(ip.network_address, net))
        raise ValueError('指定されたIPv4アドレスはネットワークの範囲外です。')

    if db.session.execute(
        db.select(Host).filter(Host.ipv4_address == str(ip.network_address))
    ).scalars().one_or_none() is not None:
        current_app.logger.info(
            '{} already exists.'.format(ip.network_address))
        raise AlreadyExistError('指定されたIPv4アドレスのホストが存在します。')

    host = Host(
        ipv4_address=str(ip.network_address),
        network_id=network.id,
        hostname=hostname,
        note=note
    )
    db.session.add(host)
    db.session.commit()
    return host
