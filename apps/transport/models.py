from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.models import Person
from qux.models import CoreModel, default_null_blank


class BusRoute(CoreModel):
    route = models.CharField(max_length=8, **default_null_blank)
    registration = models.CharField(max_length=10, **default_null_blank)
    name = models.CharField(max_length=128)
    teacher = models.ForeignKey(
        Person,
        on_delete=models.DO_NOTHING,
        related_name="route_bus_parent",
        **default_null_blank,
    )
    driver = models.ForeignKey(
        Person,
        on_delete=models.DO_NOTHING,
        related_name="route_driver",
        **default_null_blank,
    )
    attendant = models.ForeignKey(
        Person,
        on_delete=models.DO_NOTHING,
        related_name="route_attendant",
        **default_null_blank,
    )
    whatsapp = models.URLField(max_length=128, **default_null_blank)
    data = models.JSONField(**default_null_blank)

    class Meta:
        verbose_name = "Bus Route"
        ordering = ["route", "id"]

    def __repr__(self):
        return f"<{self.id}: [{self.route}] {self.name}>"

    def __str__(self):
        return f"{self.route}"

    @classmethod
    def create_record(cls, route):
        print(route)

        obj = cls()
        obj.name = str(route["name"])
        obj.data = route
        obj.save()

        return obj

    def as_dict(self):
        result = self.to_dict()
        result["id"] = self.id
        result.pop("data")
        print(result)
        return result


class BusRider(CoreModel):
    rider = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    route = models.ForeignKey(
        BusRoute, on_delete=models.DO_NOTHING, related_name="route_riders"
    )
    area = models.CharField(max_length=64, **default_null_blank)
    time = models.TimeField(**default_null_blank)

    class Meta:
        verbose_name = "Bus Rider"
        ordering = ["route", "rider"]
        unique_together = [("route", "rider")]
