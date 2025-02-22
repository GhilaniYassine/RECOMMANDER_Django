from django.shortcuts import render



def home(request):
    context = {"name":"yassine",
               "last_name":"Ghilani"}
    return render(request,"home.html",context)