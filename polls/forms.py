from django.forms import ModelForm
from polls.models import Report
from polls.models import Folder
from django.db import models



class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ['subject', 'long_text', 'short_text', 'file', 'private', 'location', 'kw']


class FolderForm(ModelForm):
    class Meta:
        model = Folder
        fields = ['name']