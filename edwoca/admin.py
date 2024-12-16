from django.contrib import admin
from .models import Work
from .models import Title

# Register your models here.
class TitleInline(admin.TabularInline):
    model = Title

class WorkAdmin(admin.ModelAdmin):
    #list_display = ('title')
    inlines = [TitleInline]

admin.site.register(Work, WorkAdmin)
