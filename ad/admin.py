from django.contrib import admin
from .models import JobAd, RentalAd, SaleAd, ServiceAd, EventAd, ClassAd, AdImage
from .models import Message

class JobAdAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'salary', 'location') 
    list_filter = ('title','location','category')                     
    search_fields = ('title', 'location', 'description')  
    fields = ('category','title','owner','description','tags','salary','location','postal_code','email','show_email', 
              'phone','show_phone')                               

admin.site.register(JobAd, JobAdAdmin)

class RentalAdAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'charge', 'period','email','phone')  
    list_filter = ('title','category')                     
    search_fields = ('title', 'category')
    fields = ('category','title','owner','description','tags','charge','period','email','show_email', 
              'phone','show_phone')                                 

admin.site.register(RentalAd, RentalAdAdmin)

class SaleAdAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price')  
    list_filter = ('title','category')                     
    search_fields = ('title', 'category','description')  
    fields = ('category','title','owner','description','tags','price')                               

admin.site.register(SaleAd, SaleAdAdmin)

class ServiceAdAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'email','phone')  
    list_filter = ('title','category')                     
    search_fields = ('title', 'category') 
    fields = ('category','title','owner','description','tags','price','email','show_email', 
              'phone','show_phone')                                

admin.site.register(ServiceAd, SaleAdAdmin)

class EventAdAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'location')  
    list_filter = ('title','location','category')                     
    search_fields = ('title', 'location') 
    fields = ('category','title','owner','description','tags','price','location','postal_code','email','show_email', 
              'phone','show_phone', 'start_date', 'end_date')                                

admin.site.register(EventAd, EventAdAdmin)

class ClassAdAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'fees', 'location','email','phone')  
    list_filter = ('title','location','category')                     
    search_fields = ('title', 'location')
    fields = ('category','title','owner','description','tags','fees','location','postal_code','email','show_email', 
              'phone','show_phone')                                 

admin.site.register(ClassAd, ClassAdAdmin)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_ad_object', 'get_ad_title','created_at', 'parent')
    search_fields = ('user__username', 'message', 'get_ad_title')
    list_filter = ('created_at', 'content_type')

    def get_ad_object(self, obj):
        return obj.content_type.model
    
    get_ad_object.short_description = 'Ad Object'

    def get_ad_title(self, obj):
        ad_instance = obj.ad
        if ad_instance:
            return getattr(ad_instance, 'title', '(No title)')
        return '(No ad)'
    get_ad_title.short_description = 'Ad Title'

class AdImageAdmin(admin.ModelAdmin):
    list_display = ( 'image', 'id')
    readonly_fields = ('id',)

admin.site.register(AdImage, AdImageAdmin)