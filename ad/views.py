from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import JobAdForm, SaleAdForm, RentalAdForm, ServiceAdForm, EventAdForm, ClassAdForm
from .models import JobAd, RentalAd, SaleAd, ServiceAd, EventAd, ClassAd

def ad_list(request):
    return HttpResponse("ad list")

class AdCreateView(LoginRequiredMixin, CreateView):
    template_name = 'ad/ad_form.html'
    success_url = reverse_lazy('ad:ad_list')
    model_mapping = {
        'job': JobAd,
        'sale': SaleAd,
        'rental': RentalAd,
        'for_sale': SaleAd,
        'service': ServiceAd,
        'event': EventAd,
        'class': ClassAd,
    }
    form_mapping = {
        'job': JobAdForm,
        'sale': SaleAdForm,
        'rental': RentalAdForm,
        'for_sale': SaleAdForm,
        'service': ServiceAdForm,
        'event': EventAdForm,
        'class': ClassAdForm,
    }

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Ad created successfully!')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['adtype'] = self.kwargs['adtype']
        return kwargs

    def get_model(self):
        adtype = self.kwargs['adtype']
        return self.model_mapping.get(adtype)

    def get_form_class(self):
        adtype = self.kwargs['adtype']
        return self.form_mapping.get(adtype)

    def get_queryset(self):
        return self.get_model().objects.all()