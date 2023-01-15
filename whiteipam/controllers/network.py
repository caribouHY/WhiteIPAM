from ipaddress import ip_network
from flask import current_app
from sqlalchemy import asc
from whiteipam.database import db
from whiteipam.models import Network


def create_network(ipv4: str, name: str = None,
                   vid: int = None, note: str = None) -> Network:
    v4net = ip_network(ipv4, False)
    net_max = str(v4net)[:str(v4net).find('.')+1]
    net_min = ''
    for s in str(v4net).split('.')[:int(v4net.prefixlen/8)]:
        net_min += s + '.'
    supernets = db.session.execute(
        db.select(Network).filter(
            Network.ipv4_address.like(net_max+'%'),
            Network.ipv4_prefix > v4net.prefixlen)
    ).scalars().all()

    subnets = db.session.execute(
        db.select(Network).filter(
            Network.ipv4_address.like(net_min+'%'),
            Network.ipv4_prefix <= v4net.prefixlen)
    ).scalars().all()

    for supernet in supernets:
        s = supernet.ipv4_address+'/'+str(supernet.ipv4_prefix)
        if (v4net.subnet_of(ip_network(s))):
            return None

    for subnet in subnets:
        s = subnet.ipv4_address+'/'+str(subnet.ipv4_prefix)
        if (v4net.subnet_of(ip_network(s))):
            return None

    network = Network(
        ipv4_address=str(v4net.network_address),
        ipv4_prefix=v4net.prefixlen,
        vid=vid,
        name=name,
        note=note
    )
    db.session.add(network)
    db.session.commit()
    current_app.logger.debug(
        'created network (id={} name={} ipv4={})'.format(
            network.id, network.name, network.get_ipv4cird()))
    return network


def get_network(id: int) -> Network:
    return db.session.execute(
        db.select(Network).filter(Network.id == id)
    ).scalars().one_or_none()


def get_network_list():
    return db.session.execute(
        db.select(Network).order_by(asc(Network.ipv4_address))
    ).scalars().all()
