from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from .models import *

def registerpage(request):
    if request.method == "POST":
        form = UserModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('loginPage')
    else:
        form = UserModelForm()
        
    # Dictionary passed as context to the template
    context = {
        'form': form,
        'title': 'Register Form',
        'btn': 'Register'
    }
    return render(request, 'baseAuth.html', context)


def loginPage(request):
    if request.method == 'POST':
        form = AuthForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboardpage')
    else:
        form = AuthForm()
        
    context = {
        'form': form,
        'title': 'login Form',
        'btn': 'Login'
    }
    return render(request, 'baseAuth.html', context)


def logoutPage(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('loginPage')


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, "task_list.html", {"tasks": tasks})

@login_required
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "add_task.html", {"form": form})

