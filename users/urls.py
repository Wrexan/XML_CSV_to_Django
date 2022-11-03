import django.contrib.auth
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.UsersView.as_view()),
    path("<int:pk>/", views.UserProfileView.as_view()),
    path("upload/", views.UsersUploadFileFieldFormView.as_view()),
    path("", include('django.contrib.auth.urls'))
]
