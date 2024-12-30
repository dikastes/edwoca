from .models import WorkTitle
from django.forms import ModelForm

class WorkTitleForm(ModelForm):
    class Meta:
        model = WorkTitle
        fields = [
                'title',
                'status',
                'language'
            ]
