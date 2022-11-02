from django.urls import path
from . import views

urlpatterns = [
    path("", views.UsersView.as_view()),
    path("<int:pk>/", views.UserProfileView.as_view()),
    path("upload/", views.UsersUploadView.as_view())
]
