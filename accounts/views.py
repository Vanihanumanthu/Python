
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email    = request.POST['email']
        password = request.POST['password']
        confirm  = request.POST['confirm']

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('dashboard')

    return render(request, 'accounts/register.html')

    if request.user.is_authenticated:
      return redirect('home')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')  # ✅ Redirect to home after login
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'accounts/login.html')



def logout_view(request):
    logout(request)
    return redirect('login')
