from django.shortcuts import render

def index(request):
    return render(request, 'interface1/interface.html')
