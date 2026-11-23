from django.urls import path

from accounts import views

urlpatterns = [
    path("signin", views.signin, name="signin"),
    path("signout", views.signout, name="signout"),
    path("register", views.register, name="register"),
    path("manage/staff", views.staff_accounts, name="staff_accounts"),
]
