from django.urls import path

from patient_portal import views

urlpatterns = [
    path("book", views.book_doctor, name="book_doctor"),
    path("book/time", views.book_time, name="book_time"),
    path("book/confirm", views.book_confirm, name="book_confirm"),
    path("me/appointments", views.my_appointments, name="my_appointments"),
]
