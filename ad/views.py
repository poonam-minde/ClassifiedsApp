from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import JobAdForm, SaleAdForm, RentalAdForm, ServiceAdForm, EventAdForm, ClassAdForm
from .models import JobAd, RentalAd, SaleAd, ServiceAd, EventAd, ClassAd
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic import UpdateView, DeleteView
from django.http import Http404

class ModelMappingMixin:
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

    def get_model(self):
        adtype = self.kwargs['adtype']
        model = self.model_mapping.get(adtype)
        if not model:
            raise Http404(f"No model found for ad type: {adtype}")
        return model

    def get_form_class(self):
        adtype = self.kwargs['adtype']
        return self.form_mapping.get(adtype)

    def get_queryset(self):
        model = self.get_model()
        return model.objects.all()

class AdListView(LoginRequiredMixin, TemplateView):
    template_name = 'ad/ad_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['jobs'] = JobAd.objects.filter(owner=self.request.user)
        context['rentals'] = RentalAd.objects.filter(owner=self.request.user)
        context['sales'] = SaleAd.objects.filter(owner=self.request.user)
        context['services'] = ServiceAd.objects.filter(owner=self.request.user)
        context['events'] = EventAd.objects.filter(owner=self.request.user)
        context['classes'] = ClassAd.objects.filter(owner=self.request.user)

        return context

class AdCreateView(LoginRequiredMixin, ModelMappingMixin,CreateView):
    template_name = 'ad/ad_form.html'
    success_url = reverse_lazy('ad:ad_list')

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
    
class AdDetailView(LoginRequiredMixin, DetailView, ModelMappingMixin):
    template_name = 'ad/ad_detail.html'
    context_object_name = 'ad'

    def get_model(self):
        adtype = self.kwargs['adtype']
        model = self.model_mapping.get(adtype)
        if not model:
            raise Http404(f"No model found for ad type: {adtype}")
        return model
    
    def get_queryset(self):
        model = self.get_model()
        return model.objects.all()
    
class AdUpdateView(LoginRequiredMixin, ModelMappingMixin, UpdateView):
    template_name = 'ad/ad_form.html'
    context_object_name = 'ad'

    def get_success_url(self):
        adtype = self.kwargs['adtype']
        return reverse_lazy('ad:ad_detail', kwargs={'adtype': adtype, 'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context
    
class AdDeleteView(LoginRequiredMixin, ModelMappingMixin, DeleteView):
    template_name = 'ad/ad_delete.html'
    context_object_name = 'ad'
    
    def get_success_url(self):
        return reverse_lazy('ad:ad_list')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, "Ad deleted successfully!")
        return response