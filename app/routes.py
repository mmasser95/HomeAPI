from flask import request
from flask_restful import Resource, abort
from functools import wraps
from app import app, db, api
from app.models import User,Recurso,Perms,Grupo
from app.token import Token
localStorage={}

def isAuth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not "Authorization" in request.headers.keys():
            abort(401, message="Unauthorized")
        t=Token()
        try:
            localStorage['payload']=t.decode(request.headers['authorization'].split(' ')[1])
        except Exception as e:
            abort(500, message=e)
        except TypeError as e:
            abort(403, message=e)
        return func(*args, **kwargs)
    return wrapper

def isAdmin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not localStorage['payload']['type']=='admin':
            abort(401,message="Unauthorized")
        return func(*args, **kwargs)
    return wrapper


class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello World'}


class UserR(Resource):
    @isAuth
    @isAdmin
    def get(self, userId):
        try:
            u = User.query.get(int(userId))
        except Exception as e:
            abort(500, message="Error %s" % e)
        if not u:
            abort(404, message="El usuario no existe")
        return u.as_dict()
    @isAuth
    @isAdmin
    def post(self, userId):
        username = request.json['username']
        email = request.json['email']
        passw = request.json['passw']
        u = User(username=username, email=email)
        u.set_pass(passw)
        db.session.add(u)
        db.session.commit()
        return {'message': 'Success'}

    @isAuth
    @isAdmin
    def put(self, userId):
        pass


class LoginR(Resource):
    def post(self):
        print(request.json)
        email = request.json['email']
        passw = request.json['passw']
        t=Token()
        try:
            u = User.query.filter_by(email=email).first()
        except Exception as e:
            abort(500, message="Error %s" % e)
        if not u:
            abort(404,message="El usuario no existe")
        if not u.check_pass(passw):
            abort(401, message="La contraseña no es correcta")
        return {'message':'Success!', 'token':t.encode(u.id, u.email, u.typ)}
    
    @isAuth
    def get(self):
        t=Token()
        userId=localStorage['payload']['sub']
        try:
            u = User.query.get(userId)
        except Exception as e:
            abort(500, message="Error %s" % e)
        if not u:
            abort(404,message="El usuario no existe")
        return {'message':'Success!', 'token':t.encode(u.id, u.email, u.typ)}


class GrupoR(Resource):
    def get(self, grupoId):
        pass
    def post(self):
        pass
    def put(self, grupoId):
        pass
    def delete(self, grupoId):
        pass


class RecursoR(Resource):
    @isAuth
    def get(self, recursoId=False):
        userId=localStorage['payload']['sub']
        try:
            u=User.query.get(userId)
        except Exception as e:
            abort(500, message="Error %s" % e)
        if not u:
            abort(404,message="El usuario no existe")
        try:
            if not recursoId:
                p=Recurso.query.filter_by(userId=userId)
            else:
                p=Recurso.query.filter_by(userId=userId, id=recursoId).first()
        except Exception as e:
            abort(500, message="Error %s" % e)
        if not p:
            abort(404,message="El objeto no existe")
        if not recursoId:
            return {'message':'Success', 'data':[i.as_dict() for i in p ]}
        else:
            return {'message':'Success', 'data':p.as_dict()}
    
    @isAuth
    def post(self):
        userId=localStorage['payload']['sub']
        nombre = request.json['nombre']
        permsId=request.json['permsId']
        tipo=request.json['tipo']
        tActivo=request.json['tActivo']
        passw=request.json['passw']
        pin=request.json['pin']
        p=Recurso(userId=userId, nombre=nombre, tipo=tipo,pin=pin, tActivo=tActivo, permsId=permsId)
        p.set_pass(passw)
        try:
            db.session.add(p)
            db.session.commit()
        except Exception as e:
            abort(500, message=f'Error: {e}')
        return {'message':'Success!'}
    
    @isAuth
    def patch(self, recursoId):
        passw=request.json['passw']
        if not recursoId:
            abort(404, message="Debes ingresar una ID")
        userId=localStorage['payload']['sub']
        try:
            p=Recurso.query.filter_by(userId=userId, id=recursoId)
        except Exception as e:
            abort(500, message=f"Error {e}")
        if not p:
            abort(404, message="El recurso no existe")
        if not p.check_pass(passw):
            abort(401, 'Unauthorized')
        try:
            pass
        except Exception as e:
            abort(500, message=f'Error {e}')
        return {'message': 'Success'}

    def put(self, recursoId):
        pass

    @isAuth
    def delete(self, recursoId):
        userId=localStorage['payload']['sub']
        try:
            u=User.query.get(userId)
        except Exception as e:
            abort(500, message="Error %s" % e)
        if not u:
            abort(404,message="El usuario no existe")
        try:
            if not recursoId:
                p=Recurso.query.filter_by(userId=userId)
            else:
                p=Recurso.query.filter_by(userId=userId, id=recursoId).first()
        except Exception as e:
            abort(500, message="Error %s" % e)
        if not p:
            abort(404,message="El objeto no existe")
        try:
            if not recursoId:
                for i in p:
                    db.session.delete(i)
            else:
                db.session.delete(p)
            db.session.commit()
        except Exception as e:
            abort(500, message=f"Error: {e}")
        return {'message':'Success!'}


class PermsR(Resource):
    @isAuth
    def get(self, recursoId):
        userId=localStorage['payload']['sub']
        try:
            if not recursoId:
                pm=Perms.query.filter_by(userId=userId)
            else:
                pm=Perms.query.filter_by(userId=userId,recursoId=recursoId)
        except Exception as e:
            abort(500, message=f"Error {e}")
        if not pm:
            abort(404, message="No hay permisos")
        return {'message':'Success!', 'data':[i.as_dict() for i in pm]}

    @isAuth
    @isAdmin
    def post(self):
        pass
    
    @isAuth
    @isAdmin
    def put(self, recursoId):
        pass
    
    @isAuth
    @isAdmin
    def delete(self, recursoId):
        userId=localStorage['payload']['sub']
        if not recursoId:
            abort(400, message='Bad Request')
        try:
            pm=Perms.query.filter_by(userId=userId, recursoId=recursoId).first()
        except Exception as e:
            abort(500, message=f'Error {e}')
        if not pm:
            abort(404, message='No existen permisos previos')
        try:
            db.session.delete(pm)
            db.session.commit()
        except Exception as e:
            abort(500,message=f'Error {e}')
        return {'message': 'Success!'}

api.add_resource(HelloWorld, '/')
api.add_resource(UserR, '/user/<string:userId>', '/user')
api.add_resource(LoginR, '/login')
api.add_resource(RecursoR, '/recurso/<string:recursoId>', '/recurso')
api.add_resource(PermsR, '/perms/<string:recursoId>', '/perms')
api.add_resource(GrupoR, '/grupo/<string:grupoId>', '/grupo')
