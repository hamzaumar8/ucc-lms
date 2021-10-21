from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-dashboard/', views.adminDashboard, name='admin-dashboard'),
    path('student-dashboard', views.studentDashboard, name='student-dashboard'),
    path('login/', views.signIn, name='login'),
    path('redirect/', views.redirect, name='redirect'),
    path('about/', views.about, name='about'),
    path('logout/', views.signOut, name='logout'),
    path('sign-up/', views.signUp, name='sign-up'),
    path('view-users/', views.viewUsers, name='view-users'),
    path('add-book/', views.addBook, name='add-book'),
    path('add-subject/', views.addSubject, name='add-subject'),
    path('edit-book/<str:pk>', views.editBook, name='edit-book'),
    path('delete-book/<str:pk>', views.deleteBook, name='delete-book'),
    path('delete-subject/<int:id>', views.deleteSubject, name='delete-subject'),
    #Subject
    path('view-subjects/', views.viewSubject, name='view-subjects'),
    path('edit-subject/<str:pk>', views.editSubject, name='edit-subject'),
    path('subject-cat-info/<int:id>', views.viewSubjectDet, name='subject-cat-info'),
    path('add-stolen-book/<int:id>', views.addStolenBook, name='add-stolen-book'),
    path('view-books/', views.viewBooks, name='view-books'),
    path('recommend-book/', views.recommendBook, name='recommend-book'),
    path('create-user/', views.createUser, name='create-user'),
    path('edit-user/<str:pk>', views.editUser, name='edit-user'),
    path('edit-profile/<str:pk>', views.editProfile, name='edit-profile'),
    path('delete-user/<str:pk>', views.deleteUser, name='delete-user'),
    path('book-records/', views.bookRecords, name='book-records'),
    path('borrow-book/<str:pk>', views.borrowBook, name='borrow-book'),
    path('student-view-books/', views.studentViewBooks, name='student-view-books'),
    path('student-borrowed-books/', views.studentBorrowedBooks, name='student-borrowed-books'),
    path('books-not-returned/', views.booksNotreturned, name='books-not-returned'),
    path('edit-book-record/<str:pk>', views.editBookRecord, name='edit-book-record'),
    path('stolen-books/', views.StolenBooks, name='stolen-books'),
    path('recommendations/', views.recommendations, name='recommendations'),
    path('user-page/', views.userPage, name='user-page'),

    # Demo Files
    path("dowload-book-demo-file/", views.download_book_deomo_file, name="download-book-demo"),
    path("dowload-user-demo-file/", views.download_user_deomo_file, name="download-user-demo"),
]
