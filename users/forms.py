from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from event.forms import CreateEventMixin
class RegisterForm(CreateEventMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name' ,'username', 'password1', 'password2', 'email']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.apply_form_style()

        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = None

class LoginForm(CreateEventMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_form_style()