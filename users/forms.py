
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = '__all__'
        exclude = ('groups','password','last_login','is_superuser','date_joined')