from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import get_script_prefix
from django.db import models
from django.db.models import Max
from django.utils.encoding import iri_to_uri, python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from hashids import Hashids
from tinymce.models import HTMLField

# Hashids attributes
hashids = Hashids(min_length=6)

### Create App ###
class Campaign(models.Model):
    user = models.ForeignKey(User)
    uid = models.CharField("User ID#", max_length=300, blank=True)
    title = models.CharField(_('title'), max_length=200, blank=True)
    content = HTMLField(_('content'), blank=True)
    position = models.PositiveIntegerField("Campaign ID #")
    slug = models.CharField(max_length=300)
    redirect_uri = models.CharField(max_length=300, blank=True) ### to add more schemes like "mailto:" add scheme to allow_schemes in /lib/python2.7/site-packages/django/http/response.py
    redirect_choice = models.BooleanField("redirect", default=False)
    sites = models.ManyToManyField(Site)
    template_name = models.CharField(_('template name'), max_length=70, blank=True,
        help_text=_(
            "Example: 'flatpages/contact_page.html'. If this isn't provided, "
            "the system will use 'flatpages/default.html'."
        ),
    )
    registration_required = models.BooleanField(_('registration required'),
        help_text=_("If this is checked, only logged-in users will be able to view the page."),
        default=False)

### Get user id ###
    def get_uid(self):
        result = self.user.id
        return result
    
### Get users individual campaign position ###
    def get_position(self):
        if not self.position:
            current_user_campaigns = self.user.campaign_set
            if current_user_campaigns.count() == 0:
                self.position = 1               
            else:
                self.position = current_user_campaigns.all().aggregate(Max('position'))["position__max"] + 1
        return self.position
        
### Hash user id/campagn position to generate slug ###
    def get_slug(self):
        result = hashids.encode(self.user.id, self.position)
        return result
    
### Save slug/uid/get_position to table  ###
    def save(self, *args, **kwargs):
        #top = Campaign.objects.order_by('-position')[:1]
        #self.position = top.position + 1
        self.position = self.get_position()
        self.slug = self.get_slug()
        self.uid = self.get_uid()
        super(Campaign, self).save(*args, **kwargs)
       
        
### Make unique the user and slug ###
    class Meta:
        unique_together = (("user", "slug"), )
    
    def __str__(self):
        return "%s -- %s" % (self.slug, self.title)
        
### Return absolute URL ###
    def get_absolute_url(self):
        # Handle script prefix manually because we bypass reverse()
        return '/%s' %(self.slug)
        

