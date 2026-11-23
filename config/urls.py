from django.urls import include, path

from core import views as core_views

urlpatterns = [
    path("", core_views.home, name="home"),
    path("healthz", core_views.healthz, name="healthz"),
    path("", include("accounts.urls")),
    path("manage/", include("scheduling.urls")),
    path("", include("patient_portal.urls")),
    path("", include("staff_portal.urls")),
]
