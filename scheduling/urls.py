from django.urls import path

from scheduling import views

urlpatterns = [
    path("hours", views.working_hours, name="working_hours"),
]
