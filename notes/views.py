from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Notes
from .forms import NoteCreationForm, NoteUpdateForm, AccountSettingsForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm

# Create your views here.


def index(request):
    return render(request, 'notes/index.html')


def login(request):

    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(username=username, password=password)

    if user is not None:
        return redirect('notes:home')
    elif username and password:
        messages.info(request, 'Login attemp failed.')

    context = {
        'form': AuthenticationForm(),
        'username': username,
        'password': password,
        'user': user
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


def logout(request):
    return render(request, 'notes/logout.html')


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


def delete(request, id):
    note_to_delete = Notes.objects.get(id=id)

    note_to_delete.delete()

    return redirect('notes:home_page')
