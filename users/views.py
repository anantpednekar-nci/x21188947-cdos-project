from django.shortcuts import render
from django.http import HttpResponse

def sign_in(request):
    return HttpResponse("You're at the Login Page.")

def sign_up(request):
    return HttpResponse("You're at the Sign up Page.")