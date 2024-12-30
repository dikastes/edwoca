from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.http import HttpResponse
from django.views import generic
from .models import Work
from dmad_on_django.models import Status, Person
from .forms import WorkTitleForm
from json import dumps as json_dump

class IndexView(generic.ListView):
    template_name = 'edwoca/index.html'
    context_object_name = 'work_list'

    def get_queryset(self):
        return [
                {
                    'id' : work.id,
                    'gnd_id' : work.gnd_id,
                    'title' : work.titles.get(status=Status.PRIMARY)
                } for
                work in
                Work.objects.all()
            ]

class WorkUpdateView(generic.edit.UpdateView):
    model = Work
    fields = [
            'work_catalog_number',
            'gnd_id',
            'history'
        ]
    template_name_suffix = '_update'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.titles.get(status=Status.PRIMARY).title
        context['work_title_forms'] = [ WorkTitleForm(instance=title) for title in self.object.titles.all() ]
        return context

def person_list(request):
    persons = [
            f"{person.names.get(status=Status.PRIMARY).last_name}_{person.names.get(status=Status.PRIMARY).first_name}-{person.gnd_id}"
            for person
            in Person.objects.all()
        ]
    serialized_persons = json_dump(persons)
    return HttpResponse(serialized_persons, content_type='application/json')
