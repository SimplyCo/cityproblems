def is_admin(user):
    if user.is_authenticated():
        return user.is_staff
    else:
        return False