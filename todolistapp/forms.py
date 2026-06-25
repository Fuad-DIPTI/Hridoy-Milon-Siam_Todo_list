from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        # Fixed: Removed password1 and password2. Django's UserCreationForm handles these automatically!
        fields = ['username', 'email','password1','password2'] 


# --- 2. LOGIN/AUTHENTICATION FORM ---
class AuthForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']  # This will now safely find 'description'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 text-sm bg-white border border-slate-200 rounded-xl focus:outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-100 transition duration-150'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 text-sm bg-white border border-slate-200 rounded-xl focus:outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-100 transition duration-150',
                'rows': 3
            }),
        }