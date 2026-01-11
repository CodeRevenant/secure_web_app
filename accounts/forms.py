from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    captcha = CaptchaField() # Added for automated bot protection

    class Meta:
        model = User
        fields = ["username", "email"] # password1 and password2 are handled by UserCreationForm

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # Adds Bootstrap styling to all fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class SecureLoginForm(AuthenticationForm):
    captcha = CaptchaField()  # This line creates the field the template is looking for

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adds Bootstrap classes to all fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'