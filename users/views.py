from django.shortcuts import render
from django.views.generic import View

from users.models import User, UserProfile


class UsersView(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, "users/users.html", {"user_list": users})

    # model = User
    # queryset = User.objects.all()


class UserProfileView(View):
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        return render(request, "users/user_profile.html", {"user": user})
