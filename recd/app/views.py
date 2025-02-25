from django.shortcuts import render
from .models import Course
from .filters import CourseFilter
from django.core.paginator import Paginator
from .forms import  RecommenderForm 

def home(request):
    courses = Course.objects.all()
    search_filter = CourseFilter(request.GET,queryset=courses)
    courses = search_filter.qs
    search_term = request.GET.get("course_title","")

    paginator =  Paginator(courses,25) 
    page_number = request.GET.get( 'page')
    page_obj = paginator.get_page(page_number   )
    context = {
        "name": "yassine",
        "last_name": "Ghilani",
        "courses": courses  # Correct variable name (plural) # don't forget to to add the search_filter context to render it on the html  page to the 
        ,"search_filter":search_filter,
        "page_obj":page_obj ,
         "search_term":search_term }
    return render(request, "home.html", context)

def read_course(request, pk):
    course = Course.objects.get(pk=pk)  # Fetch a single course by its primary key
    context = {'course': course}
    return render(request, 'read_course.html', context)

def recommend_view(request):
    if request.method == "POST":
        form = RecommenderForm(data=request.POST)
        if form.is_valid():
            search_term = form.cleaned_data["search_term"]
            # vectorized the search term
            # search the VectDB and get recommendation
            context = {"result": search_term.title(), "form": form, "search_term": search_term}
            return render(request, "recommended.html", context)
    else:
        form = RecommenderForm()
        context = {"form": form}
        return render(request, "recommended.html", context)
    