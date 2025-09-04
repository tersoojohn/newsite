from django.urls import path
from django.http import HttpResponse
from . import views

# def home(request):
#     return HttpResponse("Hello, here we go.")

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('', views.home, name='home'),
    path('category-page/<str:pk>/', views.categoryPage, name='category-page'),
    path('news-page/<str:pk>/', views.newsPage, name='newsPage'),
    path('adminPanel/', views.adminPanel, name='adminPanel'),
    path('add-staff/', views.addStaff, name='add-staff'),
    path('staff/<str:pk>/', views.staffPage, name='staff'),
    path('staff-log/', views.allStaffs, name='staff-log'),
    path('create-page/', views.createPage, name='create-page'),
    path('update-staff/<str:pk>/', views.updateStaff, name='update-staff'),
    path('delete-staff/<str:pk>/', views.deleteStaff, name='delete-staff')
]