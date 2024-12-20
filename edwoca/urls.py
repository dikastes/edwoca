from django.urls import path

from . import views

app_name='edwoca'
urlpatterns = [
        path('', views.IndexView.as_view(), name = 'index')
    ]
