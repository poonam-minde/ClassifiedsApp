from .forms import JobAdForm, SaleAdForm, RentalAdForm, ServiceAdForm, EventAdForm, ClassAdForm

def create_post_form(request,adtype):
    if adtype=='job':
        return JobAdForm(request.POST, request.FILES)
    elif adtype=='rental':
        return RentalAdForm(request.POST, request.FILES)
    elif adtype=='sale':
        return SaleAdForm(request.POST, request.FILES)
    elif adtype=='service':
        return ServiceAdForm(request.POST, request.FILES)
    elif adtype=='event':
        return EventAdForm(request.POST, request.FILES)
    elif adtype=='class':
        return ClassAdForm(request.POST, request.FILES)
    
def create_get_from(adtype):
    if adtype=='job':
        return JobAdForm()
    elif adtype=='rental':
        return RentalAdForm()
    elif adtype=='sale':
        return SaleAdForm()
    elif adtype=='service':
        return ServiceAdForm()
    elif adtype=='event':
        return EventAdForm()
    elif adtype=='class':
        return ClassAdForm()