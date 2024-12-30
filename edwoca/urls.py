from django.urls import path

from . import views

app_name='edwoca'
urlpatterns = [
        path('', views.IndexView.as_view(), name = 'index'),
        path('works/<int:pk>', views.WorkUpdateView.as_view(), name = 'work_detail'),
        path('works/update/<int:pk>', views.work_update, name = 'work_update'),
        path('persons', views.person_list, name = 'person_list'),
    ]
