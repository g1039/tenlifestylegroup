from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from inventory.forms import InventoryDataForm, MembersDataForm
from inventory.models import Bookings, Inventory, Members
from inventory.serializers import BookingsSerializer


def home_view(request):
    return render(request, 'root/index.html')


def members_data_upload_view(request):
    if request.method == 'POST':
        form = MembersDataForm(request.POST, request.FILES)
        if form.is_valid():
            form.process_members_data()
            return HttpResponseRedirect('/')
    else:
        form = MembersDataForm()
    return render(request, 'upload/upload_members.html', {'form': form})


def inventory_data_upload_view(request):
    if request.method == 'POST':
        form = InventoryDataForm(request.POST, request.FILES)
        if form.is_valid():
            form.process_inventory_data()
            return HttpResponseRedirect('/')
    else:
        form = InventoryDataForm()
    return render(request, 'upload/upload_inventory.html', {'form': form})


class BookingsViewSetList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = Bookings.objects.all()
        serializer = BookingsSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None, * args, **kwargs):
        serializer = BookingsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                get_member = Members.objects.get(id=request.data['member'])
            except Members.DoesNotExist:
                raise Http404
            
            try:
                get_inventory = Inventory.objects.get(
                    id=request.data['inventory'])
            except Inventory.DoesNotExist:
                raise Http404
            
            member_booking_count = int(get_member.booking_count)
            inventory_remaining_count = int(get_inventory.remaining_count)

            member_count = 0
            inventory_count = 0

            if member_booking_count < 2 and inventory_remaining_count > 0:
                member_count += 1 + member_booking_count
                get_member.booking_count = member_count
                get_member.save()

                inventory_count -= 1 - inventory_remaining_count
                get_inventory.remaining_count = inventory_count
                get_inventory.save()

                booking = serializer.save()
                serializer = BookingsSerializer(booking)

                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {"MAX BOOKINGS": "2"},
                    status=status.HTTP_200_OK,
                    content_type='text/html'
                )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class BookingsDetailViewSetList(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Bookings.objects.all()
    serializer_class = BookingsSerializer
    lookup_field = 'booking_id'

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        try:
            get_booking_id = Bookings.objects.get(
                booking_id=instance.booking_id)
        except Bookings.DoesNotExist:
            raise Http404

        get_member = Members.objects.get(id=get_booking_id.member.id)
        get_inventory = Inventory.objects.get(id=get_booking_id.inventory.id)

        member_count = 0
        member_count -= 1 - int(get_member.booking_count)
        get_member.booking_count = member_count
        get_member.save()

        inventory_count = 0
        inventory_count += 1 + int(get_inventory.remaining_count)
        get_inventory.remaining_count = inventory_count
        get_inventory.save()

        get_booking_id.delete()

        return Response(
            {"Deleted": "True"},
            status=status.HTTP_200_OK,
            content_type='text/html'
        )
        super(BookingsDetailViewSetList, self).destroy(
            request, *args, **kwargs)
