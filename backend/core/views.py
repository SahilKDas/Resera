import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from .models import Opportunity


def body(request):
    try:
        return json.loads(request.body or "{}")
    except json.JSONDecodeError as error:
        raise ValidationError("Request body must be valid JSON.") from error


def error(message, status=400, fields=None):
    payload = {"error": message}
    if fields:
        payload["fields"] = fields
    return JsonResponse(payload, status=status)


def user_data(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_staff": user.is_staff,
    }


def opportunity_data(item):
    return {
        "id": item.id,
        "title": item.title,
        "organization": item.organization,
        "summary": item.summary,
        "field": item.field,
        "field_label": item.get_field_display(),
        "location": item.location,
        "remote": item.remote,
        "eligibility": item.eligibility,
        "deadline": item.deadline.isoformat() if item.deadline else None,
        "source_url": item.source_url,
        "status": item.status,
        "submitted_by": item.submitted_by.username,
        "created_at": item.created_at.isoformat(),
    }


@require_GET
def health(request):
    return JsonResponse({"status": "ok"})


@require_GET
@ensure_csrf_cookie
def csrf(request):
    from django.middleware.csrf import get_token

    return JsonResponse({"csrfToken": get_token(request)})


@require_POST
def register(request):
    try:
        data = body(request)
    except ValidationError as exc:
        return error(exc.messages[0])

    username = str(data.get("username", "")).strip()
    email = str(data.get("email", "")).strip()
    password = str(data.get("password", ""))
    password_confirm = str(data.get("password_confirm", ""))
    if not username or not email or not password:
        return error("Username, email, and password are required.")
    if password != password_confirm:
        return error("Passwords do not match.", fields={"password_confirm": ["Passwords do not match."]})
    if User.objects.filter(username__iexact=username).exists():
        return error("That username is already in use.", fields={"username": ["Already in use."]})
    if User.objects.filter(email__iexact=email).exists():
        return error("That email is already registered.", fields={"email": ["Already registered."]})

    candidate = User(username=username, email=email)
    try:
        validate_password(password, user=candidate)
    except ValidationError as exc:
        return error("Choose a stronger password.", fields={"password": exc.messages})

    user = User.objects.create_user(username=username, email=email, password=password)
    login(request, user)
    return JsonResponse({"user": user_data(user)}, status=201)


@require_POST
def sign_in(request):
    try:
        data = body(request)
    except ValidationError as exc:
        return error(exc.messages[0])
    user = authenticate(
        request,
        username=str(data.get("username", "")).strip(),
        password=str(data.get("password", "")),
    )
    if user is None:
        return error("The username or password is incorrect.", status=401)
    login(request, user)
    return JsonResponse({"user": user_data(user)})


@require_POST
def sign_out(request):
    logout(request)
    return JsonResponse({"ok": True})


@require_GET
def me(request):
    return JsonResponse({"user": user_data(request.user) if request.user.is_authenticated else None})


@require_http_methods(["GET", "POST"])
def opportunities(request):
    if request.method == "GET":
        records = Opportunity.objects.select_related("submitted_by")
        if request.user.is_staff and request.GET.get("include_pending") == "1":
            records = records.exclude(status=Opportunity.Status.REJECTED)
        else:
            records = records.filter(status=Opportunity.Status.APPROVED)
        return JsonResponse({"opportunities": [opportunity_data(item) for item in records]})

    if not request.user.is_authenticated:
        return error("Sign in to submit an opportunity.", status=401)
    try:
        data = body(request)
    except ValidationError as exc:
        return error(exc.messages[0])

    required = ("title", "organization", "summary", "source_url")
    missing = [field for field in required if not str(data.get(field, "")).strip()]
    if missing:
        return error("Complete all required fields.", fields={field: ["Required."] for field in missing})
    if data.get("field", Opportunity.Field.OTHER) not in Opportunity.Field.values:
        return error("Choose a valid research field.", fields={"field": ["Invalid choice."]})

    item = Opportunity(
        title=str(data["title"]).strip(),
        organization=str(data["organization"]).strip(),
        summary=str(data["summary"]).strip(),
        field=data.get("field", Opportunity.Field.OTHER),
        location=str(data.get("location", "")).strip(),
        remote=bool(data.get("remote", False)),
        eligibility=str(data.get("eligibility", "")).strip(),
        deadline=data.get("deadline") or None,
        source_url=str(data["source_url"]).strip(),
        submitted_by=request.user,
    )
    try:
        item.full_clean()
    except ValidationError as exc:
        return error("Review the opportunity details.", fields=exc.message_dict)
    item.save()
    return JsonResponse({"opportunity": opportunity_data(item)}, status=201)


@require_http_methods(["PATCH"])
def moderate_opportunity(request, opportunity_id):
    if not request.user.is_staff:
        return error("Staff access is required.", status=403)
    try:
        data = body(request)
    except ValidationError as exc:
        return error(exc.messages[0])
    status = data.get("status")
    if status not in Opportunity.Status.values:
        return error("Choose a valid moderation status.")
    item = get_object_or_404(Opportunity, pk=opportunity_id)
    item.status = status
    item.save(update_fields=["status", "updated_at"])
    return JsonResponse({"opportunity": opportunity_data(item)})
