from django.db import models
from django import forms
from django.contrib.auth.models import User
from accounts.models import UserProfile

class settingsImage(forms.ModelForm):
	image = forms.ImageField(widget=forms.FileInput(attrs={'onchange': 'document.getElementById("settingsImage").click()'}))

	class Meta:
		model = UserProfile
		fields = ["image"]

class settingsPersonal(forms.ModelForm):

	class Meta:
		model = User
		fields = ("first_name", "last_name")

