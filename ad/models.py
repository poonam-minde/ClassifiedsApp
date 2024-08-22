from django.db import models
from django.contrib.auth.models import User
import datetime
from taggit.managers import TaggableManager
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

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
    fees = models.PositiveIntegerField()

class Message(models.Model):
    message=models.TextField(default='')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages', default=1)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    ad = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"Message by {self.user} on {self.created_at}"
     
class AdImage(models.Model):
    job_ad = models.ForeignKey(JobAd, related_name='images', on_delete=models.CASCADE, null=True, blank=True)
    rental_ad = models.ForeignKey(RentalAd, related_name='images', on_delete=models.CASCADE, null=True, blank=True)
    sale_ad = models.ForeignKey(SaleAd, related_name='images', on_delete=models.CASCADE, null=True, blank=True)
    service_ad = models.ForeignKey(ServiceAd, related_name='images', on_delete=models.CASCADE, null=True, blank=True)
    event_ad = models.ForeignKey(EventAd, related_name='images', on_delete=models.CASCADE, null=True, blank=True)
    class_ad = models.ForeignKey(ClassAd, related_name='images', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='images/')
    
    def __str__(self):
        return f"Image for {self.job_ad or self.rental_ad}"    