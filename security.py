from modules.user import UserModel
from werkzeug.security import safe_str_cmp
"""
users = [
    User(1, 'Bob', 'asdf')
]

username_mapping = {u.username: u for u in users}

userid_mapping = {u.id: u for u in users}
"""

def authenticate(username, password):
    # user = username_mapping.get(username, None)
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user 

def identity(payload):
    userid = payload['identity']
    # return userid_mapping.get(userid, None)
    return UserModel.find_by_id(userid)
