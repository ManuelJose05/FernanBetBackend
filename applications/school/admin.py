from django.contrib import admin
from .models import School


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name','postal_code','city']
    filer_fieldsets = ('name','email','phone','postal_code','city')
