from werkzeug.security import safe_str_cmp # sicher bei verschiedenen python versionen
from models.user import UserModel #importiert aus dem file user.py die Klasse User


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password,password):
        return user

def identity(payload): #payload is the content of the JWT token, identity is unique to flask jwt - jason web token
    user_id = payload['identity'] #extract user id from that payload
    return UserModel.find_by_id(user_id) # retrieve specific user who matches

#auth endpoint returns a jwt token
