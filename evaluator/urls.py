from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_entry, name='job_entry'),
    path('upload/', views.upload_cvs, name='upload_cvs'),
    path('results/', views.evaluation_results, name='evaluation_results'),
]
