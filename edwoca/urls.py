from django.urls import path

from . import views

app_name='edwoca'
urlpatterns = [
        path('', views.IndexView.as_view(), name = 'index'),
        path('works/<int:pk>', views.WorkDetailView.as_view(), name = 'work_detail'),
        path('works/update/<int:pk>', views.WorkUpdateView.as_view(), name = 'work_update'),
        path('works/new', views.WorkCreateView.as_view(), name = 'work_create'),
        path('worktitles/new/<int:work_id>', views.WorkTitleCreateView.as_view(), name = 'work_title_create'),
        path('worktitles/update/<int:pk>', views.WorkTitleUpdateView.as_view(), name = 'work_title_update'),
        path('worktitles/delete/<int:pk>', views.WorkTitleDeleteView.as_view(), name = 'work_title_delete'),
        path('relatedwork/new/<int:work_id>', views.RelatedWorkCreateView.as_view(), name = 'related_work_create'),
        path('relatedwork/update/<int:pk>', views.RelatedWorkUpdateView.as_view(), name = 'related_work_update'),
        path('relatedwork/delete/<int:pk>', views.RelatedWorkDeleteView.as_view(), name = 'related_work_delete'),
        path('contributor/new/<int:work_id>', views.ContributorCreateView.as_view(), name = 'contributor_create'),
        path('contributor/update/<int:pk>', views.ContributorUpdateView.as_view(), name = 'contributor_update'),
        path('contributor/delete/<int:pk>', views.ContributorDeleteView.as_view(), name = 'contributor_delete'),
        path('persons', views.person_list, name = 'person_list'),
    ]
