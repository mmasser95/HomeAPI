from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    admin=db.Column(db.Boolean)
    password_hash = db.Column(db.String(128))
    typ=db.Column(db.String(10), default="user")
    grupo=db.Column(db.ForeignKey('grupo.id'))
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name!= 'password_hash'}
       
    def set_pass(self,p):
        self.password_hash=generate_password_hash(p)
    
    def check_pass(self,p):
        return check_password_hash(self.password_hash, p)


class Grupo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(64), index=True, unique=True)

    
class Perms(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    grupo=db.Column(db.Integer, db.ForeignKey('grupo.id'))
    recursoId=db.Column(db.Integer, db.ForeignKey('recurso.id'))
    view=db.Column(db.Boolean)
    opn=db.Column(db.Boolean)
    admn=db.Column(db.Boolean)
    
    def __repr__(self):
        return f'<Perms {self.userId} --> {self.recursoId}>'
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Recurso(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(64), nullable=False)
    userId=db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    permsId=db.Column(db.Integer, db.ForeignKey('perms.id'),nullable=False)
    tipo=db.Column(db.String(10), nullable=False)
    pin=db.Column(db.String(10),nullable=False)
    tActivo=db.Column(db.Float(10,2),nullable=False)
    password_hash=db.Column(db.String(128),nullable=False)
    def __repr__(self):
        return '<Recurso {}>'.format(self.nombre)
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name!= 'password_hash'}
       
    def set_pass(self,p):
        self.password_hash=generate_password_hash(p)
    
    def check_pass(self,p):
        return check_password_hash(self.password_hash, p)
