"""
Data models for GET /admin/analytics.

Every field here is computed from real, already-existing data -
nothing is fabricated or estimated. Where this project genuinely
doesn't track something (API costs, request latency for image
analysis, provider usage for /analyze/image specifically), the field
either doesn't exist here or is explicitly None with a note, rather
than a made-up number. See app/routes/admin_analytics.py for exactly
where each field comes from.
"""

from pydantic import BaseModel


class ProviderCounts(BaseModel):
    success: int
    failure: int


class ProviderRow(BaseModel):
    provider: str
    success: int
    failure: int
    avg_latency_ms: float | None = None


class AIProviderStats(BaseModel):
    # One row per provider that has at least one logged attempt in the
    # window (any provider in the gateway cascade, not just two).
    providers: list[ProviderRow] = []
    # Kept for backward compatibility with older clients.
    gemini: ProviderCounts
    groq: ProviderCounts
    # Requests where every configured provider failed and the response
    # fell all the way through to the rule-engine-only fallback.
    all_failed: int
    gemini_avg_latency_ms: float | None
    groq_avg_latency_ms: float | None
    # Explicit, not omitted - see this file's module docstring.
    note: str = (
        "Covers every call that goes through the AI gateway (text analysis, "
        "follow-up chat and image analysis). Attempts skipped because a "
        "provider had no key or was cooling down are not included."
    )


class SeverityBreakdown(BaseModel):
    LOW: int
    MODERATE: int
    HIGH: int
    EMERGENCY: int


class DailyCount(BaseModel):
    date: str  # YYYY-MM-DD
    count: int


class AdminAnalyticsOut(BaseModel):
    generated_at: str
    window_days: int

    total_users: int
    signups_by_day: list[DailyCount]

    total_analyses: int
    analyses_by_day: list[DailyCount]
    severity_breakdown: SeverityBreakdown
    sos_recommended_count: int

    total_reminders: int
    active_reminders: int

    caregiver_links_active: int
    caregiver_links_pending: int
    caregiver_links_revoked: int

    total_passport_documents: int
    total_document_storage_bytes: int

    feedback_positive: int
    feedback_negative: int

    ai_provider_stats: AIProviderStats
