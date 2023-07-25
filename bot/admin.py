from django.contrib import admin

from bot.models import TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'verification_code')
    list_filter = ('user',)
    readonly_fields = list_display
