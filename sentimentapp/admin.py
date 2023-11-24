from django.contrib import admin
from .models import Slowo

# Register your models here.

class SłowoAdmin(admin.ModelAdmin):
    list_display = ['slowo', 'jest_negatywne', 'jest_pozytywne']
    list_filter = ['jest_negatywne', 'jest_pozytywne']

admin.site.register(Slowo, SłowoAdmin)