from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Notes, Category
from .forms import NoteCreationForm, NoteUpdateForm, AccountSettingsForm, CategoryCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from django.views import generic

# Create your views here.

@login_required
def index(request):
    return render(request, 'notes/index.html')


def login_view(request):

    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('notes:home')
    elif username and password:
        messages.info(request, 'Login attemp failed.')

    context = {
        'form': AuthenticationForm(),
        'username': username,
        'password': password,
    }
    return render(request, 'notes/login.html', context)


def register(request):
    form = UserCreationForm(request.POST)

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect('notes:login')

    context = {
        'form': form
    }
    return render(request, 'notes/register.html', context)

@login_required
def home_page(request):
    notes = Notes.objects.all()
    form = NoteCreationForm()

    if request.method == "POST":
        form = NoteCreationForm(request.POST)

        if form.is_valid():
            note_obj = form.save(commit=False)
            note_obj.author = request.user
            note_obj.save()

            return redirect('note/home.html')
    context = {
        'notes': notes,
        'form': form
    }
    return render(request, 'notes/home.html', context)

@login_required
def settings(request):
    user = request.user
    form = AccountSettingsForm(instance=user)

    if request.method == "POST":
        user.username = request.POST['username']
        user.email = request.POST['email']

        user.save()

        messages.success(request, "Information has been changed")

        return redirect("notes:settings")
    context = {
        'form': form,
        'user': user
    }

    return render(request, 'notes/settings.html', context)


def logout_view(request):
    logout(request)
    return render(request, 'notes/logout.html')

@login_required
def edit(request):
    note_to_update = Notes.objects.get(id=id)
    form = NoteUpdateForm(instance=note_to_update)

    if request.method == "POST":
        form = NoteUpdateForm(request.POST)

        if form.is_valid():
            note_to_update.title = form.cleaned_data["title"]
            note_to_update.description = form.cleaned_data["description"]

            note_to_update.save()

            return redirect('notes:home_page')

    context = {
        'note': note_to_update,
        'form': form
    }
    return render(request, 'notes/update.html', context)

@login_required
def delete(request, id):
    note_to_delete = Notes.objects.get(id=id)

    note_to_delete.delete()

    return redirect('notes:home_page')

@login_required
def get_category_list(request):

    # username = request.POST.get("username")
    # password = request.POST.get("password")
    # user = authenticate(username=username, password=password)
    all_categories = Category.objects.all()

    context = {
        'categories': all_categories,
        'form': CategoryCreationForm,

    }
    return render(request, 'notes/category.html', context)

@login_required
def create_category(request):
    title = request.POST.get("title")

    if title:
        form = CategoryCreationForm(request.POST)
        if form.is_valid():
            category = Category.objects.create(title=title)
            category.save()

    return get_category_list(request)

@login_required
def categories(request):
    if request.method == 'GET':
        return get_category_list(request)

    elif request.method == 'POST':
        return create_category(request)

@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    form = CategoryCreationForm(instance=category)

    if request.method == "POST":
        form = CategoryCreationForm(request.POST)

        if form.is_valid():
            category.title = form.cleaned_data["title"]

            category.save()

            return redirect('notes:category-list')

    elif request.method == 'DELETE':
        category.delete()

        return get_category_list(request)

    context = {
        'category': category,
        'form': form
    }
    return render(request, 'notes/categoryedit.html', context)

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    category.delete()

    return get_category_list(request)
