from hmac import compare_digest
from models.user import UserModel

def authenticate(username, password):
    """
    Function to authenticate a user (/auth endpoint).
    :param username: User's username in string format.
    :param password: User's un-encrypted password in string format.
    :return: A user if auth was successful.
    """
    user = UserModel.find_by_username(username)
    if user and compare_digest(user.password, password):
        return user

def identity(payload):
    """
    Function that gets called when user has already authenticated, and Flask-JWT
    verified their authorization header is correct.
    :param payload: A dictionary with 'identity' key, which is user_id
    :return: A UserModel object
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)