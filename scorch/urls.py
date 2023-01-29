from django.urls import path
from scorch import views

app_name = 'scorch'
urlpatterns = [
    path('', views.index, name='index'),
    path('scorecards', views.scorecards, name='scorecards'),
    path('scorecards/<int:scorecard_id>', views.scorecard_detail,
        name='scorecvard_detail'),
]