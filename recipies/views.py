from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import RegistrationForm, UpdateProfileForm, RecipeForm
from .models import Recipe
from django.shortcuts import get_object_or_404


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('recipies:index')
        else:
            messages.error(request, 'There was an error updating your profile. Please check the form and try again.')
    else:
        form = UpdateProfileForm(instance=request.user)
    return render(request, 'recipies/update_profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('recipies:index')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'recipies/change_password.html', {'form': form})

def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        # Get the username and password from the POST request
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        # If the user is authenticated, log them in and redirect to the homepage
        if user is not None:
            login(request, user)
            messages.success(request, 'logged in successfully.')
            return redirect('recipies:index')
        else:
            # If the user is not authenticated, display an error message
            messages.error(request, 'Invalid username or password.')
    # Render the login page
    return render(request, 'recipies/login.html', {'form': form})


#@login_required
def index(request):
    #newest_movies = Movie.objects.order_by('-release_date')[:15]
    #context = {'newest_movies': newest_movies}
    #return render(request, 'recipies/index.html',context)
    return render(request,'recipies/index.html')

# temporary view for display of 
#def recipe_view(request,id):
 #   return HttpResponse("<h1>%s</h1>" %id)

def register(request):
    if request.method == 'POST':
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            username = register_form.cleaned_data.get('username')
            raw_password = register_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            user.save()
            messages.success(request, 'Account created successfully.')
            login(request, user)
            return redirect('recipies:index')
        else:
             return HttpResponse("<h1> NOT DONE</h1>" )
    else:
        register_form = RegistrationForm()
    return render(request, 'recipies/register.html', {'register_form': register_form})

@login_required
def user_home(request):
    recipes = Recipe.objects.filter(owner=request.user)
    return render(request, 'recipies/user_home.html', {'recipes': recipes})

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.owner = request.user
            recipe.save()
            messages.success(request, 'Recipe added successfully.')
            return redirect('recipies:user_home')
    else:
        form = RecipeForm()
    return render(request, 'recipies/add_recipe.html', {'form': form})
    

@login_required
def recipe_view(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, owner=request.user)
    if request.method == 'GET':
        form = RecipeForm(instance=recipe)
        return render(request, 'recipies/recipe_view.html', {'recipe': recipe, 'form': form})
    else:
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recipe updated successfully.')
            return redirect('recipies:recipe_view', pk=recipe.pk)
        else:
            return render(request, 'recipies/recipe_view.html', {'recipe': recipe, 'form': form})

