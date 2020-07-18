from django.urls import path
from . import views


app_name="main"
 
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("api.html", views.api_welink, name="api_welink"),
    path("presentation.html", views.presentation_welink, name="presentation_welink"),
   
]
