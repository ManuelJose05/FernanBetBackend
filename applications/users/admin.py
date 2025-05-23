from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'email','course','level','experience','is_active']
    filer_fieldsets = ('first_name','course','level','is_active')
