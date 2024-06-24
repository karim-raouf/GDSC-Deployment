from django.urls import path 
from . import views


urlpatterns = [
    path('', views.homepage , name="Home"),
    path('prediction/', views.grade_class_prediction , name="prediction"),
]