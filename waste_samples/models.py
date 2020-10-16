"""
The models for the Waste Samples App.
"""

from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User

class WasteSample(models.Model):
    """
    Represents a single Waste Sample.

    A WasteSample is created by a user and contains the creation date,
    level of waste and its coordinates.
    """
    sampling_date   = models.DateTimeField('Sample Created', auto_now_add=True)
    update_date     = models.DateTimeField('Last Change', auto_now=True)
    waste_level     = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10)])
    user            = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    longitude       = models.DecimalField(max_digits=9, decimal_places=6)
    latitude        = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        """String representation of WasteSample."""
        return (
            f"{self.waste_level} by "
            f"{User.objects.get(username=self.user).username if self.user else 'Null User'}"
        )
