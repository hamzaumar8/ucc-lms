from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.fields.related import ForeignKey
# Create your models here.

class Subject(models.Model):
    name = models.CharField(unique=True, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length = 255, blank=False, null=False)
    publisher = models.CharField(max_length = 255, blank=True, null=True)
    availability = models.IntegerField(default=0, blank=True, null=True)
    year = models.CharField(max_length = 4, blank=True, null=True)
    author = models.CharField(max_length = 255, blank=True, null=True)
    location = models.CharField(max_length = 255, blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='booksubject')
    
    def __str__(self):
        return self.title



class Recommendation(models.Model):
    book_name = models.CharField(max_length = 255, blank=False, null=False)
    description = models.TextField(max_length = 255, blank=True, null=True)
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.book_name
    
    
class BookRecord(models.Model):
    book = ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    date_of_issue = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(blank=True, null=True)
    date_of_return = models.DateTimeField(null=True, blank=True)
    dues = models.IntegerField(null=True, blank=True, default=0 )
    renewals_left = models.IntegerField(null=True, blank=True, default=0 )
   
    def __str__(self):
        returnee = str(self.book)
        return returnee
    
    
class Student(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    index_number = models.CharField(max_length=20, blank=True, null=True)
    profile_pic = models.ImageField(blank=True, null=True)
    
    def __str__(self):
        return self.user.email


def student_receiver(sender, instance, created, *args, **kwargs):
    if created:
        print('checK', instance.id)
        student = Student.objects.create(user=instance)

post_save.connect(student_receiver, sender=User)    
    
class Administrator(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, blank=True, null=True)
    profile_pic = models.ImageField(blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
    

class Author(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    
    def __str__(self):
        return self.name
    