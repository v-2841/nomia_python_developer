from django.urls import path

from surveys import views


app_name = 'surveys'
urlpatterns = [
    path('', views.index, name='index'),
    path('surveys/<int:pk>/', views.survey, name='survey'),
    path('surveys/<int:pk>/results/',
         views.survey_results, name='survey_results'),
]
