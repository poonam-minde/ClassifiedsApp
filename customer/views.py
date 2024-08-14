from django.views.generic import ListView, TemplateView
from ad.models import JobAd, RentalAd, SaleAd, ServiceAd, EventAd, ClassAd

class BaseListView(ListView):
    template_name = 'customer/list.html'
    context_object_name = 'ads'

class JobListView(BaseListView):
    model = JobAd

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_type'] = 'job'
        return context

class RentalListView(BaseListView):
    model = RentalAd

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_type'] = 'rental'
        return context

class SaleListView(BaseListView):
    model = SaleAd

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_type'] = 'sale'
        return context

class ServiceListView(BaseListView):
    model = ServiceAd

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_type'] = 'service'
        return context

class EventListView(BaseListView):
    model = EventAd

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_type'] = 'event'
        return context

class ClassListView(BaseListView):
    model = ClassAd

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_type'] = 'class'
        return context
    
class AllAdListView(TemplateView):
    template_name = 'customer/all_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['jobs'] = JobAd.objects.all()[:4]
        context['rentals'] = RentalAd.objects.all()[:4]
        context['sales'] = SaleAd.objects.all()[:4]
        context['services'] = ServiceAd.objects.all()[:4]
        context['events'] = EventAd.objects.all()[:4]
        context['classes'] = ClassAd.objects.all()[:4]

        return context