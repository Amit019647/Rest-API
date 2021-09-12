from models.user import UserModel
from werkzeug.security import safe_str_cmp#for safe comaparision of strings

# these line of codes are used when there is no database i.e we store data in our in memory database
'''users=[User(1,'bob','asdf')]

# these mapping allow us to retrieve users bu id or username
username_mapping={ u.username: u for u in users}

userid_mapping={ u.id: u for u in users}'''


#tool functions
# 1. one function is going to authenticate our user(parameters==>username,password)

def authenticate(username,password):
    user=UserModel.find_by_username(username)
    # user=username_mapping.get(username,None)#this get method of dict helps to get the element and also set a default value
    if user and safe_str_cmp(user.password,password):
        return user

#2. identity function==>(payload => contents of the JWT token and we extract the user id from the payload
def identity(payload):
    user_id=payload['identity']
    return UserModel.find_by_id(user_id)



