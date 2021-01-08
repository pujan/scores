from django.contrib import admin

from .models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'type', 'method')

    def user_name(self, obj):
        return obj.user.username
    user_name.short_description = 'Nazwa'
    user_name.allow_tags = False
