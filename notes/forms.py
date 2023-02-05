from django import forms
from .models import Notes, Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"type": "username", "placeholder": ("Username")})
    )
    password = forms.CharField(
        max_length=16,
        widget=forms.PasswordInput(
            attrs={
                # 'class':'form-control',
                "placeholder": "Password"
            }
        ),
    )


class NoteCreationForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ["title", "description", "category"]


class NoteUpdateForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ["title", "description", "category"]


class AccountSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]


class CategoryCreationForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["title"]


class NotesFilterForm(forms.Form):
    title_filter = forms.CharField(required=False, max_length=45)
    category_filter = forms.ModelChoiceField(
        required=False, queryset=Category.objects.all().order_by("title")
    )
