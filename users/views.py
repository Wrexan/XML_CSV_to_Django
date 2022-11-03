from django.shortcuts import render, redirect
from django.views.generic import View, FormView

from .forms import FileFieldForm
from .models import User
from logic.users_logic import UserUploader


class UsersView(View):
    def get(self, request):
        if request.user.is_superuser:
            users = User.objects.all()
        else:
            users = None
        return render(request, "users/users.html", {"user_list": users})


class UserProfileView(View):
    def get(self, request, pk):
        if request.user.is_superuser:
            user_profile = User.objects.get(id=pk)
            return render(request, "users/user_profile.html", {"user_profile": user_profile})
        return redirect('/')


class UsersUploadFileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = 'users/upload.html'
    success_url = "/"

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return render(request, "users/upload.html")
        return redirect('/')

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            files = request.FILES.getlist('files')
            if form.is_valid():
                uploader = UserUploader()
                uploader.handle_uploaded_files(request, files)
                return super().form_valid(form)
            else:
                return self.form_invalid(form)
        return redirect('/')
