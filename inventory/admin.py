from django.contrib import admin

from inventory.models import Bookings, Inventory, Members


@admin.register(Members)
class MembersAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "surname",
        "booking_count",
        "date_joined"
    )

    search_fields = [
        "id",
        "name",
        "surname",
        "booking_count",
        "date_joined"
    ]


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "description",
        "remaining_count",
        "expiration_date"
    )

    search_fields = [
        "id",
        "title",
        "description",
        "remaining_count",
        "expiration_date"
    ]


@admin.register(Bookings)
class BookingsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "booking_id",
        "member",
        "inventory",
        "creation_date"
    )

    search_fields = [
        "id",
        "booking_id",
        "member",
        "inventory",
        "creation_date"
    ]
