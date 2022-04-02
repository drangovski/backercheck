from django.db import models
from .models import MailingListCsv
from django import forms


class mailingUploadForm(forms.ModelForm):
	csv = forms.FileField(widget=forms.FileInput(attrs={'onchange': 'document.getElementById("csvUpload").click()'}))
	
	class Meta:
		model = MailingListCsv
		fields = ("csv",)

		def __init__(self, *args, **kwargs):
			super(mailingUploadForm, self).__init__(*args, **kwargs)