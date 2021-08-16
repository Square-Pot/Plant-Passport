from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from .models import User


class UserCreateForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'password1', 'password2')
    