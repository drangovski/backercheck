from django.db import models
from .models import Project, CsvFile
from django import forms


class setProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ("title", "description", "image", "funding", "goal", "backers_count", "started", "ended",)

		def __init__(self, *args, **kwargs):
			super(setProjectForm, self).__init__(*args, **kwargs)


class csvUploadForm(forms.ModelForm):
	csv = forms.FileField(widget=forms.FileInput(attrs={'onchange': 'document.getElementById("csvUpload").click()'}))

	class Meta:
		model = CsvFile
		fields = ("csv",)

		def __init__(self, *args, **kwargs):
			super(csvUploadForm, self).__init__(*args, **kwargs)