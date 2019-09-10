from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    admin=db.Column(db.Boolean)
    password_hash = db.Column(db.String(128))
    typ=db.Column(db.String(10), default="user")

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name!= 'password_hash'}
       
    def set_pass(self,p):
        self.password_hash=generate_password_hash(p)
    
    def check_pass(self,p):
        return check_password_hash(self.password_hash, p)

class Puerta(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(64))
    estado=db.Column(db.Boolean)
    pin=db.Column(db.Integer)
    userId=db.Column(db.Integer, db.ForeignKey('user.id'))
    password_hash=db.Column(db.String(128))

    def __repr__(self):
        return '<Puerta {}>'.format(self.nombre)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name!= 'password_hash'}
       
    def set_pass(self,p):
        self.password_hash=generate_password_hash(p)
    
    def check_pass(self,p):
        return check_password_hash(self.password_hash, p)
    
class Perms(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    userId=db.Column(db.Integer, db.ForeignKey('user.id'))
    puertaId=db.Column(db.Integer, db.ForeignKey('puerta.id'))
    view=db.Column(db.Boolean)
    opn=db.Column(db.Boolean)
    admn=db.Column(db.Boolean)
    
    def __repr__(self):
        return f'<Perms {self.userId} --> {self.puertaId}>'
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}