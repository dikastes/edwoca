from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Work
from dmad_on_django.models import Status
from .forms import WorkTitleForm

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

class WorkDetailView(generic.DetailView):
    template_name = 'edwoca/work_detail.html'
    model = Work

def work_update(request, work_id):
    work = get_object_or_404(Work, id = work_id)
