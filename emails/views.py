import csv, io
from datetime import datetime, date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from projects.models import Project, CsvFile
from backers.models import Backer, Backed
from .models import MailingList
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import mailingUploadForm
from django.db.models import Case, Count, IntegerField, Sum, When, Q

@login_required
def emails(request):
    creator_id = request.user.id

    mailing_list = MailingList.objects.filter(creator_id=creator_id)

    # CSV UPLOAD
    csvform = mailingUploadForm()
    if request.method == 'POST':
        csvform = mailingUploadForm(request.POST, request.FILES)
        if csvform.is_valid():
            csvform = csvform.save(commit=False)
            csvform.creator_id = creator_id
            csvform.save()

            # READ CSV
            csv_file = csvform.csv

            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            for column in csv.reader(io_string, delimiter=',', quotechar='"'):
                _, created = MailingList.objects.update_or_create(
                    email=column[0],
                    creator_id=creator_id
                    )

            return redirect('emails')
    else:
        csvform = mailingUploadForm()

    all_projects = Project.objects.filter(creator_id=creator_id)
    backers_emails = Backer.objects.filter(backers__in=all_projects).values('email').distinct()
    mailing_emails = mailing_list.values('email').distinct()

    mailing_backers = mailing_emails.intersection(backers_emails)    

    context = {
        'csvform': csvform,
        'mailing_list': mailing_list,
        'mailing_backers': mailing_backers,
    }

    return render(request, 'mailing-list.html', context)