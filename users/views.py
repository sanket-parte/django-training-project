from django.shortcuts import render, redirect
from users.models import Profile
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.forms import CustomUserCreationForm


# Create your views here.

@login_required(login_url='user-login')
def get_profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles':profiles}
    return render(request,'profiles.html', context)

def user_login(request):
    
    if request.user.is_authenticated:
        return redirect('get-projects')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            return render(request, 'user_login.html')
        user = authenticate(username=username,password=password)
        if user:
            login(request, user)
            
            messages.success(request, 'User logged in successfully')
            return redirect('get-projects')
        else:
            messages.info(request, 'Enter correct username and password')
        
    return render(request, 'user_login.html')

def user_logout(request):
    logout(request)
    return redirect('user-login')

def create_user(request):
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, name=user.first_name+' '+user.last_name, \
                                   username=user.username)
            if request.POST.get('user_permissions'):
                request_data = request.POST
                user.user_permissions.set(request_data.getlist('user_permissions'))
                user.save()
                                 
            messages.success(request,'User created successfully.')
            return redirect('user-login')
        else:
            messages.error(request,'User creation failed.')
    
    context = {'form':form}
    return render(request, 'create_user.html', context)
