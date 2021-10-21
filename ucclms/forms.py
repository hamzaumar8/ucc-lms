from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Book, BookRecord, Recommendation, Student, Subject
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2', 'first_name', 'last_name'
        ]

class AddBookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class AddSubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'

class BorrowBookForm(ModelForm):
    class Meta:
        model = BookRecord
        fields = '__all__'


class AlterBookRecord(ModelForm):
    class Meta:
        model = BookRecord
        fields = '__all__'


class RecommendBookForm(ModelForm):
    class Meta:
        model = Recommendation
        fields = '__all__'

class EditStudentProfile(ModelForm):
    class Meta:
        model = Student
        fields = [ 'index_number', 'profile_pic',]

class CreateStudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'