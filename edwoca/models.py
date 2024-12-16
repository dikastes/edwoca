from django.db import models
from django.utils.translation import gettext_lazy as _

# ToDo replace this by some standard way?
class Language(models.TextChoices):
    FRENCH = 'FR', _('fr')
    GERMAN = 'GE', _('ge')
    ENGLISH = 'EN', _('en')

# Create your models here.
class Work(models.Model):
    class Meta:
        ordering = ['work_catalog_number']

    gnd_id = models.CharField(max_length=20, unique=True, null=True)
    work_catalog_number = models.CharField(max_length=20, unique=True, null=True)
    related_work = models.ManyToManyField('Work', through='RelatedWork')
    #title = models.OneToOneField('Title')
    #alternative_titles = models.ForeignKey('Title',related_name="alternative_title")
    history = models.TextField()

    def __str__(self):
        return '%s: %s' % (self.work_catalog_number, self.titles.get(status=Title.Status.PRIMARY).title)

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
    class Status(models.TextChoices):
        PRIMARY = 'P', _('Primary')
        ALTERNATIVE = 'A', _('Alternative')

    class Meta:
        ordering = ['title']

    title = models.CharField(max_length=100)
    status = models.CharField(max_length=1,choices=Status,default=Status.PRIMARY)
    language = models.CharField(max_length=2,choices=Language,default=Language.GERMAN)
    work = models.ForeignKey('Work', on_delete=models.CASCADE, related_name='titles')

    def is_upperclass(self):
        return self.language in {
            Language.FRENCH,
            Language.GERMAN,
            Language.ENGLISH
        } and self.status in {
            self.Status.PRIMARY,
            self.Status.ALTERNATIVE
        }

    def __str__(self):
        return self.title

