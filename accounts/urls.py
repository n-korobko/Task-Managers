from django.urls import path, include
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("", include("django.contrib.auth.urls")),
]