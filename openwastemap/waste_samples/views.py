"""
Views for the Waste Samples App.
"""

from accounts.decorators import verified_account_required
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import generic

from .forms import WasteSampleCreationForm
from .models import WasteSample


class IndexView(generic.ListView):
    """Show recently added samples."""

    template_name = "waste_samples/index.html"
    context_object_name = "samples"

    def get_queryset(self):
        """Return the last 20 samples."""
        return WasteSample.objects.filter(sampling_date__lte=timezone.now()).order_by(
            "-sampling_date"
        )[:20]

    def get_context_data(self, **kwargs):
        """Return Context for template."""
        context = super().get_context_data(**kwargs)
        context["total_samples"] = WasteSample.objects.all().count()
        return context


@verified_account_required
def new_sample(request):
    """Displays a form which allows users to create a new WasteSample."""
    if request.method == "POST":
        form = WasteSampleCreationForm(request.POST)
        if form.is_valid():
            new_waste_sample = form.save(commit=False)
            new_waste_sample.user = request.user
            new_waste_sample.save()

            return redirect("waste_samples:index")
    else:
        form = WasteSampleCreationForm()

    return render(
        request,
        "waste_samples/new_sample.html",
        {
            "form": form,
        },
    )
