from django.contrib import admin
from . import models


class RoomModelAdmin(admin.ModelAdmin):
    readonly_fields = ["uuid"]


class QuoteModelAdmin(admin.ModelAdmin):
    readonly_fields = ["user"]


admin.site.register(models.Room, RoomModelAdmin)
admin.site.register(models.Quote, QuoteModelAdmin)
