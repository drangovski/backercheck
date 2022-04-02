import csv, io
from datetime import datetime, date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Project, CsvFile
from backers.models import Backer, Backed
from emails.models import MailingList
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import setProjectForm, csvUploadForm
from django.db.models import Case, Count, IntegerField, Sum, When, Q
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from django.urls import reverse
from django.http import HttpRequest
from django.utils.cache import get_cache_key


@login_required
def projects(request):
	creator_id = request.user.id

	projects = Project.objects.filter(creator_id=creator_id)

	context = {
		'projects': projects,
	}

	return render(request, 'projects.html', context)

@login_required
@cache_page(60 * 15, key_prefix="project_cache")
def project(request, project_id):
	creator_id = request.user.id

	# Get project
	project = get_object_or_404(Project, pk=project_id, creator_id=creator_id)

	# Get all backers
	all_backers = project.backers.all().distinct()

	# CSV UPLOAD
	csvform = csvUploadForm()
	if request.method == 'POST':
		cache.clear()
		csvform = csvUploadForm(request.POST, request.FILES)
		if csvform.is_valid():
			csvform = csvform.save(commit=False)
			csvform.for_project_id = project_id
			csvform.creator_id = creator_id
			csvform.save()

			# READ CSV
			csv_file = csvform.csv
			
			data_set = csv_file.read().decode('UTF-8')
			io_string = io.StringIO(data_set)
			next(io_string)
			
			backers_list = csv.reader(io_string, delimiter=',', quotechar='"')
		
			objs = [
				Backer(
					backer_number=row[0],
					backer_uid=row[1],
					name=row[2],
					email=row[3],
					shipping_country=row[4],
					shipping_amount=row[5],
					reward_title=row[6],
					backing_minimum=row[7],
					reward_id=row[8],
					pledge_amount=row[9],
					rewards_sent=row[10],
					pledged_status=row[11],
					notes=row[12],
					pid=project_id
				)
				for row in backers_list
			]
			try:
				msg = Backer.objects.bulk_create(objs)
			except Exception as e:
				print('Error While Importing Data: ',e)


			# Add backer_id and project_id in Backed 
			new_backers = list(Backer.objects.filter(pid=project_id).values_list('id', flat=True))

			backed_ids = [
				Backed(
					backer_id=bid,
					project_id=project_id
				)
				for bid in new_backers
			]
			try:
				msg = Backed.objects.bulk_create(backed_ids)
			except Exception as e:
				print('Error While Importing Data: ',e)

			return redirect('project', project_id=project_id)
	else:
		csvform = csvUploadForm()

	####   RETURNING BACKERS   ####

	# 1. Get Current Backers by Email
	current_backers = all_backers.values('email').distinct()

	# 2. Get Previous Projects
	previous_projects = Project.objects.filter(Q(creator_id=creator_id) & Q(started__lt=project.started))

	# 3. Get All Backers for Previous Projects
	previous_backers = Backer.objects.filter(backers__in=previous_projects).values('email').distinct()

	# 4. Get Returning Backers
	returning_backers = current_backers.intersection(previous_backers)
	
	# 5. Count Returning Backers
	count_returning = returning_backers.count()

	####   NEW BACKERS   ####
	# 1. Get New Backers
	new_backers = current_backers.difference(previous_backers)

	# 2. Count New Backers
	count_new = new_backers.count()


	### LOCATION ###
	loc = all_backers.values("shipping_country").order_by("shipping_country").annotate(loc_count=Count('shipping_country')).order_by('-loc_count')


	### RETURNING FROM PROJECT ###
	returning_from_project = previous_projects.filter(backers__email__in=returning_backers).annotate(project_count=Sum(Case(When(backers__email__in=returning_backers, then=1), default=0, output_field=IntegerField()))).order_by('-project_count').exclude(pk=project_id)

	### MAILING LIST ###
	mailing_list = MailingList.objects.filter(creator_id=creator_id)

	mailing_list = mailing_list.values('email').distinct()

	mailing_backers = current_backers.intersection(mailing_list)

	context = {
		'project': project,
		'csvform': csvform,
		'project_id': project_id,
		'all_backers': all_backers,
		'current_backers': current_backers,
		'previous_projects':previous_projects,
		'previous_backers': previous_backers,
		'returning_backers': returning_backers,
		'count_returning': count_returning,
		'new_backers': new_backers,
		'count_new': count_new,
		'loc': loc,
		'returning_from_project': returning_from_project,
		'mailing_backers': mailing_backers,
	}

	return render(request, 'project.html', context)


@login_required
def deleteBackersList(request, project_id):
	creator_id = request.user.id

	# Get project
	project = get_object_or_404(Project, pk=project_id, creator_id=creator_id)

	# Get all backers
	all_backers = project.backers.all()

	all_backers.delete()

	cache.delete('project_cache')
	
	return redirect('project', project_id)

@login_required
def deleteBacker(request, backer_id):
	
	backer = Backer.objects.get(pk=backer_id)

	project_id = backer.pid

	backer.delete()

	return redirect('project', project_id)

@login_required
def deleteProject(request, project_id):

	project = Project.objects.get(pk=project_id)
	project.delete()

	backers = Backer.objects.filter(pid=project_id)
	backers.delete()

	return redirect('projects')

@login_required
def addProject(request):
	creator_id = request.user.id

	form = setProjectForm()
	if request.method == 'POST':
		form = setProjectForm(request.POST, request.FILES)
		if form.is_valid():
			form = form.save(commit=False)
			form.creator_id = creator_id
			form.save()
			return redirect('projects')
	else:
		form = setProjectForm()

	context = {
		'form': form,
	}

	return render(request, 'add-project.html', context)

@login_required
def editProject(request, project_id):
	creator_id = request.user.id

	project = get_object_or_404(Project, pk=project_id, creator_id=creator_id)

	form = setProjectForm(instance=project)
	if request.method == 'POST':
		form = setProjectForm(request.POST, request.FILES, instance=project)
		if form.is_valid():
			form = form.save(commit=False)
			form.creator_id = creator_id
			form.save()
			return redirect('project', project_id)
	else:
		form = setProjectForm(instance=project)

	context = {
		'form': form,
		'project_id': project_id
	}

	return render(request, 'edit-project.html', context)