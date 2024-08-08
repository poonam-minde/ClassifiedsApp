from django import forms
from .models import JobAd, RentalAd, SaleAd, ServiceAd, EventAd, ClassAd

class JobAdForm(forms.ModelForm):
    class Meta:
        model = JobAd
        fields = ['category', 'title', 'image', 'tags', 'location', 'postal_code', 
                  'description', 'salary','email', 'show_email', 'phone', 'show_phone']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 40}), 
        }

class RentalAdForm(forms.ModelForm):
    class Meta:
        model = RentalAd
        fields = ['category', 'title', 'image', 'tags', 
                  'description', 'charge','period','email', 'show_email', 'phone', 'show_phone']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 40}), 
        }

class SaleAdForm(forms.ModelForm):
    class Meta:
        model = SaleAd
        fields = ['category', 'title', 'image', 'tags', 'description', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 40}), 
        }

class ServiceAdForm(forms.ModelForm):
    class Meta:
        model = ServiceAd
        fields = ['category', 'title', 'image', 'tags', 'description', 
                  'price','email', 'show_email', 'phone', 'show_phone']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 40}), 
        }

class EventAdForm(forms.ModelForm):
    class Meta:
        model = EventAd
        fields = ['category', 'title', 'image', 'tags', 'location', 'postal_code', 
                  'description', 'price','email', 'show_email', 'phone', 'show_phone',
                  'start_date','end_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 40}), 
        }

class ClassAdForm(forms.ModelForm):
    class Meta:
        model = ClassAd
        fields = ['category', 'title', 'image', 'tags', 'location', 'postal_code', 
                  'description', 'fees','email', 'show_email', 'phone', 'show_phone']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 40}), 
        }