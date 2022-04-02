from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def populateReportModel(instance, sender, **kwargs):
	if sender is User:
		if kwargs["created"]:
			UserProfile.objects.create(bio=None, image=None, user_id=instance.id)


def login(request):
	if request.method == 'POST':
		username = request.POST['username']		
		password = request.POST['password']	

		user = auth.authenticate(username=username, password=password)

		if user is not None:
			auth.login(request, user)
			return redirect('projects')
		else:
			return redirect('login')

	else:		
		return render(request, 'login.html')

@login_required
def logout(request):
	if request.user.is_authenticated:
		auth.logout(request)
		return redirect('login')

@login_required
def deleteAccount(request):

	if request.user.is_authenticated:
		user = User.objects.get(pk=request.user.id)
		user.delete()
		auth.logout(request)
		return redirect('login')

	return render(request, '/login')