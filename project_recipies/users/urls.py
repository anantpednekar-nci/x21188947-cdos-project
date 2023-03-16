from django.urls import path
from . import views
app_name = 'users'
urlpatterns = [
 path('sign_up/', views.sign_up, name='sign_up'),
 path('sign_in/', views.sign_in, name='sign_in'),
 
]

"""

app_name = "user_app"
urlpatterns = [

path('profile/', views.profile, name='profile'),
path('password/', views.password, name='password'),
path('connections/', views.connections, name='connections'),
path('delete/', views.delete, name='delete'),

]
"""