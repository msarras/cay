import os
from django.shortcuts import render
from dotenv import load_dotenv

load_dotenv()

def home(request):
    email = os.environ.get('EMAIL', None)
    context = {
        'email': email,
    }
    return render(request, 'home.html', context)
