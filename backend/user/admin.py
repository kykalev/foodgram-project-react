from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email')
    list_display_links = ('id',)
    list_filter = ('email', 'first_name')
    list_editable = ('username', 'first_name', 'last_name', 'email')


admin.site.register(CustomUser, CustomUserAdmin)
