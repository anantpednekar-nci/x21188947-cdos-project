"""views configs for app."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms import RegistrationForm, UpdateProfileForm, RecipeForm
from .models import Recipe, RecipeRating


def logout_view(request):
    """Logout View"""
    logout(request)
    messages.success(request, 'logged out successfully.')
    return redirect('recipies:index')


@login_required
def update_profile(request):
    """View to allow users to update their profile information."""
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('recipies:user_home')
        messages.error(request, 'There was an error updating your profile.')
    else:
        form = UpdateProfileForm(instance=request.user)
    return render(request, 'recipies/update_profile.html', {'form': form})


@login_required
def change_password(request):
    """Change password view."""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('recipies:user_home')
        messages.error(request, 'There was an error updating your password.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'recipies/change_password.html', {'form': form})


def login_view(request):
    """Login view."""
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
            return redirect('recipies:user_home')
        # If the user is not authenticated, display an error message
        messages.error(request, 'Invalid username or password.')
    # Render the login page
    return render(request, 'recipies/login.html', {'form': form})


def index(request):
    """Index view."""
    recipes = Recipe.objects.all()
    context = {'recipes': recipes}
    return render(request, 'recipies/index.html', context)


def register(request):
    """register view."""
    if request.method == 'POST':
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            username = register_form.cleaned_data.get('username')
            raw_password = register_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            user.save()
            messages.success(request, 'Account created successfully.')
            #login(request, user)
            return redirect('recipies:index')
        messages.error(request, 'Error while registering')
    else:
        register_form = RegistrationForm()
    return render(request, 'recipies/register.html', {'register_form': register_form})


@login_required
def user_home(request):
    """user_home view."""
    recipes = Recipe.objects.all()
    return render(request, 'recipies/user_home.html', {'recipes': recipes})


@login_required
def add_recipe(request):
    """add_recipe view."""
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.owner = request.user
            recipe.save()
            messages.success(request, 'Recipe added successfully.')
            return redirect('recipies:user_home')
    form = RecipeForm()
    return render(request, 'recipies/add_recipe.html', {'form': form})


def recipe_view(request, recipe_pk):
    """ recipe view"""
    recipe = get_object_or_404(Recipe, pk=recipe_pk)
    return render(request, 'recipies/recipe_view.html', {'recipe': recipe})


@login_required
def recipe_update(request, recipe_pk):
    """ recipe view"""
    recipe = get_object_or_404(Recipe, pk=recipe_pk, owner=request.user)
    form = RecipeForm(request.POST or None, request.FILES or None, instance=recipe)
    if form.is_valid():
        form.save()
        messages.success(request, 'Recipe updated successfully.')
        return redirect('recipies:recipe_view', pk=recipe.pk)
    return render(request, 'recipies/recipe_update.html', {'form': form})


@login_required
def recipe_delete(request, recipe_pk):
    """ recipe_delete view"""
    recipe = get_object_or_404(Recipe, pk=recipe_pk, owner=request.user)
    recipe.delete()
    messages.success(request, 'Recipe deleted successfully.')
    return redirect('recipies:user_home')


@require_POST
def rate_recipe(request, recipe_pk):
    """ rate_recipe view"""
    recipe = get_object_or_404(Recipe, pk=recipe_pk)
    rating = int(request.POST.get('rating'))
    if recipe.owner != request.user:
        user_rating, created = RecipeRating.objects.get_or_create(user=request.user, recipe=recipe)
        user_rating.rating = rating
        if created:
            messages.success(request, 'You have successfully rated this recipe!')
        user_rating.save()
    return redirect('recipies:user_home')
    