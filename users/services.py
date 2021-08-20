from .models import User


def is_friend(user_requester, user_target):
    if user_requester in user_target.friends.all():
        return True
    else:
        return False