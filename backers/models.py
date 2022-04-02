from django.conf import settings
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.conf.urls.static import static
from projects.models import Project
from emails.models import MailingList

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Sum, Count

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

class Backer(models.Model):
	pid = models.IntegerField(blank=True, null=True)
	backer_number = models.CharField(max_length=160, blank=True, null=True)
	backer_uid = models.CharField(max_length=160, blank=True, null=True)
	name = models.CharField(max_length=200, blank=True, null=True)
	email = models.CharField(max_length=200, blank=True, null=True)
	shipping_country = models.CharField(max_length=200, blank=True, null=True)
	shipping_amount = models.CharField(max_length=200, blank=True, null=True)
	reward_title = models.CharField(max_length=300, blank=True, null=True)
	backing_minimum = models.CharField(max_length=200, blank=True, null=True)
	reward_id = models.CharField(max_length=200, blank=True, null=True)
	pledge_amount = models.CharField(max_length=200, blank=True, null=True)
	pledged_at = models.CharField(max_length=200, blank=True, null=True)
	rewards_sent = models.CharField(max_length=200, blank=True, null=True)
	pledged_status = models.CharField(max_length=200, blank=True, null=True)
	notes = models.TextField(blank=True, null=True)
	created_on = models.DateField(default=datetime.now)

	def get_backed_project(self):
	
		backer = self.email
		current_project = Project.objects.get(pk=self.pid)
		backed = Project.objects.filter(Q(backers__email=backer) & Q(started__lt=current_project.started)).exclude(pk=self.pid)

		return backed

	def get_all_backed_projects(self):
		backer = self.email
		backed = Project.objects.filter(backers__email=backer)

		return backed

	def checkMailingList(self):
		email = self.email
		backed = MailingList.objects.filter(email=email)

		return backed

	def __str__(self):
		return self.email

@receiver(post_delete, sender=Backer)
def object_post_delete_handler(sender, instance, **kwargs):
     cache.clear()

class Backed(models.Model):
	backer = models.ForeignKey(Backer, on_delete=models.CASCADE, related_name="backedbacker")
	project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="backedproject")