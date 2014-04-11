from django.contrib.auth.forms import AuthenticationForm

from cityproblems.accounts.forms import RegisterUserForm


def get_auth_forms(request):
    if not request.user.is_authenticated():
        return dict(login_form=AuthenticationForm(), register_form=RegisterUserForm())
    return dict()
