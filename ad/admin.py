from django.contrib import admin
from .models import JobAd, RentalAd, SaleAd, ServiceAd, EventAd, ClassAd

class JobAdAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'salary', 'location') 
    list_filter = ('title','location','category')                     
    search_fields = ('title', 'location', 'description')  
    fields = ('category','title','owner','image','description','tags','salary','location','postal_code','email','show_email', 
              'phone','show_phone')                               

admin.site.register(JobAd, JobAdAdmin)

class RentalAdAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'charge', 'period','email','phone')  
    list_filter = ('title','category')                     
    search_fields = ('title', 'category')
    fields = ('category','title','owner','image','description','tags','charge','period','email','show_email', 
              'phone','show_phone')                                 

admin.site.register(RentalAd, RentalAdAdmin)

class SaleAdAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'image')  
    list_filter = ('title','category')                     
    search_fields = ('title', 'category','description')  
    fields = ('category','title','owner','description','image','tags','price')                               

admin.site.register(SaleAd, SaleAdAdmin)

class ServiceAdAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'email','phone')  
    list_filter = ('title','category')                     
    search_fields = ('title', 'category') 
    fields = ('category','title','owner','image','description','tags','price','email','show_email', 
              'phone','show_phone')                                

admin.site.register(ServiceAd, SaleAdAdmin)

class EventAdAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'location')  
    list_filter = ('title','location','category')                     
    search_fields = ('title', 'location') 
    fields = ('category','title','owner','image','description','tags','price','location','postal_code','email','show_email', 
              'phone','show_phone', 'start_date', 'end_date')                                

admin.site.register(EventAd, EventAdAdmin)

class ClassAdAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'fees', 'location','email','phone')  
    list_filter = ('title','location','category')                     
    search_fields = ('title', 'location')
    fields = ('category','title','owner','image','description','tags','fees','location','postal_code','email','show_email', 
              'phone','show_phone')                                 

admin.site.register(ClassAd, ClassAdAdmin)
