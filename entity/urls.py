from django.urls import path
from entity import views

app_name = 'entity'
urlpatterns = [
    path('', views.index, name='index'),
]