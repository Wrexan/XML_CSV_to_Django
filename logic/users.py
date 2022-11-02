import codecs
import csv
from datetime import datetime
import xml.etree.ElementTree as ET

from django.db import IntegrityError
from django.utils import timezone

from django.contrib import messages

from users.models import User


class UserUploader:

    def handle_uploaded_files(self, request, files) -> None:
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
        csv_dicts = self.csv_file_rows_to_dict(files_by_ext['csv'])
        xml_dicts = self.xml_file_rows_to_dict(files_by_ext['xml'])
        users_dicts = self.unite_files_data(csv_dicts, xml_dicts)
        self.insert_users_to_db(request, users_dicts)

    @staticmethod
    def insert_users_to_db(request, users_dict: [dict]) -> None:
        users_success = 0
        users_amount = len(users_dict)
        errors = {}
        for user_data in users_dict:
            errored_username = user_data['username']
            try:
                user = User.objects.create_user(
                    username=user_data['username'],
                    password=user_data['password'],
                    date_joined=datetime.fromtimestamp(int(user_data['date_joined']), tz=timezone.utc),
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                )
                User.save(user)
                users_success += 1
            except IntegrityError as err:
                if len(errors) < 5:
                    errors[errored_username] = err
        if users_success == users_amount:
            messages.success(request, f'Successfully uploaded all {users_success} users')
        if users_success > 0:
            messages.info(request, f'Successfully uploaded {users_success} users of {users_amount}')
        [messages.warning(request, f'{user}: {error}') for user, error in errors.items()]

    def csv_file_rows_to_dict(self, file) -> [dict]:
        """Parse .csv rows using header format
        returns: [dict{username: *, password: *, date_joined: *}]"""
        users = []
        reader = csv.DictReader(codecs.iterdecode(file, 'utf-8'), delimiter=',', lineterminator='\r\n')
        for row in reader:
            if 'username' in row and 'password' in row and 'date_joined' in row:
                row['username'] = self.clean_text_in_brackets(row['username'])
                if row['username'] and row['password'] and row['date_joined']:
                    users.append(row)
        return users

    def xml_file_rows_to_dict(self, file) -> [dict]:
        """Parse *.xml tree to get users
        returns: [dict{first_name: *, last_name: *, avatar: *}]"""
        users = []
        tree = ET.parse(file)
        root_user_in_tree = tree.find('user')
        users_in_tree = root_user_in_tree.find('users')
        for user in users_in_tree:
            first_name = self.clean_text_in_brackets(user.find('first_name').text)
            last_name = self.clean_text_in_brackets(user.find('last_name').text)
            avatar_url = user.find('avatar').text
            if first_name and last_name and avatar_url:
                users.append({'first_name': first_name,
                              'last_name': last_name,
                              'avatar_url': avatar_url})
        return users

    @staticmethod
    def unite_files_data(csv_dicts: [dict], xml_dicts: [dict]) -> [dict]:
        """aggregate two dicts if their users looks the same"""
        united_users = []
        for i, user_profile_data in enumerate(xml_dicts):
            for k, user_login_data in enumerate(csv_dicts):
                if user_profile_data['last_name'] in user_login_data['username']:
                    unite = csv_dicts.pop(k)
                    unite.update(user_profile_data)
                    united_users.append(unite)
                    break
        return united_users

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
                return f"{text[:cutter['start']]}{text[len(text) - cutter['end']:]}".strip()
            return text
