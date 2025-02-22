from django.db import models
from datetime import datetime

class Course(models.Model):

        
    LEVELS= [
                ("ALL Levels","ALL Levels"),
                ("Intermidate level","Intermidate level"),
                ("Beginner level","beginners level"),
                ("Expert level")
        ]
    Subjects = [
                ("Business Fianace"," Business Fianace"),
                ("Graphic Design","Graphic Design"),
                ("Musical Instruments","Musical Instruments")
                ("Web Development","Web Development"),


        ]
        
    course_id = models.IntegerField(blank=True, null=True)
    course_title = models.CharField(max_length=1000,blank=True)
    url = models.URLField(null = True,blank=True , max_length=1000)
    is_paid = models.CharField(null=True,blank=True,max_length=1000)
    price = models.CharField(null=True,blank=True,max_length=1000)
    subscribers = models.IntegerField(blank=True,null=True)
    num_lectures = models.IntegerField(blank=True,null= True)
    reviews = models.IntegerField(blank=True,null= True)
    level =models.CharField(max_length=100,blank=True , null=True , choices=LEVELS)
    content_durations = models.CharField(max_length=100, blank=True,null=True)
    subjects = models.CharField(max_length=100,blank=True,null=True,choices=Subjects)
    published_timestamp  = models.CharField(max_length=1000,blank=True , null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)


    @property 
    def published_on(self):
        date_format= "%Y-%m-%dT:%M:%SZ"
        datetime_object = datetime.strptime(self.published_timestamp,date_format)
        return datetime_object

