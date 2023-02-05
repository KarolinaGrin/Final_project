from django.urls import path
from . import views
import django.contrib.auth.views as auth_views

app_name = 'notes'

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', views.login_view, name='login'),
    path('home/', views.home_page, name='home'),
    path('register/', views.register, name='register'),
    path('settings/', views.settings, name='settings'),
    path('category/', views.categories, name='category-list'),
    path('logout/', views.logout_view, name='logout'),
    path('category/<int:category_id>/', views.edit_category, name='category-detail'),
    path('category/delete/<int:category_id>/', views.delete_category, name='category-delete'),
    path('note/<int:note_id>/', views.edit_note, name='edit-note'),
    path('note/delete/<int:note_id>/', views.delete_note, name='note-delete'),
]
