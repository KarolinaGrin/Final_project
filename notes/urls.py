from django.urls import path
from . import views

urlpatterns =[
    path('',views.index, name='index'),
    path('login/',views.login, name='login'),
    path('home/', views.home_page, name='home'),
    path('edit/',views.edit, name='edit'),
    path('register/',views.register, name='register'),
    path('settings/',views.settings, name='settings'),
]
