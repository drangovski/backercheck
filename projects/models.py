from django.conf import settings
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.conf.urls.static import static

from imagekit.models import ProcessedImageField
from imagekit.processors import SmartResize

def upload_to(instance, filename):
	# Remember to change this to username
	return 'images/%s/%s' %(instance.creator.username, filename)

def csv_upload(instance, filename):
	return 'csv/%s/%s' %(instance.for_project.creator.username, filename)

class Project(models.Model):
	backers = models.ManyToManyField(to='backers.Backer', through='backers.Backed', related_name="backers")
	title = models.CharField(max_length=160)
	description = models.TextField()
	image = ProcessedImageField(upload_to=upload_to, processors=[SmartResize(290, 290)], format='JPEG', options={'quality': 100}, null=True, blank=True)
	funding = models.IntegerField()
	goal = models.IntegerField()
	backers_count = models.IntegerField(null=True, blank=True)
	started = models.DateField()
	ended = models.DateField()
	created_on = models.DateField(default=datetime.now)
	creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return self.title

class CsvFile(models.Model):
	for_project = models.ForeignKey(Project, on_delete=models.CASCADE)
	creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	csv = models.FileField(upload_to=csv_upload, null=True, blank=True)
	created_on = models.DateField(default=datetime.now)