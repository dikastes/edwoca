from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.http import HttpResponse
from django.views import generic
from django.forms import HiddenInput
from .models import Work, WorkTitle, RelatedWork, WorkContributor, Expression, ExpressionContributor, ExpressionTitle
from dmad_on_django.models import Status, Person, Period
from dmad_on_django.forms import PeriodForm
from .forms import WorkTitleForm
from json import dumps as json_dump


class ReturnButtonView(generic.detail.SingleObjectTemplateResponseMixin):
    template_name = 'edwoca/base_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['return_target'] = 'edwoca:work_detail'
        context['return_pk'] = self.get_work().id
        context['button_label'] = 'anlegen'
        return context


class WorkRelationCreateView(generic.edit.CreateView, ReturnButtonView):
    def get_success_url(self):
        return reverse_lazy('edwoca:work_detail', kwargs = {'pk': self.get_work().id})

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super().get_form(form_class)
        for entity in ['work', 'source_work']:
            if entity in form.fields:
                form.fields[entity].initial = self.get_work()
                form.fields[entity].widget = HiddenInput()
                form.fields[entity].label = ''
        return form

    def get_work(self):
        return Work.objects.get(id=self.kwargs['work_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_label'] = 'anlegen'
        return context


class ExpressionRelationCreateView(generic.edit.CreateView, ReturnButtonView):
    def get_success_url(self):
        return reverse_lazy('edwoca:work_detail', kwargs = {'pk': self.get_work().id})

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super().get_form(form_class)
        for entity in ['expression', 'source_expression']:
            if entity in form.fields:
                form.fields[entity].initial = self.get_expression()
                form.fields[entity].widget = HiddenInput()
                form.fields[entity].label = ''
        return form

    def get_expression(self):
        return Expression.objects.get(id=self.kwargs['expression_id'])

    def get_work(self):
        return self.get_expression().work

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_label'] = 'anlegen'
        return context


class WorkRelationUpdateView(generic.edit.UpdateView, ReturnButtonView):
    def get_success_url(self):
        return reverse_lazy('edwoca:work_detail', kwargs = {'pk': self.get_work().id})

    def get_work(self):
        try:
            return self.object.work
        except:
            return self.object.source_work

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_label'] = 'speichern'
        return context


class ExpressionRelationUpdateView(generic.edit.UpdateView, ReturnButtonView):
    def get_success_url(self):
        return reverse_lazy('edwoca:work_detail', kwargs = {'pk': self.get_work().id})

    def get_expression(self):
        try:
            return self.object.expression
        except:
            return self.object.source_expression

    def get_work(self):
        return self.get_expression().work

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_label'] = 'speichern'
        return context


class WorkRelationDeleteView(generic.edit.DeleteView, ReturnButtonView):
    def get_success_url(self):
        return reverse_lazy('edwoca:work_detail', kwargs = {'pk': self.get_work().id})

    def get_work(self):
        try:
            return self.object.work
        except:
            return self.object.source_work

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_label'] = 'löschen'
        return context


class ExpressionRelationDeleteView(generic.edit.DeleteView, ReturnButtonView):
    def get_success_url(self):
        return reverse_lazy('edwoca:work_detail', kwargs = {'pk': self.get_work().id})

    def get_expression(self):
        try:
            return self.object.expression
        except:
            return self.object.source_expression

    def get_work(self):
        return self.get_expression().work

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_label'] = 'löschen'
        return context


class IndexView(generic.ListView):
    template_name = 'edwoca/index.html'
    context_object_name = 'work_list'

    def get_queryset(self):
        return Work.objects.all()


class WorkCreateView(generic.edit.CreateView):
    model = Work
    fields = [
            'work_catalog_number',
            'gnd_id',
            'history'
        ]
    template_name = 'edwoca/base_form.html'

    def get_success_url(self):
        return reverse_lazy('edwoca:work_detail', kwargs = {'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Neues Werk anlegen"
        context['button_label'] = "speichern"
        context['return_target'] = 'edwoca:index'
        context['return_pk'] = None
        return context


class WorkUpdateView(generic.edit.UpdateView):
    model = Work
    fields = [
            'work_catalog_number',
            'gnd_id',
            'history'
        ]
    template_name = 'edwoca/base_form.html'
    context_object_name = 'work'

    #def get_success_url(self):
        #return reverse_lazy('edwoca:work_detail', kwargs = {'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Werk { self.object } bearbeiten"
        context['button_label'] = "speichern"
        context['return_target'] = 'edwoca:work_detail'
        context['return_pk'] = self.object.id
        return context


class WorkDeleteView(generic.edit.DeleteView):
    model = Work
    success_url = reverse_lazy('edwoca:index')
    template_name_suffix = '_delete'
    context_object_name = 'work'


class WorkTitleView(generic.edit.ModelFormMixin):
    model = WorkTitle
    fields = [
            'title',
            'status',
            'language',
            'work'
        ]


class WorkTitleCreateView(WorkRelationCreateView, WorkTitleView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Neuen Titel für {self.get_work()} anlegen"
        return context


class WorkContributorView(generic.edit.ModelFormMixin):
    model = WorkContributor
    fields = [
            'work',
            'person',
            'role'
        ]


class WorkContributorCreateView(WorkRelationCreateView, WorkContributorView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Neuen Beteiligten für Werk {self.get_work()} anlegen"
        return context


class WorkContributorUpdateView(WorkRelationUpdateView, WorkContributorView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Beteiligten {self.object.person} am Werk {self.object.work} bearbeiten"
        return context


class WorkContributorDeleteView(WorkRelationDeleteView):
    model = WorkContributor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Beteiligten {self.object.person} am Werk {self.object.work} löschen"
        return context


class RelatedWorkView(generic.edit.ModelFormMixin):
    model = RelatedWork
    fields = [
            'source_work',
            'target_work',
            'comment',
            'label'
        ]


class RelatedWorkCreateView(WorkRelationCreateView, RelatedWorkView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Neuen Titel für {self.get_work()} anlegen"
        return context


class RelatedWorkUpdateView(WorkRelationUpdateView, RelatedWorkView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Werkrelation zwischen Werk {self.object.source_work} und {self.object.target_work} bearbeiten"
        return context


class RelatedWorkDeleteView(WorkRelationDeleteView):
    model = RelatedWork

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Werkrelation zwischen Werk {self.object.source_work} und {self.object.target_work} löschen"
        return context


class ExpressionPeriodView(generic.edit.ModelFormMixin):
    model = Period
    fields = [
            'not_before',
            'not_after',
            'display'
        ]


class ExpressionPeriodCreateView(ExpressionRelationCreateView, ExpressionPeriodView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Datumsangabe für Expression { self.get_expression() } von Werk { self.get_work() } anlegen"
        return context

    def form_valid(self, form):
        period = form.save()
        expression = self.get_expression()
        expression.period = period
        expression.save()
        return super().form_valid(form)


class ExpressionPeriodUpdateView(ExpressionRelationUpdateView, ExpressionPeriodView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Datumsangabe für Expession {self.object.expression} bearbeiten"
        return context


class ExpressionPeriodDeleteView(ExpressionRelationDeleteView):
    model = Period

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Datumsangabe von Expression {self.object.expression} löschen"
        return context


class ExpressionTitleView(generic.edit.ModelFormMixin):
    model = ExpressionTitle
    fields = [
            'title',
            'language',
            'status',
            'expression'
        ]


class ExpressionTitleCreateView(ExpressionRelationCreateView, ExpressionTitleView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Titel für Expression {self.get_expression()} von Werk {self.get_expression().work} anlegen"
        return context


class ExpressionTitleUpdateView(ExpressionRelationUpdateView, ExpressionTitleView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Titel { self.object } der Expression { self.object.expression } bearbeiten"
        return context


class ExpressionTitleDeleteView(ExpressionRelationDeleteView):
    model = ExpressionTitle

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Titel { self.object } von Expression {self.object.expression} löschen"
        return context


class ExpressionContributorView(generic.edit.ModelFormMixin):
    model = ExpressionContributor
    fields = [
            'expression',
            'person',
            'role'
        ]


class ExpressionContributorCreateView(ExpressionRelationCreateView, ExpressionContributorView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Beteiligten für Expression { self.get_expression() } anlegen"
        return context


class ExpressionContributorUpdateView(ExpressionRelationUpdateView, ExpressionContributorView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Beteiligten { self.object.person } von Expression { self.get_expression() } bearbeiten"
        return context


class ExpressionContributorDeleteView(ExpressionRelationDeleteView):
    model = ExpressionContributor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Expression { self.object } an Expression { self.get_expression() } löschen"
        return context


class ExpressionView(generic.edit.ModelFormMixin):
    model = Expression
    fields = [
            'incipit_music',
            'incipit_text',
            'period_comment',
            'history',
            'work'
        ]


class ExpressionCreateView(WorkRelationCreateView, ExpressionView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Neue Expression am Werk { self.get_work() } anlegen"
        return context


class ExpressionUpdateView(WorkRelationUpdateView, ExpressionView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Expression { self.object } von Werk { self.get_work() } bearbeiten"
        return context


class ExpressionDeleteView(WorkRelationDeleteView):
    model = Expression

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Expression { self.object } am Werk { self.get_work() } löschen"
        return context


class WorkTitleUpdateView(WorkRelationUpdateView, WorkTitleView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Titel { self.object } des Werks { self.get_work() } bearbeiten"
        return context


class WorkTitleDeleteView(WorkRelationDeleteView):
    model = WorkTitle

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = f"Titel { self.object } des Werks { self.get_work() } löschen"
        return context


class WorkDetailView(generic.detail.DetailView):
    model = Work

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_work_targets'] = RelatedWork.objects.filter(source_work=self.object)
        context['related_work_sources'] = RelatedWork.objects.filter(target_work=self.object)
        context['contributors'] = WorkContributor.objects.filter(work=self.object)
        return context

def person_list(request):
    persons = [
            f"{person.names.get(status=Status.PRIMARY).last_name}_{person.names.get(status=Status.PRIMARY).first_name}-{person.gnd_id}"
            for person
            in Person.objects.all()
        ]
    serialized_persons = json_dump(persons)
    return HttpResponse(serialized_persons, content_type='application/json')
