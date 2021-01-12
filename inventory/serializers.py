from rest_framework import serializers
from inventory.models import Bookings, Members


class BookingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bookings
        fields = (
            'id',
            'booking_id',
            'member',
            'inventory',
            'creation_date'
        )

    read_only_fields = ['id', 'booking_id']
