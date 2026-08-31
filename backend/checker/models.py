from django.db import models
# Create your models here.



class Submission(models.Model):

    class RiskChoices(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    raw_text = models.TextField(
        max_length=2000, 
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True, 
        db_index=True 
    )

    score = models.IntegerField()

    matched_pattern = models.ForeignKey(
        "dashboard.ScamPattern",
        on_delete=models.SET_NULL,
        null=True, #matched nothing 
        blank=True, #form can be blank
        related_name="matches"
    )

    match_score = models.FloatField(
        null=True, 
        blank=True
    )

    risk_level = models.CharField(
        max_length=10, 
        choices=RiskChoices
    )

    llm_explaination = models.TextField(
        blank=True 
    )

    recommended_action = models.TextField(
        blank=True
    )

    reported = models.BooleanField(
        default = False
    )

    def __str__(self):
        return self.raw_text
