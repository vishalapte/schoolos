from django.contrib import admin

from qux.models import CoreModelAdmin
from .models import BusRoute, BusRider


class BusRouteAdmin(CoreModelAdmin):
    list_display = (
        "id",
        "route",
        "whatsapp",
        "registration",
        "name",
        "teacher",
        "driver",
        "attendant",
        "data",
    )
    list_filter = []


admin.site.register(BusRoute, BusRouteAdmin)


class BusRiderAdmin(CoreModelAdmin):
    list_display = ("id", "rider", "route", "area", "time")
    list_filter = []


admin.site.register(BusRider, BusRiderAdmin)
