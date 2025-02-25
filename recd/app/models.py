from django.db import models
from datetime import datetime

from django.db import models

class Course(models.Model):
    LEVELS = [
        ("ALL Levels", "ALL Levels"),
        ("Intermediate level", "Intermediate level"),
        ("Beginner level", "Beginner level"),
        ("Expert level", "Expert level"),
    ]

    SUBJECTS = [
        ("Business Finance", "Business Finance"),
        ("Graphic Design", "Graphic Design"),
        ("Musical Instruments", "Musical Instruments"),
        ("Web Development", "Web Development"),
    ]

    level = models.CharField(max_length=20, choices=LEVELS)
    subject = models.CharField(max_length=50, choices=SUBJECTS)

        
    course_id = models.IntegerField(blank=True, null=True)
    course_title = models.CharField(max_length=1000,blank=True)
    url = models.URLField(null = True,blank=True , max_length=1000)
    is_paid = models.CharField(null=True,blank=True,max_length=1000)
    price = models.CharField(null=True,blank=True,max_length=1000)
    num_subscribers = models.IntegerField(blank=True,null=True)
    num_lectures = models.IntegerField(blank=True,null= True)
    num_reviews = models.IntegerField(blank=True,null= True)
    level =models.CharField(max_length=100,blank=True , null=True , choices=LEVELS)
    content_duration = models.CharField(max_length=100, blank=True,null=True)
    subject = models.CharField(max_length=100,blank=True,null=True,choices=SUBJECTS)
    published_timestamp  = models.CharField(max_length=1000,blank=True , null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)


    @property 
    def published_on(self):
        date_format= "%Y-%m-%dT:%M:%SZ"
        datetime_object = datetime.strptime(self.published_timestamp,date_format)
        return datetime_object

