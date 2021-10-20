from django.contrib import admin
from .models import BookRecord, Recommendation, Book, Author, Student, Administrator, Subject
# Register your models here.
admin.site.register(Recommendation)
admin.site.register(Book)
admin.site.register(BookRecord)
admin.site.register(Author)
admin.site.register(Student)
admin.site.register(Administrator)
admin.site.register(Subject)
