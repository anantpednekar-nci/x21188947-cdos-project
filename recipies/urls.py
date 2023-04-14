from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

app_name = 'recipies'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('change_password/', views.change_password, name='change_password'),
    
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    #path('update_recipe/<int:pk>/', views.update_recipe, name='update_recipe'),
    #path('delete_recipe/<int:pk>/', views.delete_recipe, name='delete_recipe'),
    path('user_home/', views.user_home, name='user_home'),
    
    path('recipe_update/<int:pk>/', views.recipe_update, name='recipe_update'),
    path('recipe_view/<int:pk>/', views.recipe_view, name='recipe_view'),
    path('recipe_delete/<int:pk>/', views.recipe_delete, name='recipe_delete'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)