from flask_login import UserMixin
from .database import db


class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)


class Network(db.Model):

    __tablename__ = 'network'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    vid = db.Column(db.Integer)
    ipv4_address = db.Column(db.String(16), nullable=False)
    ipv4_prefix = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String(64))

    def __init__(self, ipv4_address: str, ipv4_prefix: int,
                 name: str, vid: int, note: str) -> None:
        super().__init__()
        self.name = name
        self.ipv4_address = ipv4_address
        self.ipv4_prefix = ipv4_prefix
        self.vid = vid
        self.note = note

    def get_ipv4cidr(self) -> str:
        return '{}/{}'.format(self.ipv4_address, self.ipv4_prefix)


class Host(db.Model):

    __tablename__ = 'hosts'

    id = db.Column(db.Integer, primary_key=True)
    network_id = db.Column(db.Integer, db.ForeignKey("network.id"))
    hostname = db.Column(db.String(64))
    ipv4_address = db.Column(db.String(16), nullable=False, unique=True)
    note = db.Column(db.String(64))

    def __init__(self, network_id: str, ipv4_address: str,
                 hostname: str = None, note: str = None) -> None:
        super().__init__()
        self.network_id = network_id
        self.hostname = hostname
        self.ipv4_address = ipv4_address
        self.note = note
