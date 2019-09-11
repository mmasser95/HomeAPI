from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    typ = db.Column(db.String(10), default="user")

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def as_dict(self):
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns if c.name != 'password_hash'
        }

    def set_pass(self, p):
        self.password_hash = generate_password_hash(p)

    def check_pass(self, p):
        return check_password_hash(self.password_hash, p)


class UserPermsRecurso(db.Model):
    userId = db.Column(db.ForeignKey('user.id'), primary_key=True)
    permsId = db.Column(db.ForeignKey('perms.id'), nullable=False)
    recursoId = db.Column(db.ForeignKey('recurso.id'), primary_key=True)

    def __repr__(self):
        return f'<User  {self.userId} --> Perms {self.permsId} --> Recurso {self.recursoId}>'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Perms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    view = db.Column(db.Boolean, nullable=False)
    opn = db.Column(db.Boolean, nullable=False)
    admn = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Perms {self.userId}>'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Recurso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.ForeignKey('user.id'))
    nombre = db.Column(db.String(64), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)
    pin = db.Column(db.String(10), nullable=False)
    tActivo = db.Column(db.Float(10, 2), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<Recurso {}>'.format(self.nombre)

    def as_dict(self):
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns if c.name != 'password_hash'
        }

    def set_pass(self, p):
        self.password_hash = generate_password_hash(p)

    def check_pass(self, p):
        return check_password_hash(self.password_hash, p)
