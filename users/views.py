from django.shortcuts import render
from django.views.generic import View, FormView

from .forms import FileFieldForm
from .models import User


class UsersView(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, "users/users.html", {"user_list": users})


class UserProfileView(View):
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        return render(request, "users/user_profile.html", {"user": user})


class UsersUploadFileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = 'users/upload.html'
    success_url = "/"

    def get(self, request, *args, **kwargs):
        return render(request, "users/upload.html")

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('files')
        if form.is_valid():
            self.handle_uploaded_files(files)
            return super().form_valid(form)
        else:
            print(f'form is invalid: {form.__dict__=}')
            return self.form_invalid(form)

    def handle_uploaded_files(self, files):
        print(f'{files=}')
        pass
