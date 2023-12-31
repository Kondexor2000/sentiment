from django.contrib import admin
from .models import Slowo, Sentyment

# Register your models here.

class SłowoAdmin(admin.ModelAdmin):
    list_display = ['slowo', 'jest_pozytywne']
    list_filter = ['jest_pozytywne']

admin.site.register(Slowo, SłowoAdmin)
admin.site.register(Sentyment)