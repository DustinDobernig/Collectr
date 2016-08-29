from django.contrib import admin
from django.contrib.auth.models import User
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# Register your models here.
from .models import Campaign


class CampaignAdmin(ImportExportModelAdmin):
    
    
    superuser_fields = [ 'user',]
    normaluser_fields = [ 'redirect_uri', 'redirect_choice', 'title', 'content', 'sites']
    search_fields = ['user__username', 'slug']
    list_display = ["slug", "position", 'title', "user", "uid", "redirect_uri", 'redirect_choice']
    list_editable = ['redirect_uri', 'redirect_choice']                 
    class Meta:
        model = Campaign
        
#Show appropriate fields to superuser and users
    
    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.fields = self.superuser_fields + self.normaluser_fields
        else:
            self.fields = self.normaluser_fields

        return super(CampaignAdmin, self).get_form(request, obj, **kwargs)
    
#User can only edit their own campaigns

    def has_change_permission(self, request, obj=None):
        has_class_permission = super(CampaignAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.user.id:
            return False
        return True
    
#Only show campaigns to their own user

    def get_queryset(self, request):
        qs = super(CampaignAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
        
        
#Non super user campaign save 
    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            obj.save()
        else:
            if not change:
                obj.user = request.user
            obj.save()

class CampaignResource(resources.ModelResource):

    class Meta:
        model = Campaign
        fields = ("slug", "position", 'title', "user", "uid", "redirect_uri", 'redirect_choice')
  
resource_class = CampaignResource

# class CampaignResourceAdmin(ImportExportModelAdmin):
#     resource_class = CampaignResource
#     pass
    
admin.site.register(Campaign, CampaignAdmin)

