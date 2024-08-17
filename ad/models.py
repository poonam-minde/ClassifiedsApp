from django.db import models
from django.contrib.auth.models import User
import datetime
from taggit.managers import TaggableManager
from django.utils import timezone

class AdInfo(models.Model):
    title = models.CharField(
        max_length=255,
    )
    description = models.TextField()
    tags = TaggableManager()
    
    def __str__(self):
        return self.title

    class Meta:
        abstract = True

class ContactInfo(models.Model):
    email = models.EmailField()
    show_email = models.BooleanField(default=True)
    phone = models.CharField(
        max_length=15,
        blank=True,
    )
    show_phone = models.BooleanField(default=False)

    class Meta:
        abstract = True

class AddressInfo(models.Model):
    location = models.CharField(
        max_length=255,
    )
    postal_code = models.CharField(
        max_length=20,
    )
    class Meta:
        abstract = True

class JobAd(AdInfo, ContactInfo, AddressInfo):
    CATEGORY_CHOICES = [
        ('FT', 'Full Time'),
        ('PT', 'Part Time'),
        ('IN', 'Internship'),
    ]
    category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default='FT',
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobads')
    image = models.ImageField(
        upload_to='images/jobs',
        blank=True,
        null=True,
    )
    salary = models.PositiveIntegerField()

class RentalAd(AdInfo, ContactInfo):
    CATEGORY_CHOICES = [
        ('FT', 'Flat'),
        ('PT', 'Furniture'),
        ('IN', 'Electronics'),
        ('VH', 'Vehicals'),
    ]
    category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default='FT',
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentalads')
    image = models.ImageField(
        upload_to='images/rentals',
        blank=True,
        null=True,
    )
    charge = models.PositiveIntegerField()
    PERIOD_CHOICES = [
        ('M', 'Month'),
        ('D', 'Day'),
        ('Y', 'Year'),
    ]
    period = models.CharField(
        max_length=1,
        choices=PERIOD_CHOICES,
        default='D',
    )

class SaleAd(AdInfo):
    CATEGORY_CHOICES = [
        ('EL', 'Electronics'),
        ('FU', 'Furniture'),
        ('BE', 'Beauty'),
        ('JW', 'Jwellary'),
        ('GR', 'Grocery'),
        ('BK', 'Books'),
        ('FA', 'Fashion'),
    ]
    category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default='FA',
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saleads')
    image = models.ImageField(
        upload_to='images/sales',
        blank=True,
        null=True,
    )
    price = models.PositiveIntegerField()
    
class ServiceAd(AdInfo, ContactInfo):
    CATEGORY_CHOICES = [
        ('IN', 'Insurance'),
        ('CT', 'Contruction'),
        ('LE', 'Legal'),
        ('WM', 'Waste Management'),
        ('GR', 'Gadget Repairing'),
    ]
    category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default='IN',
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='serviceads')
    image = models.ImageField(
        upload_to='images/services',
        blank=True,
        null=True,
    )
    price = models.PositiveIntegerField()
    
class EventAd(AdInfo, ContactInfo, AddressInfo):
    CATEGORY_CHOICES = [
        ('FE', 'Festival'),
        ('SE', 'Seminar'),
        ('SP', 'Sports Event'),
        ('MO', 'Modeling'),
    ]
    category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default='FE',
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eventads')
    image = models.ImageField(
        upload_to='images/events',
        blank=True,
        null=True,
    )
    price = models.PositiveIntegerField()
    start_date = models.DateTimeField(default=datetime.datetime.now)
    end_date = models.DateTimeField(default=datetime.datetime.now)

class ClassAd(AdInfo, ContactInfo, AddressInfo):
    CATEGORY_CHOICES = [
        ('DA', 'Daily'),
        ('WE', 'Weekend'),
        ('WO', 'Workshop'),
        ('WO', 'Weekdays'),
    ]
    category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default='DA',
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classads')
    image = models.ImageField(
        upload_to='images/classes',
        blank=True,
        null=True,
    )
    fees = models.PositiveIntegerField()

class Message(models.Model):
    message=models.TextField(default='')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(default=timezone.now)
     
    class Meta:
        abstract = True

class JobMessage(Message):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_message_user', default=1)
    ad=models.ForeignKey(JobAd, on_delete=models.CASCADE, related_name='job_message')

class SaleMessage(Message):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='sale_message_user', default=1)
    ad=models.ForeignKey(SaleAd, on_delete=models.CASCADE, related_name='sale_message')

class RentalMessage(Message):
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name='rental_message_user', default=1)
    ad=models.ForeignKey(RentalAd, on_delete=models.CASCADE, related_name='rental_message')

class ServiceMessage(Message):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_message_user', default=1)
    ad=models.ForeignKey(ServiceAd, on_delete=models.CASCADE, related_name='service_message')

class EventMessage(Message):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_message_user', default=1)
    ad=models.ForeignKey(EventAd, on_delete=models.CASCADE, related_name='event_message')

class ClassMessage(Message):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='class_message_user', default=1)
    ad=models.ForeignKey(ClassAd, on_delete=models.CASCADE, related_name='class_message')
