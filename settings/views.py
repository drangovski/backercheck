from datetime import datetime, date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required
from .forms import settingsPersonal, settingsImage
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def settings(request):

	# Change Image
	userprofileid = UserProfile.objects.get(user_id=request.user.id)

	newForm = settingsImage(instance=userprofileid)

	if request.method == 'POST' and 'settingsImage' in request.POST:
		newForm = settingsImage(request.POST, request.FILES, instance=userprofileid)
		if newForm.is_valid():
			newForm.save()
			return redirect('{}?tab=personal'.format(reverse('settings')))
		else:
			return redirect('projects')
	else:
		newForm = settingsImage(instance=userprofileid)



	user = request.user

	# Personal Settings
	form = settingsPersonal(instance=user)

	if request.method == 'POST' and 'settingsPersonal' in request.POST:
		form = settingsPersonal(request.POST, instance=user)
		if form.is_valid():
			form.save()
			return redirect('{}?tab=personal'.format(reverse('settings')))
		else:
			return redirect('projects')

	else:
		form = settingsPersonal(instance=user)


	# Security Settings
	if request.method == 'POST' and 'settingsSecurity' in request.POST:
		changePassForm = PasswordChangeForm(request.user, request.POST)
		if changePassForm.is_valid():
			user = changePassForm.save()
			update_session_auth_hash(request, changePassForm.user)
			return redirect('{}?tab=security'.format(reverse('settings')))
		else:
			return redirect('projects')
	else:
		changePassForm = PasswordChangeForm(request.user)

	context = {
		'form': form,
		'user': user,
		'changePassForm': changePassForm,
		'newForm': newForm,
	}


	return render(request, 'settings.html', context)