import datetime
import uuid

from django.utils import formats
from django.db import models


class Members(models.Model):

    name = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    surname = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    booking_count = models.CharField(
        max_length=5,
        blank=True,
        null=True
    )

    date_joined = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = 'Members'


class Inventory(models.Model):

    title = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    remaining_count = models.CharField(
        max_length=5,
        blank=True,
        null=True
    )

    expiration_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = 'Inventory'


class Bookings(models.Model):

    booking_id = models.CharField(
        max_length=50,
        blank=True,
        unique=True
    )
    member = models.ForeignKey(
        Members,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    inventory = models.ForeignKey(
        Inventory,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if len(self.booking_id.strip(" ")) == 0:
            self.booking_id = generate_booking_id()
        super(Bookings, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Bookings'


def generate_booking_id():
    return str(uuid.uuid4()).split("-")[-1]
