from django.shortcuts import render
from .models import Course

def home(request):
    courses = Course.objects.all()
    context = {
        "name": "yassine",
        "last_name": "Ghilani",
        "courses": courses  # Correct variable name (plural)
    }
    return render(request, "home.html", context)