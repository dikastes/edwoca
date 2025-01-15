from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.http import HttpResponse
from django.views import generic
from .models import Work, WorkTitle, RelatedWork, Contributor
from dmad_on_django.models import Status, Person
from .forms import WorkTitleForm
from json import dumps as json_dump

class IndexView(generic.ListView):
    template_name = 'edwoca/index.html'
    context_object_name = 'work_list'

    def get_queryset(self):
        return Work.objects.all()
        #return [
                #{
                    #'id' : work.id,
                    #'gnd_id' : work.gnd_id,
                    #'title' : work.titles.get(status=Status.PRIMARY)
                #} for
                #work in
                #Work.objects.all()
            #]

class WorkCreateView(generic.edit.CreateView):
    model = Work
    fields = [
            'work_catalog_number',
            'gnd_id',
            'history'
        ]
    template_name_suffix = '_create'
    context_object_name = 'work'

    def get_success_url(self):
        return reverse_lazy('edwoca:work_detail', kwargs = {'pk': self.object.id})

class WorkUpdateView(generic.edit.UpdateView):
    model = Work
    fields = [
            'work_catalog_number',
            'gnd_id',
            'history'
        ]
    template_name_suffix = '_update'
    context_object_name = 'work'

    def get_success_url(self):
        return reverse_lazy('edwoca:work_detail', kwargs = {'pk': self.object.id})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            pref_title = self.object.titles.get(status=Status.PRIMARY).title
        except:
            pref_title = '<ohne Titel>'
        context['title'] = pref_title
        return context

class WorkTitleCreateView(generic.edit.CreateView):
    model = WorkTitle
    fields = [
            'title',
            'status',
            'language',
            'work'
        ]
    template_name = 'edwoca/update_relation.html'
    context_object_name = 'work_title'

    def get_success_url(self):
        return reverse_lazy('edwoca:work_detail', kwargs = {'pk': self.object.work.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        work = Work.objects.get(id=self.kwargs['work_id'])
        form = self.get_form_class()(initial = {'work': work})
        context['form'] = form
        context['view_title'] = f"Neuen Titel für {work} anlegen"
        return context

class ContributorCreateView(generic.edit.CreateView):
    model = Contributor
    fields = [
            'work',
            'person',
            'role'
        ]
    template_name = 'edwoca/update_relation.html'
    context_object_name = 'contributor'

    def get_success_url(self):
        return reverse_lazy('edwoca:work_detail', kwargs = {'pk': self.object.work.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        work = Work.objects.get(id=self.kwargs['work_id'])
        form = self.get_form_class()(initial = {'work': work})
        context['form'] = form
        context['view_title'] = f"Neuen Beteiligten für Werk {work} anlegen"
        return context

class ContributorUpdateView(generic.edit.UpdateView):
    model = Contributor
    fields = [
            'work',
            'person',
            'role'
        ]
    template_name = 'edwoca/update_relation.html'
    context_object_name = 'contributor'

    def get_success_url(self):
        return reverse_lazy('edwoca:work_detail', kwargs = {'pk': self.object.work.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Beteiligten {self.object.person} am Werk {self.object.work} bearbeiten"
        return context

class ContributorDeleteView(generic.edit.DeleteView):
    model = Contributor
    template_name = 'edwoca/update_relation.html'
    context_object_name = 'contributor'

    def get_success_url(self):
        return reverse_lazy('edwoca:work_detail', kwargs = {'pk': self.object.work.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Beteiligten {self.object.person} am Werk {self.object.work} löschen"
        return context

class RelatedWorkCreateView(generic.edit.CreateView):
    model = RelatedWork
    fields = [
            'source_work',
            'target_work',
            'comment',
            'label'
        ]
    template_name = 'edwoca/update_relation.html'
    context_object_name = 'work'

    def get_success_url(self):
        return reverse_lazy('edwoca:work_detail', kwargs = {'pk': self.object.source_work.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        work = Work.objects.get(id=self.kwargs['work_id'])
        form = self.get_form_class()(initial = {'source_work': work})
        context['form'] = form
        context['view_title'] = f"Werkrelation für Werk {work} anlegen"
        return context

class RelatedWorkUpdateView(generic.edit.UpdateView):
    model = RelatedWork
    fields = [
            'source_work',
            'target_work',
            'comment',
            'label'
        ]
    template_name = 'edwoca/update_relation.html'
    context_object_name = 'work'

    def get_success_url(self):
        return reverse_lazy('edwoca:work_detail', kwargs = {'pk': self.object.source_work.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Werkrelation zwischen Werk {self.object.source_work} und {self.object.target_work} bearbeiten"
        return context

class RelatedWorkDeleteView(generic.edit.DeleteView):
    model = RelatedWork
    template_name = 'edwoca/update_relation.html'
    context_object_name = 'work'

    def get_success_url(self):
        return reverse_lazy('edwoca:work_detail', kwargs = {'pk': self.object.source_work.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Werkrelation zwischen Werk {self.object.source_work} und {self.object.target_work} löschen"
        return context

class WorkTitleUpdateView(generic.edit.UpdateView):
    model = WorkTitle
    template_name = 'edwoca/update_relation.html'
    fields = [
            'title',
            'status',
            'language'
        ]
    context_object_name = 'work_title'

    def get_success_url(self):
        return reverse_lazy('edwoca:work_detail', kwargs = {'pk': self.object.work.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['work_title'] = self.object
        return context

class WorkTitleDeleteView(generic.edit.DeleteView):
    model = WorkTitle
    template_name = 'edwoca/update_relation.html'
    context_object_name = 'work_title'

    def get_success_url(self):
        return reverse_lazy('edwoca:work_detail', kwargs = {'pk': self.object.work.id})

class WorkDetailView(generic.detail.DetailView):
    model = Work

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_work_targets'] = RelatedWork.objects.filter(source_work=self.object)
        context['related_work_sources'] = RelatedWork.objects.filter(target_work=self.object)
        context['contributors'] = Contributor.objects.filter(work=self.object)
        return context

def person_list(request):
    persons = [
            f"{person.names.get(status=Status.PRIMARY).last_name}_{person.names.get(status=Status.PRIMARY).first_name}-{person.gnd_id}"
            for person
            in Person.objects.all()
        ]
    serialized_persons = json_dump(persons)
    return HttpResponse(serialized_persons, content_type='application/json')
