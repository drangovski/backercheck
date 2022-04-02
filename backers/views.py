from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Backer, Backed
from projects.models import Project

@login_required
def backers(request):

	creator_id = request.user.id

	projects = Project.objects.filter(creator_id=creator_id)

	backers = Backer.objects.filter(backers__in=projects).distinct('email')

	context = {
		'backers': backers,
	}

	return render(request, 'backers.html', context)

@login_required
def backerDetails(request, project_id, backer_id):

	creator_id = request.user.id

	# Get project
	project = get_object_or_404(Project, pk=project_id, creator_id=creator_id)

	# Get backers
	backer = project.backers.get(pk=backer_id)

	context = {
		'backer': backer
	}

	return render(request, 'backer-details.html', context)