from django.contrib import messages
from django.http import HttpRequest

from logic.users_logic import UserUploader
from django.test import RequestFactory, TestCase


class File:
    name: str


file_1 = File()
file_2 = File()
file_3 = File()
rf = RequestFactory()
request = rf.get('/')
request._messages = messages.storage.default_storage(request)


def test_check_file_number_name_success():
    file_1.name, file_2.name = 'file_1.csV', 'file_2.Xml'
    result = UserUploader.check_file_number_and_extensions((file_1, file_2), request)
    assert result == {'csv': file_1, 'xml': file_2}


def test_check_file_number_fail():
    file_1.name, file_2.name, file_3.name = 'file_1.csv', 'file_2.xml', 'file_2.xml'
    result = UserUploader.check_file_number_and_extensions((file_1,), request)
    assert result is None
    result = UserUploader.check_file_number_and_extensions((file_1, file_2, file_3), request)
    assert result is None


def test_check_file_name_fail():
    file_1.name, file_2.name = 'file_1.csv', 'file_2.xls'
    result = UserUploader.check_file_number_and_extensions((file_1, file_2), request)
    assert result is None
