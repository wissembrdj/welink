from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', views.UserqueryApi.as_view()),
    path('', include('main.urls')),
]
