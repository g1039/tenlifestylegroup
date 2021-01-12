import csv
import os

from django.test import Client, TestCase, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse

from inventory.models import Members, Inventory


class MembersCsvFileUploadTests(TestCase):

    def setUp(self):
        self.Client = Client()
        self.user = get_user_model().objects.create_user(
            username='Foo',
            password='password123',
            first_name='Foo full name'
        )

    def generate_csv_file(self):
        try:
            my_csv_file = open('test.csv', 'w')
            wr = csv.writer(my_csv_file)
            wr.writerow((
                'name',
                'surname',
                'booking_count',
                'date_joined'
            ))
            wr.writerow((
                'Trevor',
                'October',
                '1',
                '2020-11-12T12:10:12'
            ))
            wr.writerow((
                'Bob',
                'Foo',
                '0',
                '2020-12-12T12:00:12'
            ))
        finally:
            my_csv_file.close()
        return my_csv_file

    def generate_invalid_csv_file(self):
        try:
            invalid_csv_file = open('invalid.csv', 'w')
            wr = csv.writer(invalid_csv_file)
            wr.writerow((
                'username',
                'email',
                'firstname',
                'lastname'
            ))
            wr.writerow((
                'root',
                'root@mail.com',
                'foo',
                'bob',
            ))
        finally:
            invalid_csv_file.close()
            return invalid_csv_file

    def generate_text_file(self):
        try:
            my_txt_file = open('test.txt', 'w')
            my_txt_file.write("Hello World!!!")
        finally:
            my_txt_file.close()
        return my_txt_file

    def test_csv_upload(self):
        response = self.client.login(
            username=self.user.username,
            password='password123'
        )
        self.assertTrue(response)

        my_csv_file = self.generate_csv_file()
        csv_file_path = my_csv_file.name
        c = open(csv_file_path, "rb")

        invalid_csv_file = self.generate_invalid_csv_file()
        invalid_csv_file_path = invalid_csv_file.name
        i = open(invalid_csv_file_path, "rb")

        my_txt_file = self.generate_text_file()
        txt_file_path = my_txt_file.name
        t = open(txt_file_path, "rb")

        url = reverse('members')

        # post wrong data type
        post_wrong_data = {'data_file': t}
        response = self.client.post(url, post_wrong_data, format='multipart')
        self.assertContains(response, 'File Type not Supported')

        # post invalid data type
        post_invalid_data = {'data_file': i}
        response = self.client.post(url, post_invalid_data, format='multipart')
        self.assertRaises(TypeError)

        # Post correct data type
        post_correct_data = {'data_file': c}
        self.client.post(url, post_correct_data, format='multipart')
        self.assertEqual(Members.objects.all().count(), 2)

        os.remove(my_csv_file.name)
        os.remove(invalid_csv_file.name)
        os.remove(my_txt_file.name)


class InventoryCsvFileUploadTests(TestCase):

    def setUp(self):
        self.Client = Client()
        self.user = get_user_model().objects.create_user(
            username='Foo',
            password='password123',
            first_name='Foo full name'
        )

    def generate_csv_file(self):
        try:
            my_csv_file = open('test.csv', 'w')
            wr = csv.writer(my_csv_file)
            wr.writerow((
                'title',
                'description',
                'remaining_count',
                'expiration_date'
            ))
            wr.writerow((
                'Japan',
                'Quisque ut eleifend turpis',
                '1',
                '2020-11-20T12:10:12'
            ))
            wr.writerow((
                'Kenya',
                'Kila moja kama Japani mbaya',
                '5',
                '2020-12-31T12:19:14'
            ))
        finally:
            my_csv_file.close()
        return my_csv_file

    def generate_invalid_csv_file(self):
        try:
            invalid_csv_file = open('invalid.csv', 'w')
            wr = csv.writer(invalid_csv_file)
            wr.writerow((
                'titel',
                'beskrywing',
                'count',
                'date'
            ))
            wr.writerow((
                'root',
                'root@mail.com',
                'foo',
                'bob',
            ))
        finally:
            invalid_csv_file.close()
            return invalid_csv_file

    def generate_text_file(self):
        try:
            my_txt_file = open('test.txt', 'w')
            my_txt_file.write("Hello World!!!")
            my_txt_file.writelines(["Yay\n TDD rocks!!!"])
        finally:
            my_txt_file.close()
        return my_txt_file

    def test_csv_upload(self):
        response = self.client.login(
            username=self.user.username,
            password='password123'
        )
        self.assertTrue(response)

        my_csv_file = self.generate_csv_file()
        csv_file_path = my_csv_file.name
        c = open(csv_file_path, "rb")

        invalid_csv_file = self.generate_invalid_csv_file()
        invalid_csv_file_path = invalid_csv_file.name
        i = open(invalid_csv_file_path, "rb")

        my_txt_file = self.generate_text_file()
        txt_file_path = my_txt_file.name
        t = open(txt_file_path, "rb")

        url = reverse('inventory')

        # post wrong data type
        post_wrong_data = {'data_file': t}
        response = self.client.post(url, post_wrong_data, format='multipart')
        self.assertContains(response, 'File Type not Supported')

        # post invalid data type
        post_invalid_data = {'data_file': i}
        response = self.client.post(url, post_invalid_data, format='multipart')
        self.assertRaises(TypeError)

        # Post correct data type
        post_correct_data = {'data_file': c}
        self.client.post(url, post_correct_data, format='multipart')
        self.assertEqual(Inventory.objects.all().count(), 2)

        os.remove(my_csv_file.name)
        os.remove(invalid_csv_file.name)
        os.remove(my_txt_file.name)
