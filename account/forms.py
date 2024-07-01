from django.forms import ModelForm

from .models import MyUser


class RegisterForm(ModelForm):
    class Meta:
        model = MyUser
        fields = ['email', 'password', 'username']
