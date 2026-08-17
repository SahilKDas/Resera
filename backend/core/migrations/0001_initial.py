import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="Opportunity",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=180)),
                ("organization", models.CharField(max_length=180)),
                ("summary", models.TextField()),
                ("field", models.CharField(choices=[("natural-sciences", "Natural sciences"), ("technology", "Technology"), ("humanities", "Humanities"), ("social-impact", "Social impact"), ("other", "Other")], default="other", max_length=32)),
                ("location", models.CharField(blank=True, max_length=180)),
                ("remote", models.BooleanField(default=False)),
                ("eligibility", models.TextField(blank=True)),
                ("deadline", models.DateField(blank=True, null=True)),
                ("source_url", models.URLField()),
                ("status", models.CharField(choices=[("pending", "Pending review"), ("approved", "Approved"), ("rejected", "Rejected")], default="pending", max_length=16)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("submitted_by", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="opportunities", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["deadline", "-created_at"]},
        )
    ]
