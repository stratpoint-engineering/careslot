from django.urls import path

from staff_portal import views

urlpatterns = [
    path("desk/day", views.desk_day, name="desk_day"),
    path("desk/book", views.desk_book, name="desk_book"),
    path("desk/appointments/<int:appointment_id>", views.desk_appointment, name="desk_appointment"),
    path("doctor/day", views.doctor_day, name="doctor_day"),
]
