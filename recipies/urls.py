"""project_recipies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""
# pylint: disable=C0103

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'recipies'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('user_home/', views.user_home, name='user_home'),
    path('recipe_update/<int:recipe_pk>/', views.recipe_update, name='recipe_update'),
    path('recipe_view/<int:recipe_pk>/', views.recipe_view, name='recipe_view'),
    path('recipe_delete/<int:recipe_pk>/', views.recipe_delete, name='recipe_delete'),
    path('recipes/<int:recipe_pk>/rate/', views.rate_recipe, name='rate_recipe'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
