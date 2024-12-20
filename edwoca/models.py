from django.db import models
from django.utils.translation import gettext_lazy as _
from dmad_on_django.models import Language, Status, Person
from xml.etree import ElementTree as ET
from iso639 import to_iso639_1

# Create your models here.
class Work(models.Model):
    class Meta:
        ordering = ['work_catalog_number']

    gnd_id = models.CharField(max_length=20, unique=True, null=True)
    work_catalog_number = models.CharField(max_length=20, unique=True, null=True)
    related_work = models.ManyToManyField('Work', through='RelatedWork')
    history = models.TextField()

    def __str__(self):
        return '%s: %s' % (self.work_catalog_number, self.titles.get(status=Status.PRIMARY).title)

    def to_mei(self):
        work = ET.Element('work')

        for title in self.titles.all():
            work.append(title.to_mei())

        gnd_id = ET.Element('identifier')
        gnd_id.attrib['label'] = 'GND'
        gnd_id.text = self.gnd_id

        work_catalog_number = ET.Element('identifier')
        work_catalog_number.attrib['label'] = 'LQWV'
        work_catalog_number.text = self.work_catalog_number

        history = ET.Element('history')
        history.text = self.history

        contributors = ET.Element('contributor')
        for contributor in self.contributors.all():
            contributors.append(contributor)

        work.append(gnd_id)
        work.append(work_catalog_number)
        work.append(history)

        return work

class Contributor(models.Model):
    class Role(models.TextChoices):
        COMPOSER = 'CP', _('Composer')
        WRITER = 'WR', _('Writer')
        TRANSLATOR = 'TR', _('Translator')
        POET = 'PT', _('Poet')
        DEDICATEE = 'DD', _('Dedicatee')

    work = models.ForeignKey(
        'Work',
        on_delete=models.CASCADE,
        related_name='contributors'
    )
    person = models.ForeignKey(
        'dmad.Person',
        on_delete=models.CASCADE,
        related_name='contributed_to'
    )
    role = models.CharField(max_length=10, choices=Role, default=Role.COMPOSER)

    def to_mei(self):
        contributor = ET.Element('persName')
        contributor.attrib['role'] = self.role
        contributor.attrib['auth'] = 'GND'
        contributor.attrib['auth.uri'] = 'd-nb.info/gnd'
        contributor.attrib['codedval'] = self.person.gnd_id
        contributor.text = self.person.name

        return contributor

class RelatedWork(models.Model):
    class Label(models.TextChoices):
        PARENT = 'PR', _('Parent')
        RELATED = 'RE', _('Related')

    source_work = models.ForeignKey('Work',on_delete=models.CASCADE, related_name="source_work_of")
    target_work = models.ForeignKey('Work',on_delete=models.CASCADE, related_name="target_work_of")
    comment = models.TextField()
    label = models.CharField(max_length=2,choices=Label,default=Label.PARENT)

    def is_upperclass(self):
        return self.label in {
            self.Label.PARENT,
            self.Label.RELATED
        }

class Title(models.Model):
    class Meta:
        ordering = ['title']

    title = models.CharField(max_length=100)
    status = models.CharField(max_length=1,choices=Status,default=Status.PRIMARY)
    language = models.CharField(max_length=15, choices=Language, default=Language['DE'])
    work = models.ForeignKey('Work', on_delete=models.CASCADE, related_name='titles')

    #def is_upperclass(self):
        #return self.language in {
            #Language.FRENCH,
            #Language.GERMAN,
            #Language.ENGLISH
        #} and self.status in {
            #self.Status.PRIMARY,
            #self.Status.ALTERNATIVE
        #}

    def __str__(self):
        return self.title

    def to_mei(self):
        title = ET.Element('title')
        if self.status == Status.ALTERNATIVE:
            title.attrib['type'] = 'alternative'
        title.text = self.title
        title.attrib['lang'] = to_iso639_1(self.language)
        return title
