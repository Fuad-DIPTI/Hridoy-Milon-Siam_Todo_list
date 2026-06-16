from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("task_list/", views.task_list, name="task_list"),
    path("add/", views.add_task, name="add_task"),
    path("dashboard/", views.dashboard, name="dashboard"),
]

