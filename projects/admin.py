from django.contrib import admin

from .models import Project, CsvFile

admin.site.register(Project)
admin.site.register(CsvFile)
