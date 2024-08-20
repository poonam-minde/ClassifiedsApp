from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import JobAdForm, SaleAdForm, RentalAdForm, ServiceAdForm, EventAdForm, ClassAdForm, MessageForm
from .models import JobAd, RentalAd, SaleAd, ServiceAd, EventAd, ClassAd, Message
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic import UpdateView, DeleteView, ListView
from django.http import Http404
from django.shortcuts import redirect
from django.contrib.contenttypes.models import ContentType

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
        return model.objects.filter(owner=self.request.user)

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ad = self.get_object()
        adtype = self.kwargs['adtype']

        if ad.owner != self.request.user:
            context['comments'] = Message.objects.filter(
                content_type__model=adtype+'ad',
                object_id=ad.id,
                user=self.request.user
            )
        else:
            context['comments'] = Message.objects.filter(
                content_type__model=adtype+'ad',
                object_id=ad.id
            ).exclude(user=self.request.user)

        context['adtype'] = adtype
        context['form'] = MessageForm()

        return context
    
    def post(self, request, *args, **kwargs):
        ad = self.get_object()
        adtype = self.kwargs['adtype']
        pk = self.kwargs['pk']
        form = MessageForm(request.POST)
        
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.ad = ad
            new_comment.user = request.user
            
            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    parent_comment = Message.objects.get(id=parent_id)
                    new_comment.parent = parent_comment
                except Message.DoesNotExist:
                    pass
            
            new_comment.content_type = ContentType.objects.get_for_model(ad)
            new_comment.object_id = ad.id
            new_comment.save()
            print(new_comment)
            return redirect('ad:ad_detail', adtype=adtype, pk=pk)
        
        return self.get(request, *args, **kwargs)
      
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
    
class BaseListView(ListView):
    template_name="ad/adtype_list.html"
    context_object_name = 'ads'

class JobListView(BaseListView):
    model = JobAd

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_type'] = 'job'
        return context

class SaleListView(BaseListView):
    model = SaleAd
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_type'] = 'sale'
        return context

class RentalListView(BaseListView):
    model = RentalAd

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_type'] = 'rental'
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
    template_name = 'ad/all_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['jobs'] = JobAd.objects.all()[:4]
        context['rentals'] = RentalAd.objects.all()[:4]
        context['sales'] = SaleAd.objects.all()[:4]
        context['services'] = ServiceAd.objects.all()[:4]
        context['events'] = EventAd.objects.all()[:4]
        context['classes'] = ClassAd.objects.all()[:4]

        return context

class EditCommentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'comment/edit_comment.html'
    
    def get_success_url(self):
        ad = self.object.ad
        adtype = self.kwargs['adtype']
        return reverse_lazy('ad:ad_detail', kwargs={'adtype': adtype, 'pk': ad.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message  
    template_name = 'comment/delete_comment.html'
    
    def get_success_url(self):
        ad = self.object.ad
        adtype = self.kwargs['adtype']
        return reverse_lazy('ad:ad_detail', kwargs={'adtype': adtype, 'pk': ad.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['adtype'] = adtype = self.kwargs['adtype']
        context['id'] = self.object.ad.pk
        return context