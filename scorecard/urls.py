from django.urls import path
from scorecard import views

app_name = 'scorecard'
urlpatterns = [
    path('', views.index, name='index'),
    path('scorecards', views.scorecards, name='scorecards'),
    path('scorecards/<int:scorecard_id>', views.scorecard_detail,
        name='scorecvard_detail'),
]