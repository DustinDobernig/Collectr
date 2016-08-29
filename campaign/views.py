from django.views.generic import DeleteView											
from django.views.decorators.csrf import csrf_protect											
from django.utils.safestring import mark_safe											
from django.template import loader																					
from django.shortcuts import get_object_or_404, redirect, render																							
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect											
from django.core.urlresolvers import reverse_lazy											
from django.contrib.sites.shortcuts import get_current_site											
from django.conf import settings											
from .models import Campaign											
from .forms import CampaignForm											

# Template for Content and Title
DEFAULT_TEMPLATE = 'default.html'

# Create your views here.
def home(request):
    title ='Welcome'
     
    #user is authenticated 
    if request.user.is_authenticated():
        title = "Hello %s" %(request.user)
        form = CampaignForm(request.POST or None)
        message = " "
        queryset = Campaign.objects.filter(user=request.user)
        context = {
            "title": title,
            "form": form,
            "queryset": queryset
        }
        
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            context = {
                "message": "Campaign created",
                "title": title,
                "form": form,
                "queryset": queryset
            }
            return HttpResponseRedirect('/')
        
        
        return render(request, "base.html", context )
    
    #end user is authenticated 
    
    context = {
            "title": title,
        }
    return render(request, "base.html", context)

### render flatpage ###

def flatpage(request, slug):
    
    if not slug.startswith(''):
        slug = '' + slug
    site_id = get_current_site(request).id
    try:
        f = get_object_or_404(Campaign,
            slug=slug, sites=site_id)
    except Http404:
        if not slug.endswith('') and settings.APPEND_SLASH:
            slug += ''
            f = get_object_or_404(Campaign,
                slug=slug, sites=site_id)
            return HttpResponsePermanentRedirect('%s' % request.path)
        else:
            raise
    return render_flatpage(request, f)


@csrf_protect
def render_flatpage(request, f):
    """
    Internal interface to the flat page view.
    """
    # If registration is required for accessing this page, and the user isn't
    # logged in, redirect to the login page.
    if f.registration_required and not request.user.is_authenticated():
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.path)
    if f.template_name:
        template = loader.select_template((f.template_name, DEFAULT_TEMPLATE))
    else:
        template = loader.get_template(DEFAULT_TEMPLATE)

    # To avoid having to always use the "|safe" filter in flatpage templates,
    # mark the title and content as already safe (since they are raw HTML
    # content in the first place).
    f.title = mark_safe(f.title)
    f.content = mark_safe(f.content)

    response = HttpResponse(template.render({'flatpage': f}, request))
    return response

#Return appropriate campaign view when redirect boolean is selected

def campaign_views(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    if campaign.redirect_choice:
        return redirect(campaign.redirect_uri)
    else:
        return flatpage(request, slug=slug)
