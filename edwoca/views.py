from django.shortcuts import render
from django.views import generic
from .models import Work
from dmad_on_django.models import Status

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'edwoca/index.html'
    context_object_name = 'work_list'

    def get_queryset(self):
        return [
                {
                    'gnd_id' : work.gnd_id,
                    'title' : work.titles.get(status=Status.PRIMARY)
                } for
                work in
                Work.objects.all()
            ]
