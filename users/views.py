from django.shortcuts import render
from django.views.generic import View, DetailView

from users.models import User, UserProfile


class UsersView(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, "users/users.html", {"user_list": users})

    # model = User
    # queryset = User.objects.all()


class UserDetailView(UsersView, DetailView):
    model = User
