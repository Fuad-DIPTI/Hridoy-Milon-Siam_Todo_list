from django.shortcuts import render, redirect  
# FIX: Alias 'login' as 'auth_login' so it doesn't break your routes!
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate  
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.http import Http404  
from .models import *
from .forms import RegisterForm, AuthForm, TaskForm

# ==================== ১. CLASS-BASED LOGIN VIEW ====================
class UserLoginView(LoginView):
    template_name = 'auth/login.html'
    authentication_form = AuthForm  # You can uncomment this safely now!
    redirect_authenticated_user = True
    next_page = 'dashboard'


# ==================== FUNCTION-BASED LOGIN VIEW (Alternative) ====================
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = AuthForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user) # Uses the aliased function safely
                return redirect('dashboard')
    else:
        form = AuthForm()
        
    return render(request, 'auth/login.html', {'form': form})


# ==================== LOGOUT VIEW ====================
def logout_view(request):
    auth_logout(request)
    return redirect('login')  


# ==================== ২. REGISTER VIEW ====================
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  
        
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Updated to use auth_login alias
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})


# ==================== ৩. DASHBOARD VIEW ====================

@login_required
def dashboard(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  
            task.save()
            return redirect('dashboard')

    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    
    # 👇 Add this line to count completed tasks cleanly in Python
    completed_count = tasks.filter(completed=True).count()
    
    form = TaskForm()
    
    context = {
        'tasks': tasks, 
        'completed_count': completed_count,  # 👇 Add this to the context
        'form': form
    }
    return render(request, 'tasks/dashboard.html', context)


# ==================== ৪. UPDATE: TOGGLE TASK STATUS ====================
@login_required
def toggle_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)
        task.completed = not task.completed
        task.save()
    except Task.DoesNotExist:
        raise Http404("Task not found or access denied.")
        
    return redirect('dashboard')


# ==================== ৫. UPDATE: EDIT TASK ====================
@login_required
def edit_task_view(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)
    except Task.DoesNotExist:
        raise Http404("Task not found or access denied.")

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)

    context = {
        'form': form, 
        'task': task
    }
    return render(request, 'tasks/edit_task.html', context)


# ==================== ৬. DELETE: REMOVE TASK ====================
@login_required
def delete_task_view(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)
        task.delete()
    except Task.DoesNotExist:
        raise Http404("Task not found or access denied.")
        
    return redirect('dashboard')

@login_required
def task_list_view(request):
    # Fetch all tasks belonging to the current user
    all_tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    
    # Optional: Filter by status via query parameters (e.g., /tasks/?status=completed)
    status_filter = request.GET.get('status')
    if status_filter == 'completed':
        all_tasks = all_tasks.filter(completed=True)
    elif status_filter == 'active':
        all_tasks = all_tasks.filter(completed=False)

    context = {
        'tasks': all_tasks,
        'current_filter': status_filter or 'all'
    }
    return render(request, 'tasks/task_list.html', context)