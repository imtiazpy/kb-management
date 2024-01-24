from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model


USER = get_user_model()


class Fisherman(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    location = models.CharField(_("Location"), max_length=200)
    phone = models.CharField(_("Phone"), max_length=11)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class Harvest(models.Model):
    title = models.CharField(_("Title"), max_length=100)
    fisherman = models.ForeignKey(Fisherman, on_delete=models.SET_NULL, null=True, related_name="harvests")
    fish_qty = models.FloatField(_("Quantity"))
    fisherman_bill = models.FloatField(_("Bill"))
    other_cost = models.FloatField(_("Other Cost"))
    created_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, related_name='staff_harvests')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"