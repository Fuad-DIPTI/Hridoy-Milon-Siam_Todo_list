from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # This includes all paths from your app's urls.py
    path('', include('todolistapp.urls')), 
]