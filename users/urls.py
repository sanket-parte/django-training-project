
from django.urls import path
from users.views import get_profiles, user_login, user_logout, create_user

urlpatterns = [
    path('', get_profiles, name='get-profiles'),
    path('user-login', user_login, name='user-login'),
    path('user-logout', user_logout, name='user-logout'),
    path('create-user', create_user, name='create-user'),
]
