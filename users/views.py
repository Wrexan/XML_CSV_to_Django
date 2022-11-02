from django.shortcuts import render
from django.views.generic import View

from users.models import User, UserProfile


class UsersView(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, "users/users.html", {"user_list": users})


class UserProfileView(View):
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        return render(request, "users/user_profile.html", {"user": user})


class UsersUploadView(View):
    def get(self, request):
        return render(request, "users/upload.html")

    def post(self, request):
        return render(request, "users/upload.html")
