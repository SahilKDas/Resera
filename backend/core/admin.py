from django.contrib import admin

from .models import Opportunity


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "field", "status", "submitted_by", "created_at")
    list_filter = ("status", "field", "remote")
    search_fields = ("title", "organization", "summary", "submitted_by__username")
    list_editable = ("status",)
    readonly_fields = ("submitted_by", "created_at", "updated_at")
