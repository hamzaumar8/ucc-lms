import time
import os
import csv, io
from django.views.static import serve
from django.contrib.auth import forms
from django.contrib.auth.models import User, Group
from django.contrib.messages.api import error
from django.db import IntegrityError
from django.forms.forms import Form
from django.urls import reverse
from django.conf import settings
from django.db.models import Count, Q
from django.utils.crypto import get_random_string
from django.http import request, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import get_template
from .forms import AddSubjectForm, BorrowBookForm, CreateStudentForm, CreateUserForm, AddBookForm, AlterBookRecord, EditStudentProfile, ProfileUserUpdateForm, RecommendBookForm, BorrowBookForm
from .models import *
from .decorators import unauthenticated_user, allowed_users
from datetime import datetime, timedelta




def signup_invite_email(request, email, password):
    html = get_template("ucclms/emails/users.html")
    content = html.render({"email": email, "password": password})
    msg = "Kindly visit %s to create an account" % email
    send_mail(
        "Login Details for UCC LMS Portal",
        msg,
        'ucclms@gmail.com',
        [email],
        fail_silently=False,
        html_message=content,
    )

    

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
            print('howdy',user_group)
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
    context = {'dash_title':'','student': student}
    return render(request, 'ucclms/student-dashboard.html', context)

@allowed_users(allowed_roles=['admin'])
def adminDashboard(request):
    admin = Administrator.objects.get(user=request.user)
    context = {'dash_title':'Dashboard','admin': admin}
    return render(request, 'ucclms/admin-dashboard.html', context)


@unauthenticated_user
def signUp(request):
    sform = ProfileUserUpdateForm()
    form = CreateUserForm()

    if request.method == 'POST':
        sform = ProfileUserUpdateForm(request.POST)
        form = CreateUserForm(request.POST)
        if form.is_valid() and sform.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='student')
            user.groups.add(group)
            user_profile = user.student
            user_profile.index_number = sform.cleaned_data['index_number']
            user_profile.save()
            messages.success(request, f'Account created for {username}')
 
            return redirect('login')
    context = {'form': form, 'sform': sform}
    return render(request, 'ucclms/sign-up.html', context)


@allowed_users(allowed_roles=['admin'])
def createUser(request):
    sform = ProfileUserUpdateForm()
    form = CreateUserForm()
    if request.method == 'POST':
        sform = ProfileUserUpdateForm(request.POST)
        form = CreateUserForm(request.POST)
        if form.is_valid() and sform.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='student')
            user.groups.add(group)
            user_profile = user.student
            user_profile.index_number = sform.cleaned_data['index_number']
            user_profile.save()
            messages.success(request, f'{username} has been added successfully')
            return redirect('view-users')
    context = {'form': form, 'sform': sform}
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
        
    context = {'dash_title':'Edit User','form': form}
    return render(request, 'ucclms/edit-user.html', context)

from django.contrib.auth.hashers import make_password

@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def viewUsers(request):
    users = User.objects.order_by('-id')
    
    if request.method == "POST":
        csv_file = request.FILES['file']

        if csv_file.name.endswith('.csv'):
            if csv_file.size < 33554432:
                data_set = csv_file.read().decode('UTF-8')

                io_string = io.StringIO(data_set)
                next(io_string)
                csv_read = csv.reader(io_string, delimiter=',', quotechar="|")
                for column in csv_read:
                    try:
                        generated_pass = get_random_string(length=8)
                        user = User.objects.create(
                            username= column[1],
                            first_name= column[2],
                            last_name= column[3],
                            email= column[4],
                            password= make_password(generated_pass)
                        )
                        group = Group.objects.get(name='student')
                        user.groups.add(group)
                        user_profile = user.student
                        user_profile.index_number = column[1]
                        user_profile.save()

                        # send mail
                        signup_invite_email(request, column[4], generated_pass)
                        
                    except IntegrityError as e: 
                        messages.warning(request, f"Duplicate entry, Please don't import an already existing User Index Number And Email")
                        return HttpResponseRedirect(request.path_info)
                    except Exception as e:
                        error = str(e)
                        messages.warning(request, f"{error}")
                        return HttpResponseRedirect(request.path_info)
            else:
                messages.error(request, 'The size must no br more then 32GB.')
        else:
            messages.error(request, 'THIS IS NOT A CSV FILE')
    
    context = {'dash_title':'Users','users': users}
    return render(request, 'ucclms/view-users.html', context)


def userPage(request):
    return render(request, 'ucclms/user-page.html')

def download_book_deomo_file(request):
    path = 'Books-demo.csv'
    filepath = os.path.join(settings.DEMO_ROOT, path)
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))


def download_user_deomo_file(request):
    path = 'Users-demo.csv'
    filepath = os.path.join(settings.DEMO_ROOT, path)
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))



@login_required(login_url='login')
def viewBooks(request):
    books = Book.objects.order_by('-id')
    # print(os.path.dirname(os.path.realpath(__file__)))
    # print('gr', os.path.basename(settings.DEMO_DOWNLOAD_CSV_FILE))
    # print('gr', os.path.dirname(settings.DEMO_DOWNLOAD_CSV_FILE))
    # print('grab', os.path.join(settings.BASE_DIR, 'static'))
    if request.method == "POST":
        csv_file = request.FILES['file']
        # let's check if it is a csv file
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
        if csv_file.size > 33554432:
            messages.error(request, 'The size must no br more then 32GB.')
        data_set = csv_file.read().decode('UTF-8')
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            try:
                _subject, created = Subject.objects.update_or_create(name=column[6])
                _book, created = Book.objects.update_or_create(
                    title=column[0],
                    publisher=column[1],
                    availability=column[2],
                    year=column[3],
                    author=column[4],
                    location=column[5],
                    subject=_subject,
                )
                _book.save()
                
            except IntegrityError as e: 
                messages.warning(request, f"Duplicate entry, Please don't import an already existing Entity Name or Admin email (book title)!")
                return HttpResponseRedirect(request.path_info)
            except Exception as e:
                error = str(e)
                messages.warning(request, f"{error}")
                return HttpResponseRedirect(request.path_info)

    context = {'dash_title':'All Books','books': books}
    return render(request, 'ucclms/view-books.html', context)


@login_required(login_url='login')
def viewSubject(request):
    subjects = Subject.objects.order_by('-id').annotate(num_subject=Count('booksubject', distinct=True))
    context = {'dash_title':"Books Categories (Subjects)",'subjects': subjects}
    return render(request, 'ucclms/view-subjects.html', context)

@login_required(login_url='login')
def viewSubjectStudent(request):
    subjects = Subject.objects.order_by('-id').annotate(num_subject=Count('booksubject', distinct=True))
    context = {'dash_title':"Books Categories (Subjects)",'subjects': subjects}
    return render(request, 'ucclms/student-view-subjects.html', context)





@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def recommendations(request):
    recommendations = Recommendation.objects.all()
    context = {'dash_title':'Recommendations','recommendations': recommendations}
    return render(request, 'ucclms/recommendations.html', context)



@allowed_users(allowed_roles=['admin'])
def addBook(request):
    form = AddBookForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, f'Book has been added successfully')
            return redirect('view-books')
    context = {'dash_title':'Add New Book','form': form}
    return render(request, 'ucclms/add-book.html', context)


@allowed_users(allowed_roles=['admin'])
def addSubject(request):
    form = AddSubjectForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, f'Subject has been added successfully')
            return redirect('view-subjects')
    context = {'dash_title':'Add Subject Category','form': form}
    return render(request, 'ucclms/add-subject.html', context)


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
        
    context = {'dash_title':'Edit Book','form': form}
    return render(request, 'ucclms/edit-book.html', context)

@allowed_users(allowed_roles=['admin'])
def editSubject(request, pk):
    book = Subject.objects.get(id=pk)
    form = AddSubjectForm(instance=book)
    
    if request.method == 'POST':
        form = AddSubjectForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'{book} has been updated')
            return redirect('view-subjects')
        
    context = {'dash_title':'Edit Subject Category','form': form}
    return render(request, 'ucclms/edit-subject.html', context)


@allowed_users(allowed_roles=['admin'])
def deleteBook(request, pk):
    book = Book.objects.get(id=pk)

    if request.method == "POST":
        book.delete()
        messages.success(request, f'{book} has been deleted successfully')
        return redirect('view-books')
    context = {'book': book}
    return render(request, 'ucclms/delete-book.html', context)


@allowed_users(allowed_roles=['admin'])
def deleteSubject(request, *args, **kwargs):
    subject = get_object_or_404(Subject, pk=kwargs["id"])
    subject.delete()
    messages.success(request, f'{subject} has been deleted  successfully')
    return redirect(reverse('view-subjects'))


@allowed_users(allowed_roles=['admin'])
def addStolenBook(request, *args, **kwargs):
    book_rec = get_object_or_404(BookRecord, pk=kwargs["id"])
    book = Book.objects.filter(id=book_rec.book.id)
    book_st = book.first().no_stolen
    no_stolen = book_st + 1
    book = book.update(is_stolen=True, no_stolen=no_stolen)
    messages.success(request, f'{book} has been recorded  Stolen')
    return redirect(reverse('books-not-returned'))


@login_required(login_url='login')
def bookRecords(request):
    book_records = BookRecord.objects.all()
    context = {'dash_title':'Book Records','book_records': book_records}
    return render(request, 'ucclms/book-records.html', context)

@login_required(login_url='login')
def studentBorrowedBooks(request):
    book_records = BookRecord.objects.filter(user=request.user)
    context = {'dash_title':'Borrowed Books','book_records': book_records}
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
    context = {'dash_title':'Recomend Book','form': form}
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
            bk = Book.objects.filter(id=pk)
            if bk.availability > 0:
                avail = bk.availability - 1
                bk.update(availability=avail)
            messages.success(request, f'Book requested. You can pick up your book "{book.title}" at Sam Jonah Library at "{book.location}"')
            return redirect('student-dashboard')
        
    context = {'dash_title':'Borrow A Book','form': form}
    return render(request, 'ucclms/borrow-book.html', context)


def studentViewBooks(request):
    print(request.user.groups)
    books = Book.objects.all()
    if request.method == 'POST':
        book=request.post
    context = {'dash_title':'Books','books': books}
    return render(request, 'ucclms/student-view-books.html', context)    



def about(request):
    return render(request, 'ucclms/about.html')    

def editProfile(request, pk):
    student = Student.objects.get(user=request.user)
    print(request.user.student)
    form = EditStudentProfile(instance=request.user.student)
    if request.method == 'POST':
        form = EditStudentProfile(request.POST, request.FILES, instance=request.user.student)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your Profile has been updated!')
            return redirect('edit-profile', pk=pk)

    context = {'dash_title':'Edit Profile','form': form, 'person': student}
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







@allowed_users(allowed_roles=['admin'])
def booksNotreturned(request):
    book_records = BookRecord.objects.filter(date_of_return=None)
    context = {'dash_title':'Books Not Returned','book_records': book_records}
    return render(request, 'ucclms/student-booksnot.html', context)


@allowed_users(allowed_roles=['admin'])
def StolenBooks(request):
    stolen_books = Book.objects.filter(is_stolen=True)
    context = {'dash_title':'Stolen Books','stolen_books': stolen_books}
    return render(request, 'ucclms/stolen-books.html', context)




@login_required(login_url='login')
def viewSubjectDet(request, *args, **kwargs):
    subject = get_object_or_404(Subject, pk=kwargs["id"])
    books = Book.objects.filter(subject=subject).order_by('-id')
    context = {'dash_title':"Books Categories (Subjects)",'books': books}
    return render(request, 'ucclms/view-book-cat.html', context)


@login_required(login_url='login')
def viewSubjectDetStu(request, *args, **kwargs):
    subject = get_object_or_404(Subject, pk=kwargs["id"])
    books = Book.objects.filter(subject=subject).order_by('-id')
    context = {'dash_title':"Books Categories (Subjects)",'books': books}
    return render(request, 'ucclms/view-book-cat-stu.html', context)







