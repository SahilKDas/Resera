import json

from django.contrib.auth.models import User
from django.test import Client, TestCase

from .models import Opportunity


class AuthTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.csrf_token = self.client.get("/api/auth/csrf/").json()["csrfToken"]

    def post(self, path, payload):
        return self.client.post(
            path,
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_X_CSRFTOKEN=self.csrf_token,
        )

    def test_registration_creates_authenticated_session(self):
        response = self.post(
            "/api/auth/register/",
            {
                "username": "diver",
                "email": "diver@example.com",
                "password": "A-strong-passphrase-2026",
                "password_confirm": "A-strong-passphrase-2026",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.client.get("/api/auth/me/").json()["user"]["username"], "diver")

    def test_registration_requires_csrf(self):
        response = Client(enforce_csrf_checks=True).post(
            "/api/auth/register/",
            data=json.dumps({"username": "x"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)


class OpportunityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("researcher", password="A-strong-passphrase-2026")
        self.approved = Opportunity.objects.create(
            title="Published study",
            organization="Resera Lab",
            summary="A public opportunity.",
            source_url="https://example.com/approved",
            status=Opportunity.Status.APPROVED,
            submitted_by=self.user,
        )
        Opportunity.objects.create(
            title="Needs review",
            organization="Resera Lab",
            summary="A pending opportunity.",
            source_url="https://example.com/pending",
            submitted_by=self.user,
        )

    def test_public_feed_only_contains_approved_records(self):
        records = self.client.get("/api/opportunities/").json()["opportunities"]
        self.assertEqual([record["id"] for record in records], [self.approved.id])

    def test_authenticated_member_can_submit_for_review(self):
        self.client.force_login(self.user)
        response = self.client.post(
            "/api/opportunities/",
            data=json.dumps(
                {
                    "title": "Ocean fieldwork",
                    "organization": "Blue Institute",
                    "summary": "Help catalog coastal species.",
                    "field": "natural-sciences",
                    "source_url": "https://example.com/fieldwork",
                    "remote": False,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["opportunity"]["status"], "pending")

    def test_anonymous_submission_is_rejected(self):
        response = self.client.post(
            "/api/opportunities/",
            data=json.dumps({}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)
