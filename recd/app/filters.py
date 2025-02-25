import django_filters
from django_filters.filters import  CharFilter
from .models import Course

class CourseFilter(django_filters.FilterSet):
    course_title = CharFilter(lookup_expr="icontains") # this if give us anything that contains that charcter
    # and ths is should be definded before Meta class but a question what is the meta calss 
    
    class Meta :    
        model = Course
        fields = ["course_title"] # now here it will just  exact search  by the title 