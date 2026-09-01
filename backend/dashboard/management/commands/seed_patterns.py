"""
Management command to seed ScamPattern with curated, research-informed templates.

Install at: core/management/commands/seed_patterns.py
(create empty __init__.py files in management/ and management/commands/ if
they don't exist yet)

Run:
    python manage.py seed_patterns

Safe to re-run — uses get_or_create keyed on template_text, so running it
twice will not create duplicate rows.

Sources these patterns are adapted from (documented modus operandi, not
verbatim captured messages — say this plainly if a judge asks):
  - cybercrime.gov.in (I4C / NCRP) advisories on smishing and digital arrest
  - Chakshu / Sanchar Saathi (DoT) reporting categories
  - State police advisories (Haryana, Mumbai, Maharashtra DGIPR) on the
    electricity-bill and courier-customs scam patterns
"""

import re
from django.core.management.base import BaseCommand
from dashboard.models import ScamPattern  # adjust "core" if your app is named differently


def normalize(text: str) -> str:
    """Same normalization used at request time in the matching pipeline —
    keep this in one shared place (e.g. core/matching.py) and import it
    both here and in your /api/analyze/ view, don't redefine it twice."""
    text = text.lower()
    text = re.sub(r"http\S+|www\.\S+", "<URL>", text)
    text = re.sub(r"[^\w\s<>]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# category values MUST match ScamPattern's CATEGORY_CHOICES keys exactly
PATTERNS = [
    # ---------------- KYC ----------------
    ("KYC", "Your KYC has expired. Update your KYC immediately or your bank account will be blocked."),
    ("KYC", "Your bank KYC is incomplete. Verify your account now to avoid suspension."),
    ("KYC", "KYC verification is required today. Click the link below to keep your account active."),
    ("KYC", "Your account will be suspended due to pending KYC verification. Complete the verification immediately."),
    ("KYC", "Please verify your bank account using the link provided. Enter your OTP and card details to complete KYC."),

    # ---------------- ELECTRICITY ----------------
    ("ELECTRICITY", "Your electricity power will be disconnected tonight because your previous bill was not updated. Contact the electricity officer immediately."),
    ("ELECTRICITY", "Your electricity bill is pending. Pay immediately to avoid disconnection of your power supply."),
    ("ELECTRICITY", "Electricity KYC update is required today. Call the officer or your connection will be disconnected."),
    ("ELECTRICITY", "Your electricity connection is scheduled for disconnection due to an unpaid bill. Verify your payment immediately."),
    ("ELECTRICITY", "Your last electricity payment was not updated. Contact the electricity department now to prevent service interruption."),

    # ---------------- COURIER ----------------
    ("COURIER", "Your parcel has been held by customs. Pay the required charges immediately to avoid return of the package."),
    ("COURIER", "Your shipment could not be delivered due to pending customs charges. Complete payment using the link provided."),
    ("COURIER", "A parcel registered in your name has been stopped. Contact the courier department immediately for verification."),
    ("COURIER", "Your international package is pending clearance. Pay the processing fee now to release your parcel."),
    ("COURIER", "Your parcel is linked to an illegal shipment. Contact the courier officer immediately to avoid legal action."),

    # ---------------- JOB / LOAN ----------------
    ("JOB", "Work from home and earn high income every day. Pay a small registration fee to start your job."),
    ("JOB", "Congratulations! You have been selected for a high-paying job. Pay the registration fee to confirm your position."),
    ("JOB", "Earn thousands of rupees by completing simple online tasks. Pay the training fee to activate your account."),
    ("JOB", "Guaranteed online job with high earnings and no experience required. Pay the software or registration charges to begin."),
    ("JOB", "Your loan has been approved. Pay the processing or insurance fee before the loan amount can be released."),

    # ---------------- GOVERNMENT / DIGITAL ARREST ----------------
    ("GOVERNMENT", "Your mobile number and Aadhaar details are linked to an illegal activity. Contact the police officer immediately."),
    ("GOVERNMENT", "A case has been registered against you. You must verify your identity immediately to avoid arrest."),
    ("GOVERNMENT", "This is an official notification from the cyber crime department. Respond immediately regarding the investigation against your identity."),
    ("GOVERNMENT", "Your bank account is involved in a criminal investigation. Transfer the required amount for verification to avoid legal action."),
    ("GOVERNMENT", "Your identity has been used for illegal transactions. Stay on the video call and follow the officer's instructions to clear the case."),

    # ---------------- SEXTORTION ----------------
    ("SEXTORTION", "We have your private photos and videos. Send money immediately or they will be shared with your contacts."),
    ("SEXTORTION", "Pay the requested amount within 24 hours or your private video will be sent to your family and friends."),
    ("SEXTORTION", "Your video has been recorded. Transfer the money now if you want us to delete it."),
    ("SEXTORTION", "We will publish your private images online unless you send the payment immediately."),
    ("SEXTORTION", "Your private content will be shared publicly. Pay the demanded amount to stop the video from being released."),
]


class Command(BaseCommand):
    help = "Seed ScamPattern with 30 curated scam templates across 6 categories"

    def handle(self, *args, **options):
        created_count = 0
        skipped_count = 0

        for category, template_text in PATTERNS:
            _, created = ScamPattern.objects.get_or_create(
                template_text=template_text,
                defaults={
                    "category": category,
                    "normalized_text": normalize(template_text),
                    "sighting_count": 0,
                },
            )
            if created:
                created_count += 1
            else:
                skipped_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done. Created {created_count} new patterns, skipped {skipped_count} already present."
        ))