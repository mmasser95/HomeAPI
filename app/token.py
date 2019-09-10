import json
from app import config
import jwt 
from math import trunc
from datetime import datetime, timedelta

class Token:
    def encode(self, userId, email, typ):
        exp=datetime.today() + timedelta(days=14)
        payload={
            'sub':userId,
            'email':email,
            'iat':trunc(datetime.today().timestamp()),
            'exp':trunc(exp.timestamp()),
            'type':typ
        }
        
        return jwt.encode(payload, config.Config.SECRET_KEY,algorithm='HS512').decode('utf-8')
    
    def decode(self,token):
        try:
            payload= jwt.decode(token, config.Config.SECRET_KEY,algorithm='HS512')
        except Exception as e:
             raise Exception('Fail to decode the token %s'%e)
        if(payload['exp'] < trunc(datetime.today().timestamp())):
             raise ValueError('Expired Token')
        return payload
        