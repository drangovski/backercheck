from django.conf import settings
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.conf.urls.static import static
from projects.models import Project

def csv_upload(instance, filename):
	return 'mailing-csv/%s/%s' %(instance.creator.username, filename)

class MailingList(models.Model):
	email = models.CharField(max_length=260, blank=True, null=True)
	created_on = models.DateField(default=datetime.now)
	creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

	def email_backed_projects(self):
		backer = self.email
		backed = Project.objects.filter(backers__email=backer)

		return backed

	def __str__(self):
		return self.email

class MailingListCsv(models.Model):
	csv = models.FileField(upload_to=csv_upload, null=True, blank=True)
	created_on = models.DateField(default=datetime.now)
	creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return self.csv