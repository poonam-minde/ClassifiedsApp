from django import forms
from .models import JobAd, RentalAd, SaleAd, ServiceAd, EventAd, ClassAd, Message

class AdForm(forms.ModelForm):
    class Meta:
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 40}), 
        }

    def __init__(self, *args, **kwargs):
        adtype = kwargs.pop('adtype', None)
        super().__init__(*args, **kwargs)

        if adtype:
            self.fields['title'].label = f'{adtype.capitalize()} Title'

class JobAdForm(AdForm):
    class Meta(AdForm.Meta):
        model = JobAd
        fields = ['category', 'title', 'image', 'tags', 'location', 'postal_code', 
                  'description', 'salary','email', 'show_email', 'phone', 'show_phone']
        

class RentalAdForm(AdForm):
    class Meta(AdForm.Meta):
        model = RentalAd
        fields = ['category', 'title', 'image', 'tags', 
                  'description', 'charge','period','email', 'show_email', 'phone', 'show_phone']

class SaleAdForm(AdForm):
    class Meta(AdForm.Meta):
        model = SaleAd
        fields = ['category', 'title', 'image', 'tags', 'description', 'price']

class ServiceAdForm(AdForm):
    class Meta(AdForm.Meta):
        model = ServiceAd
        fields = ['category', 'title', 'image', 'tags', 'description', 
                  'price','email', 'show_email', 'phone', 'show_phone']

class EventAdForm(AdForm):
    class Meta(AdForm.Meta):
        model = EventAd
        fields = ['category', 'title', 'image', 'tags', 'location', 'postal_code', 
                  'description', 'price','email', 'show_email', 'phone', 'show_phone',
                  'start_date','end_date']

class ClassAdForm(AdForm):
    class Meta(AdForm.Meta):
        model = ClassAd
        fields = ['category', 'title', 'image', 'tags', 'location', 'postal_code', 
                  'description', 'fees','email', 'show_email', 'phone', 'show_phone']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 1, 'cols': 40}), 
        }
    