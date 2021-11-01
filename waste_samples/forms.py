"""
Formulars for the Waste Sample management.
"""

from django.forms import ModelForm

from .models import WasteSample


class WasteSampleCreationForm(ModelForm):
    """The form used to create a new Waste Sample."""

    class Meta:
        """Define fields for the Form."""

        model = WasteSample
        fields = ["waste_level", "latitude", "longitude"]
