from django.contrib import messages
from django.shortcuts import render
from django.views.generic import View, FormView
import xml.etree.ElementTree as ET

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
            self.handle_uploaded_files(request, files)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def handle_uploaded_files(self, request, files):
        errors = {"csv": "Expected CSV and XML file. CSV absent",
                  "xml": "Expected CSV and XML file. XML absent"}
        files_by_ext = {}
        if len(files) != 2:
            errors['AMT'] = f"There must be 2 files, you're trying to upload {len(files)}"
        for file in files:
            extension = file.name.lower()[-3:]
            if extension in errors:
                files_by_ext[extension] = file
                del errors[extension]
        if errors:
            [messages.error(request, message) for message in errors.values()]
            return
        # csv_dicts = self.csv_file_rows_to_dict(files_by_ext['csv'])
        xml_dicts = self.xml_file_rows_to_dict(files_by_ext['xml'])

    # @staticmethod
    # def csv_file_rows_to_dict(lst: list) -> dict:
    #     """Parse .csv rows using header format
    #     returns: [dict{first_name: *, last_name: *, avatar: *}]"""
    #     if isinstance(lst[0], bytes):
    #         stringed_dict = {}
    #         for row in lst:
    #             if len(row) > 2:
    #                 string = row.decode(encoding='utf-8', errors='strict')
    #                 stringed_dict[string[0:3]] = string[3:].rstrip()
    #         return stringed_dict
    #     return {row[0:3]: row[3:].rstrip() for row in lst if len(row) > 2}

    def xml_file_rows_to_dict(self, file) -> [dict]:
        """Parse abbreviations rows using abbreviations format
        returns: [dict{first_name: *, last_name: *, avatar: *}]"""
        users = []
        tree = ET.parse(file)
        root_user_in_tree = tree.find('user')
        users_in_tree = root_user_in_tree.find('users')
        for user in users_in_tree:
            first_name = self.clean_text_in_brackets(user.find('first_name').text)
            last_name = self.clean_text_in_brackets(user.find('last_name').text)
            avatar = user.find('avatar').text
            if first_name and last_name and avatar:
                users.append({'first_name': first_name,
                              'last_name': last_name,
                              'avatar': avatar})
        return users

    @staticmethod
    def clean_text_in_brackets(text: str or None) -> str or None:
        if text:
            cutter = {}
            for i, symbol in enumerate(text):
                if symbol in '([':
                    cutter['start'] = i
                    break
            for i, symbol in enumerate(text[::-1]):
                if symbol in ')]':
                    cutter['end'] = i
                    break
            if len(cutter) == 2:
                print(f'{text=} {cutter=}')
                return f"{text[:cutter['start']]}{text[len(text)-cutter['end']:]}".strip()
            return text
