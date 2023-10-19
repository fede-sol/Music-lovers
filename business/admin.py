from django.contrib import admin
from .models import Business, BusinessComment, BusinessPhoto, Event, EventComment, EventPhoto

admin.site.register(Business)
admin.site.register(BusinessComment)
admin.site.register(BusinessPhoto)
admin.site.register(Event)
admin.site.register(EventComment)
admin.site.register(EventPhoto)