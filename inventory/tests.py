import csv
import os

from django.test import Client, TestCase, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from inventory.models import Bookings, Members, Inventory
from inventory.serializers import BookingsSerializer


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


BOOKING_URL = reverse('book')

class BookingApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@mail.com',
            'testpass'
        )

        self.member_0 = Members.objects.create(
            name='Foo',
            surname='TDD',
            booking_count=1,
            date_joined='2021-01-12T16:11:58.644787Z'
        )

        self.member_1 = Members.objects.create(
            name='Bob',
            surname='py',
            booking_count=0,
            date_joined='2021-01-11T14:12:28.644787Z'
        )

        self.inventory_0 = Inventory.objects.create(
            title='Japan',
            description='Toyko',
            remaining_count=3,
            expiration_date='2021-01-11T14:12:28.644787Z'
        )

        self.inventory_1 = Inventory.objects.create(
            title='Mzansi',
            description='Fo Sho',
            remaining_count=2,
            expiration_date='2021-01-12T16:11:58.644787Z'
        )

        self.inventory_2 = Inventory.objects.create(
            title='RSA',
            description='CPT',
            remaining_count=0,
            expiration_date='2021-02-12T16:11:58.644787Z'
        )

        self.booking_3 = Bookings.objects.create(
            booking_id='d7b8b05d1e38',
            member=self.member_1,
            inventory=self.inventory_2,
            creation_date='2021-01-11T14:12:28.644787Z'
        )

        self.client.force_authenticate(self.user)


    def test_retrieve_booking_list(self):

        Bookings.objects.create(
            booking_id='dab9bc908ff9',
            member=self.member_0,
            inventory=self.inventory_0,
            creation_date='2021-01-12T16:11:58.644787Z'
        )

        Bookings.objects.create(
            booking_id='1013b5cbc7e5',
            member=self.member_1,
            inventory=self.inventory_1,
            creation_date='2021-01-11T14:12:28.644787Z'
        )

        res = self.client.get(BOOKING_URL)

        bookings = Bookings.objects.all()
        serializer = BookingsSerializer(bookings, many=True)

        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Bookings.objects.all().count(), 3)


    def test_get_valid_single_booking(self):

        BOOKING_DETAILS_URL = reverse(
            'cancel', args=[self.booking_3.booking_id])

        res = self.client.get(BOOKING_DETAILS_URL)
        booking = Bookings.objects.get(booking_id=self.booking_3.booking_id)
        serializer = BookingsSerializer(booking)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        member = Members.objects.get(pk=self.member_1.pk)
        self.assertEqual(len(member.booking_count), 1)

        inventory = Inventory.objects.get(pk=self.inventory_2.pk)
        self.assertEqual(len(inventory.remaining_count), 1)


    def test_get_invalid_single_booking(self):

        BOOKING_DETAILS_URL = reverse(
            'cancel', args=['2w23dedfws'])
        res = self.client.get(BOOKING_DETAILS_URL)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


    def test_valid_delete_booking(self):
        BOOKING_DETAILS_URL = reverse(
            'cancel', args=[self.booking_3.booking_id])
        res = self.client.delete(BOOKING_DETAILS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_invalid_delete_booking(self):
        BOOKING_DETAILS_URL = reverse(
            'cancel', args=['2w23dedfws'])
        res = self.client.delete(BOOKING_DETAILS_URL)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
