from django.core.validators import RegexValidator
from django.db import models

from qux.models import CoreModel, default_null_blank


roman2integer = {
    "I": 1,
    "II": 2,
    "III": 3,
    "IV": 4,
    "V": 5,
    "VI": 6,
    "VII": 7,
    "VIII": 8,
    "IX": 9,
    "X": 10,
    "XI": 11,
    "XII": 12,
}


PERSON_CATEGORIES = (
    ("student", "Student"),
    ("faculty", "Faculty"),
    ("staff", "Staff"),
    ("other", "Other"),
)


class Person(CoreModel):
    phone_re = RegexValidator(
        regex=r"^\+?[1-9]\d{4,14}$",
        message="Phone number must be entered in the format: '+999999999'. "
        "Up to 15 digits allowed.",
    )

    last_name = models.CharField(max_length=32)
    first_name = models.CharField(max_length=32, **default_null_blank)
    middle_name = models.CharField(max_length=64, **default_null_blank)
    category = models.CharField(
        max_length=8, choices=PERSON_CATEGORIES, default="student"
    )
    grade = models.IntegerField(**default_null_blank)
    phone = models.CharField(max_length=16, validators=[phone_re], **default_null_blank)
    email = models.EmailField(**default_null_blank)
    address = models.TextField(**default_null_blank)
    address_city = models.CharField(max_length=32, default="Pune")
    address_pincode = models.CharField(max_length=6, **default_null_blank)
    address_country = models.CharField(max_length=2, default="IN")
    is_student = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    class Meta:
        db_table = "person"
        unique_together = [
            ("first_name", "last_name"),
            ("first_name", "last_name", "phone"),
            ("first_name", "last_name", "email"),
        ]

    @classmethod
    def create_record(cls, record):
        if not hasattr(record.get("name", None), "split"):
            return None

        n = [x.strip().upper() for x in record["name"].strip().split(" ")]

        params = {
            "first_name": n[0],
            "phone": record["phone"],
            "grade": roman2integer.get(record.get("grade", None), None),
        }
        if len(n) > 1:
            params["last_name"] = n[-1]
        if len(n) > 2:
            params["middle_name"] = " ".join(n[1:-1])

        try:
            obj, created = cls.objects.get_or_create(**params)
            obj.address = record["address"]
            obj.save()
        except:
            obj = None

        return obj

    def name(self):
        result = ""
        if self.first_name:
            result = self.first_name
        if self.last_name:
            if result:
                result += " " + self.last_name
            else:
                result = self.last_name

        return result

    def catgrade(self):
        return self.grade if self.grade else self.category.upper()[0]

    def __repr__(self):
        return f"<{self.name()} :: {self.phone}>"

    def __str__(self):
        return self.name()
