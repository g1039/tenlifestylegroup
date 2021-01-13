from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import generics

from inventory import views
from inventory.models import Bookings
from inventory.serializers import BookingsSerializer


urlpatterns = [
    path("", views.home_view, name="home"),
    path(
        "members/upload",
        views.members_data_upload_view,
        name="members"
    ),
    path(
        "inventory/upload",
        views.inventory_data_upload_view,
        name="inventory"
    ),
    path(
        'book/',
        views.BookingsViewSetList.as_view(),
        name='book'),
    path(
        'book/cancel/<str:booking_id>/',
        views.BookingsDetailViewSetList.as_view(),
        name='cancel'
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
