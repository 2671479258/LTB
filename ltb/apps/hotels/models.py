from datetime import datetime

from django.db import models
from users.models import User,Roomtype
# Create your models here.

def generate_order_number():
    now = datetime.now()
    date_str = now.strftime('%Y%m%d')
    last_order = Hotel_Order.objects.filter(order_number__startswith=date_str).order_by('order_number').last()
    if not last_order:
        new_order_number = f"{date_str}0001"
    else:
        last_order_number = int(last_order.order_number[-4:])
        new_order_number = f"{date_str}{last_order_number + 1:04d}"
    return new_order_number



class Hotel_Order(models.Model):
    order_number = models.CharField(max_length=12, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    selectedRoom = models.ForeignKey(Roomtype, on_delete=models.CASCADE)
    current_year = models.IntegerField()
    checkInDate = models.CharField(max_length=20)
    checkOutDate = models.CharField(max_length=20)
    roomCount = models.IntegerField()
    guestName = models.CharField(max_length=255)
    email = models.CharField(max_length=40)
    phoneNumber = models.CharField(max_length=20)
    estimatedArrivalTime = models.CharField(max_length=20)



    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number

    class Meta:
        app_label = 'hotels'
        db_table='hotels_order'
        verbose_name='酒店预约'
        verbose_name_plural=verbose_name