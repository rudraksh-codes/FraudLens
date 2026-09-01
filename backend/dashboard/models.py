from django.db import models
from .utils import normalize_text

# Create your models here.
class ScamPattern(models.Model):

    def save(self, *args, **kwargs):
        self.normalized_text = normalize_text(self.template_text)
        super().save(*args, **kwargs)


    class CategoryChoices(models.TextChoices):
        KYC = 'kyc', 'Bank / KYC'
        ELECTRICITY = 'electricity', 'Electricity Disconnection'
        COURIER = 'courier', 'Courier / Customs'
        JOB = 'job', 'Job / Loan Offer'
        GOVERNMENT = 'government', 'Government Impersonation'
        SEXTORTION = 'sextortion', 'Sextortion'

    category = models.CharField(
        max_length=20,
        choices=CategoryChoices
    )

    template_text = models.TextField()

    normalized_text = models.TextField()

    sighting_count = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.template_text