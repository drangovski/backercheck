from django.urls import path

from . import views

urlpatterns = [
	path('projects/', views.projects, name="projects"),
	path('project/<project_id>', views.project, name="project"),
	path('add-project/', views.addProject, name="addproject"),
	path('edit-project/<project_id>', views.editProject, name="editproject"),
	path('delete-backers/<project_id>', views.deleteBackersList, name="deletebackers"),
	path('delete-backer/<backer_id>', views.deleteBacker, name="deletebacker"),
	path('delete-project/<project_id>', views.deleteProject, name="deleteproject"),
]