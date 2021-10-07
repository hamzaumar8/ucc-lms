import time
from django.contrib.auth import forms
from django.contrib.auth.models import User, Group
from django.contrib.messages.api import error
from django.forms.forms import Form
from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BorrowBookForm, CreateStudentForm, CreateUserForm, AddBookForm, AlterBookRecord, EditStudentProfile, RecommendBookForm, BorrowBookForm
from .models import *
from .decorators import unauthenticated_user, allowed_users
from datetime import datetime, timedelta


def home(request):
    return render(request, 'ucclms/home.html')

@unauthenticated_user
def signIn(request):
    users = User.objects.all()
    datadict={
        'user': users.last()
        }
    studCreate = CreateStudentForm(datadict)
    # print(users[len(users)-1])
    if request.method == 'POST':
        studCreate = CreateStudentForm(request.POST, datadict)
        if studCreate.is_valid():
            studCreate.save()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
            
        if user is not None:
            login(request, user)
            user_group = request.user.groups.all()[0].name
            print(user_group)
            if 'admin' in user_group:          
                return redirect('admin-dashboard')
            elif 'student' in user_group:          
                return redirect('student-dashboard')
            else:       
                print(f'User groups: {user_group}')
        else:
            messages.info(request, 'WRONG USERNAME AND/OR PASSWORD')


    context = {'studCreate': studCreate}
    return render(request, 'ucclms/login.html', context)


def signOut(request):
    logout(request)
    return redirect('login')

@allowed_users(allowed_roles=['student'])
def studentDashboard(request):
    student = Student.objects.get(user=request.user)
    context = {'student': student}
    return render(request, 'ucclms/student-dashboard.html', context)

@allowed_users(allowed_roles=['admin'])
def adminDashboard(request):
    admin = Administrator.objects.get(user=request.user)
    context = {'admin': admin}
    return render(request, 'ucclms/admin-dashboard.html', context)


@unauthenticated_user
def signUp(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='student')
            user.groups.add(group)
            messages.success(request, f'Account created for {username}')
 
            return redirect('login')
    context = {'form': form}
    return render(request, 'ucclms/sign-up.html', context)


@allowed_users(allowed_roles=['admin'])
def createUser(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'{user} has been added successfully')
            return redirect('view-users')
    context = {'form': form}
    return render(request, 'ucclms/create-user.html', context)


@allowed_users(allowed_roles=['admin'])
def deleteUser(request, pk):
    user = User.objects.get(id=pk)

    if request.method == "POST":
        user.delete()
        messages.success(request, f'{user} has been deleted successfully')
        return redirect('view-users')
    context = {'user': user}
    return render(request, 'ucclms/delete-user.html', context)


@allowed_users(allowed_roles=['admin'])
def editUser(request, pk):
    person = User.objects.get(id=pk)
    form = CreateUserForm(instance=person)
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            messages.success(request, f'{person} has been updated')
            return redirect('view-users')
        
    context = {'form': form}
    return render(request, 'ucclms/edit-user.html', context)


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def viewUsers(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'ucclms/view-users.html', context)


def userPage(request):
    return render(request, 'ucclms/user-page.html')



@login_required(login_url='login')
def viewBooks(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'ucclms/view-books.html', context)


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def recommendations(request):
    recommendations = Recommendation.objects.all()
    context = {'recommendations': recommendations}
    return render(request, 'ucclms/recommendations.html', context)



@allowed_users(allowed_roles=['admin'])
def addBook(request):
    form = AddBookForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, f'Book has been added successfully')
            return redirect('view-books')
    context = {'form': form}
    return render(request, 'ucclms/add-book.html', context)


@allowed_users(allowed_roles=['admin'])
def editBook(request, pk):
    book = Book.objects.get(id=pk)
    form = AddBookForm(instance=book)
    
    if request.method == 'POST':
        form = AddBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'{book} has been updated')
            return redirect('view-books')
        
    context = {'form': form}
    return render(request, 'ucclms/edit-book.html', context)


@allowed_users(allowed_roles=['admin'])
def deleteBook(request, pk):
    book = Book.objects.get(id=pk)

    if request.method == "POST":
        book.delete()
        messages.success(request, f'{book} has been deleted successfully')
        return redirect('view-books')
    context = {'book': book}
    return render(request, 'ucclms/delete-book.html', context)


@login_required(login_url='login')
def bookRecords(request):
    book_records = BookRecord.objects.all()
    context = {'book_records': book_records}
    return render(request, 'ucclms/book-records.html', context)

@login_required(login_url='login')
def studentBorrowedBooks(request):
    book_records = BookRecord.objects.filter(user=request.user)
    context = {'book_records': book_records}
    return render(request, 'ucclms/student-borrowed-books.html', context)



@login_required(login_url='login')
def recommendBook(request):
    data_dict = {
        'user': request.user,
        # 'book_name': '',
        # 'description': '',
    }
    form = RecommendBookForm(data_dict)
    # print('USER ID', request.user)
    if request.method == 'POST':
        form.user = request.user
        form = RecommendBookForm(request.POST)
        # print('POST b name:', request.user)
        if form.is_valid():
            form.user = request.user
            form.save()
            messages.success(request, 'Book has been recommended')
            return redirect('student-dashboard')
    context = {'form': form}
    return render(request, 'ucclms/recommend-book.html', context)

def borrowBook(request, pk):
    book = Book.objects.get(id=pk)
    person = request.user
    datey = datetime.now() + timedelta(days=7)
    datey = datey.strftime("%Y-%m-%d %H:%M:%S")
    datadict = {'book': book, 'user': person, 'due_date': datey}
    form = BorrowBookForm(datadict)
    
    if request.method == 'POST':
        form.user = request.user
        form = BorrowBookForm(request.POST)
        if form.is_valid():
            form.user = request.user
            form.save()
            messages.success(request, f'Book requested. You can pick up your book "{book.title}" at Sam Jonah Library at "{book.location}"')
            return redirect('student-dashboard')
        
    context = {'form': form}
    return render(request, 'ucclms/borrow-book.html', context)


def studentViewBooks(request):
    books = Book.objects.all()
    if request.method == 'POST':
        book=request.post
    context = {'books': books}
    return render(request, 'ucclms/student-view-books.html', context)    



def about(request):
    return render(request, 'ucclms/about.html')    

def editProfile(request, pk):
    student = Student.objects.get(user=request.user)
    form = CreateStudentForm(instance=student)
    if request.method == 'POST':
        form = CreateStudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()

            return redirect(request, 'student-dashboard')

    context = {'form': form, 'person': student}
    return render(request, 'ucclms/edit-profile.html', context)

@allowed_users(allowed_roles=['admin'])
def editBookRecord(request, pk):
    record = BookRecord.objects.get(id=pk)
    form = AlterBookRecord(instance=record)
    
    if request.method == 'POST':
        form = AlterBookRecord(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book record has been updated')
            return redirect('book-records')
        
    context = {'form': form}
    return render(request, 'ucclms/edit-book-record.html', context)