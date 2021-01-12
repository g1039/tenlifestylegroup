import csv
import io

from django import forms

from inventory.models import Members, Inventory


class MembersDataForm(forms.Form):
    data_file = forms.FileField()

    def clean_data_file(self):
        f = self.cleaned_data['data_file']

        if f:
            ext = f.name.split('.')[-1]
            if ext != 'csv':
                raise forms.ValidationError('File Type not Supported')
        return f

    def process_members_data(self):
        f = io.TextIOWrapper(self.cleaned_data['data_file'].file)
        reader = csv.DictReader(f)

        field_names = [
            'name',
            'surname',
            'booking_count',
            'date_joined'
        ]

        for column in reader:
            if len(set(field_names).intersection(set(column))) == 0:
                return("CSV Error: Invalid headers: %s" % str(column))
            else:
                Members.objects.create(
                    name=column['name'],
                    surname=column['surname'],
                    booking_count=column['booking_count'],
                    date_joined=column['date_joined']
                )


class InventoryDataForm(forms.Form):
    data_file = forms.FileField()

    def clean_data_file(self):
        f = self.cleaned_data['data_file']

        if f:
            ext = f.name.split('.')[-1]
            if ext != 'csv':
                raise forms.ValidationError('File Type not Supported')
        return f

    def process_inventory_data(self):
        f = io.TextIOWrapper(self.cleaned_data['data_file'].file)
        reader = csv.DictReader(f)

        field_names = [
            'title',
            'description',
            'remaining_count',
            'expiration_date'
        ]

        for column in reader:
            if len(set(field_names).intersection(set(column))) == 0:
                return("CSV Error: Invalid headers: %s" % str(column))
            else:
                Inventory.objects.create(
                    title=column['title'],
                    description=column['description'],
                    remaining_count=column['remaining_count'],
                    expiration_date=column['expiration_date']
                )
