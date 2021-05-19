from django.contrib import admin
from . import models


class HistoryModelAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at"]


admin.site.register(models.Profile)
admin.site.register(models.History, HistoryModelAdmin)
