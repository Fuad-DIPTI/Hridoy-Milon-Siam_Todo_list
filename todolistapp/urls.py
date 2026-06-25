from django.urls import path
from . import views

urlpatterns = [
    # Login / Logout Routes
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Registration Route
    path('register/', views.register_view, name='register'),
    path('tasks/', views.task_list_view, name='task_list'),
    
    # Main Application Tasks Routes
    path('', views.dashboard, name='dashboard'),  # Homepage / Dashboard
    path('task/toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('task/edit/<int:task_id>/', views.edit_task_view, name='edit_task'),
    path('task/delete/<int:task_id>/', views.delete_task_view, name='delete_task'),
]