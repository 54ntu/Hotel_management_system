from django.db.models import Q
from Hotel_Mgmt.models import RoomBooking

def is_room_available(room_id,check_in_date,check_out_date):
    overlap_booking = RoomBooking.objects.filter(room_number_id = room_id).filter(Q(check_in_date__lt = check_out_date) & Q(check_out_date__gt = check_in_date))
    return not overlap_booking.exists() # if no overlap false so it negates the value and return true


