from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'users/sign_up.html', {'form': form})
    
def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Log the user in.
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('recipies:index')
    else:
        form = UserCreationForm()
    return render(request, 'users/sign_up.html', {'form': form})

def sign_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Log the user in.
            user = form.get_user()
            login(request, user)
            return redirect('recipies:index')
    else:
        form = AuthenticationForm()
    return render(request, 'users/sign_in.html', {'form': form})


def sign_out(request):
    logout(request)
    return render(request, 'users/sign_out.html')