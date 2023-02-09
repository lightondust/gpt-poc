from utils import load_json


def user_table(user):
    return load_json('./config/users.json').get(user)


def check_user(user, password):
    if user_table(user) == password:
        return True
    else:
        return False
