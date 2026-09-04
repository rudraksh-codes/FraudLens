# dashboard/views.py
from datetime import timedelta

from django.db.models import Count
from django.shortcuts import render
from django.utils import timezone

from .models import ScamPattern
from checker.models import Submission

# {'kyc': 'Bank / KYC', 'electricity': 'Electricity Disconnection', ...}
CATEGORY_LABELS = dict(ScamPattern.CategoryChoices.choices)


def dashboard(request):
    scam_patterns = ScamPattern.objects.annotate(
        match_count=Count('matches')
    ).order_by('-sighting_count')

    total_matches = Submission.objects.filter(matched_pattern__isnull=False).count()

    reports_last_7_days = Submission.objects.filter(
        reported=True,
        submitted_at__gte=timezone.now() - timedelta(days=7),
    ).count()

    # Most common category among matched submissions — one query, then a
    # plain dict lookup for the display label (no extra query needed).
    top_category_row = (
        Submission.objects.filter(matched_pattern__isnull=False)
        .values('matched_pattern__category')
        .annotate(count=Count('id'))
        .order_by('-count')
        .first()
    )
    most_matched_category = (
        CATEGORY_LABELS.get(top_category_row['matched_pattern__category'], '—')
        if top_category_row else '—'
    )

    recent_submissions = Submission.objects.select_related('matched_pattern').order_by('-submitted_at')[:10]
    recent_activity = [
        {
            'category': CATEGORY_LABELS.get(s.matched_pattern.category, 'Unclassified') if s.matched_pattern else 'Unclassified',
            'time': s.submitted_at,
            'pattern': s.matched_pattern.template_text if s.matched_pattern else s.raw_text[:80],
            'risk_level': s.risk_level,
            'match_status': bool(s.matched_pattern),
            'reported': s.reported,
        }
        for s in recent_submissions
    ]

    context = {
        'scam_patterns': scam_patterns,
        'total_matches': total_matches,
        'most_matched_category': most_matched_category,
        'reports_last_7_days': reports_last_7_days,
        'recent_activity': recent_activity,
    }
    return render(request, 'dashboard.html', context)