from django.contrib import admin

from .models import CustomUser, Follow


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email')
    list_display_links = ('id',)
    list_filter = ('email', 'first_name')
    list_editable = ('username', 'first_name', 'last_name', 'email')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    list_display_links = ('id',)
    list_filter = ('user',)
    list_editable = ('user', 'author')


admin.site.register(Follow, FollowAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
