from django.conf import settings
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.conf.urls.static import static

from imagekit.models import ProcessedImageField
from imagekit.processors import SmartResize

def upload_to(instance, filename):
	return 'images/%s/%s' %(instance.user.username, filename)


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(blank=True, null=True)
	image = ProcessedImageField(upload_to=upload_to, processors=[SmartResize(105, 105)], format='JPEG', options={'quality': 100}, null=True, blank=True)

	def __str__(self):
		return str(self.user.email)