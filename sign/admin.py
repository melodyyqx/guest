from django.contrib import admin
from sign.models import Event,Guest

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'starttime','id']
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ['name']

class GuestAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone','email','sign','createtime']
    list_display_links = ['name','phone']
    search_fields = ['phone']
    list_filter = ['name']


admin.site.register(Event,EventAdmin)
admin.site.register(Guest,GuestAdmin)