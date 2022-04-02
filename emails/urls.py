from django.urls import path

from . import views

urlpatterns = [
	path('mailing-list/', views.emails, name="emails"),
]