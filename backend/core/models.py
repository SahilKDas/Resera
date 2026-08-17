from django.contrib.auth.models import User
from django.db import models


class Opportunity(models.Model):
    class Field(models.TextChoices):
        NATURAL_SCIENCES = "natural-sciences", "Natural sciences"
        TECHNOLOGY = "technology", "Technology"
        HUMANITIES = "humanities", "Humanities"
        SOCIAL_IMPACT = "social-impact", "Social impact"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending review"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    title = models.CharField(max_length=180)
    organization = models.CharField(max_length=180)
    summary = models.TextField()
    field = models.CharField(max_length=32, choices=Field.choices, default=Field.OTHER)
    location = models.CharField(max_length=180, blank=True)
    remote = models.BooleanField(default=False)
    eligibility = models.TextField(blank=True)
    deadline = models.DateField(null=True, blank=True)
    source_url = models.URLField()
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="opportunities")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["deadline", "-created_at"]

    def __str__(self):
        return self.title
