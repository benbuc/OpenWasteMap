"""
The models for the Waste Samples App.
"""

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models


class WasteSample(models.Model):
    """
    Represents a single Waste Sample.

    A WasteSample is created by a user and contains the creation date,
    level of waste and its coordinates.
    """

    sampling_date = models.DateTimeField("Sample Created", auto_now_add=True)
    update_date = models.DateTimeField("Last Change", auto_now=True)
    waste_level = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10)])
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        """String representation of WasteSample."""
        user = "Null User"
        if self.user:
            user = get_user_model().objects.get(username=self.user).username

        return f"{self.waste_level} by {user}"
