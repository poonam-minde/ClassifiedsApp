from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .utility import create_post_form, create_get_from

def ad_list(request):
    return HttpResponse("ad list")

@login_required
def create_ad(request,adtype):
    if request.method == 'POST':
        form = create_post_form(request,adtype)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.owner = request.user
            ad.save()
            messages.success(request, 'Ad created successfully!')
            return redirect('ad:ad_list')
    else:
        form = create_get_from(adtype)
    return render(request, 'ad/ad_form.html', {'form': form})

