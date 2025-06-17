from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Welcome to the Freelance Platform API</h1>")

urlpatterns = [
    path('', home),  # This line adds a root URL
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
]