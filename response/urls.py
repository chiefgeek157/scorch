from django.urls import path
from response import views

app_name = 'response'
urlpatterns = [
    path('', views.index, name='index'),
]