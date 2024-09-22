from django.db import models

# Create your models here.
class Data(models.Model): 
    Name = models.CharField(max_length=100)  
    Password = models.CharField(max_length=123)


    