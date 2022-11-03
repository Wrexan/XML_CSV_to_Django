from copy import copy
from xml.etree.ElementTree import ParseError

from django.contrib import messages
from io import StringIO

from logic.users_logic import UserUploader
from django.test import RequestFactory, TestCase


class File:
    name: str


U = UserUploader()
file_1 = File()
file_2 = File()
file_3 = File()
rf = RequestFactory()
request = rf.get('/')
request._messages = messages.storage.default_storage(request)

test_csv_content = [b'username,password,date_joined\r\n',
                    b'M.Steam,ASDf43f#$dsD,1638700932\r\n',
                    b'V.Markus,DSA4FSFF54w%$#df,1464014817\r\n',
                    b'M.Stone,Lkds(*dsdadf,1466078973']

test_csv_result = [{'username': 'M.Steam', 'password': 'ASDf43f#$dsD', 'date_joined': '1638700932'},
                   {'username': 'V.Markus', 'password': 'DSA4FSFF54w%$#df', 'date_joined': '1464014817'},
                   {'username': 'M.Stone', 'password': 'Lkds(*dsdadf', 'date_joined': '1466078973'}]

test_xml_content = '<user_list>\r\n' \
                   '<user>\r\n' \
                   '<name>Users Test Task XML</name>\r\n' \
                   '<company>CxDojo</company>\r\n' \
                   '<users>\r\n' \
                   '<user id="6">\r\n' \
                   '<first_name>Max</first_name>\r\n' \
                   '<last_name>St(dsa53d)eam</last_name>\r\n' \
                   '<avatar>https://pbs.twimg.com/media/BcINeMVCIAABeWd.jpg</avatar>\r\n' \
                   '</user>\r\n' \
                   '<user id="1">\r\n' \
                   '<first_name>Anton</first_name>\r\n' \
                   '<last_name>Mechailov</last_name>\r\n' \
                   '<avatar>https://mir-s3-cdn-cf.behance.net/project_modules/2800_opt_1/35af6a41332353.57a1ce913e889.jpg</avatar>\r\n' \
                   '</user>\r\n' \
                   '<user id="54">\r\n' \
                   '<first_name>Valerii</first_name>\r\n' \
                   '<last_name>Jmishenko</last_name>\r\n' \
                   '<avatar>https://static.boredpanda.com/blog/wp-content/uploads/2017/04/Virrappan2-58f79980ae6fb__880.jpg</avatar>\r\n' \
                   '</user>\r\n' \
                   '</users>\r\n' \
                   '</user>\r\n' \
                   '</user_list>'

test_xml_result = [{'first_name': 'Max', 'last_name': 'Steam',
                    'avatar_url': 'https://pbs.twimg.com/media/BcINeMVCIAABeWd.jpg'},
                   {'first_name': 'Anton', 'last_name': 'Mechailov',
                    'avatar_url': 'https://mir-s3-cdn-cf.behance.net/project_modules/2800_opt_1/35af6a41332353.57a1ce913e889.jpg'},
                   {'first_name': 'Valerii', 'last_name': 'Jmishenko',
                    'avatar_url': 'https://static.boredpanda.com/blog/wp-content/uploads/2017/04/Virrappan2-58f79980ae6fb__880.jpg'}]

test_united_result = [{'username': 'M.Steam', 'password': 'ASDf43f#$dsD', 'date_joined': '1638700932',
                       'first_name': 'Max', 'last_name': 'Steam',
                       'avatar_url': 'https://pbs.twimg.com/media/BcINeMVCIAABeWd.jpg'},
                      {'username': 'V.Markus', 'password': 'DSA4FSFF54w%$#df', 'date_joined': '1464014817',
                       'first_name': 'Anton', 'last_name': 'Mechailov',
                       'avatar_url': 'https://mir-s3-cdn-cf.behance.net/project_modules/2800_opt_1/35af6a41332353.57a1ce913e889.jpg'},
                      {'username': 'M.Stone', 'password': 'Lkds(*dsdadf', 'date_joined': '1466078973',
                       'first_name': 'Valerii', 'last_name': 'Jmishenko',
                       'avatar_url': 'https://static.boredpanda.com/blog/wp-content/uploads/2017/04/Virrappan2-58f79980ae6fb__880.jpg'}]

test_bracketed_text = (('gper [[iwnIEWOFN]WIO]', 'gper'),
                       ('U(EIFnf)wu', 'Uwu'),
                       ('a([braCAD]Ab)ra', 'ara'))


def test_check_file_number_extensions_success():
    file_1.name, file_2.name = 'file_1.csV', 'file_2.Xml'
    result = U.check_file_number_and_extensions((file_1, file_2), request)
    assert result == {'csv': file_1, 'xml': file_2}


def test_check_file_number_fail():
    file_1.name, file_2.name, file_3.name = 'file_1.csv', 'file_2.xml', 'file_2.xml'
    result = U.check_file_number_and_extensions((file_1,), request)
    assert result is None
    result = U.check_file_number_and_extensions((file_1, file_2, file_3), request)
    assert result is None


def test_check_file_extensions_fail():
    file_1.name, file_2.name = 'file_1.csv', 'file_2.xls'
    result = U.check_file_number_and_extensions((file_1, file_2), request)
    assert result is None


def test_clean_bracketed_text_success():
    for pair in test_bracketed_text:
        assert U.clean_text_in_brackets(pair[0]) == pair[1]


def test_clean_bracketed_text_fail():
    for pair in test_bracketed_text:
        assert U.clean_text_in_brackets(pair[1]) != pair[0]


def test_csv_file_to_dict_success():
    result = U.csv_file_rows_to_dict(test_csv_content)
    assert result == test_csv_result


def test_damaged_csv_file_to_dict_fail():
    result = U.csv_file_rows_to_dict(test_csv_content[1:])
    assert result == []


def test_xml_file_to_dict_success():
    result = U.xml_file_rows_to_dict(StringIO(test_xml_content))
    assert result == test_xml_result


def test_damaged_xml_file_to_dict_fail():
    try:
        U.xml_file_rows_to_dict(StringIO(test_xml_content[20:]))
        assert False
    except ParseError:
        assert True


def test_unite_files_data_to_dict_success():
    dict_1 = copy(test_csv_result)
    for result in U.unite_files_data(dict_1, test_xml_result):
        assert result in test_united_result


def test_unite_files_data_to_dict_fail():
    dict_1 = copy(test_csv_result)
    result = len(U.unite_files_data(dict_1, [test_xml_result[0]]))
    assert result != len(test_united_result)
