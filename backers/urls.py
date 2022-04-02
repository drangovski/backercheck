from django.urls import path

from . import views

urlpatterns = [
	path('backers/', views.backers, name="backers"),
	path('backers/<project_id>/<backer_id>', views.backerDetails, name="backerDetails"),
]