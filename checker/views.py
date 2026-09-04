# from django.shortcuts import render
# from .services.ml_model import spam_ham_detector
# # Create your views here.



# def checker(request):
#     result = None
#     if request.method == "POST":
#         text = request.POST.get("text", "").strip() 




# # # Your analysis pipeline
# #         rule_result = check_rules(text)

#         ml_result = spam_ham_detector(text)
    
# #         pattern_result = match_pattern(text)

# #         score = calculate_score(
# #             rule_result,
# #             ml_result,
# #             pattern_result
# #         )

# #         llm_result = get_llm_explanation(text)

# #         # Save to database
# #         submission = Submission.objects.create(
# #             raw_text=text,
# #             score=score,
# #             matched_pattern=pattern_result["pattern"],
# #             match_score=pattern_result["score"],
# #             risk_level=get_risk_level(score),
# #             llm_explaination=llm_result["explanation"],
# #             recommended_action=llm_result["recommended_action"],
# #         )

# #         # Data for template
# #         result = {
# #             "risk_level": submission.risk_level,
# #             "score": submission.score,
# #             "category": (
# #                 submission.matched_pattern.category
# #                 if submission.matched_pattern
# #                 else None
# #             ),
# #             "matched_pattern": (
# #                 submission.matched_pattern.template_text
# #                 if submission.matched_pattern
# #                 else None
# #             ),
# #             "match_score": submission.match_score,
# #             "evidence": rule_result["evidence"],
# #             "llm_explanation": submission.llm_explaination,
# #             "recommended_action": submission.recommended_action,
# #         }
#         result = {
#             "ml_result" : ml_result,
#         "risk_level": "HIGH",
#         "score": 90,
#         "category": "Bank / KYC",
#         "matched_pattern": "Your KYC has expired. Update immediately or your account will be blocked.",
#         "match_score": 89,
#         "evidence": [
#             "Urgency language detected",
#             "Sensitive information (OTP) requested",
#             "Suspicious URL detected",
#             "Known scam pattern matched"
#         ],
#         "llm_explanation": "This message creates urgency, asks for sensitive banking information, and contains a suspicious link. It closely resembles a known KYC scam pattern.",
#         "recommended_action": "Do not click the link or share your OTP, PIN, CVV, or other banking information."
#         }



#     context = dict(result = result)
#     return render(request, "checker.html", context)



# checker/views.py
import logging

from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import Submission  # adjust if Submission lives in checker.models instead
from .services.analyzer import analyze_text

logger = logging.getLogger(__name__)


@require_http_methods(["GET", "POST"])
def checker(request):
    result = None
    error = None

    if request.method == "POST":
        # Your checker.html textarea is name="text" — "message" would
        # silently read empty on every submission.
        text = request.POST.get("text", "").strip()[:2000]

        if not text:
            error = "Please enter a message or URL."
        else:
            try:
                analysis = analyze_text(text)

                print(dict(
                    raw_text=text,
                    score=analysis["rule_score"],
                    matched_pattern=analysis["matched_pattern"],
                    match_score=analysis["pattern_score"],
                    risk_level=analysis["risk_level"],
                    llm_explanation=analysis["llm_explanation"],  # correct spelling
                    recommended_action=analysis["recommended_action"],
                ))

                submission = Submission.objects.create(
                    raw_text=text,
                    score=analysis["rule_score"],
                    matched_pattern=analysis["matched_pattern"],
                    match_score=analysis["pattern_score"],
                    risk_level=analysis["risk_level"],
                    llm_explanation=analysis["llm_explanation"],  # correct spelling
                    recommended_action=analysis["recommended_action"],
                )


                result = {
                    "risk_level": submission.risk_level,
                    "score": analysis["score"],
                    "category": analysis["category"],
                    "matched_pattern": (
                        submission.matched_pattern.template_text
                        if submission.matched_pattern else "No close match found"
                    ),
                    "match_score": round(analysis["pattern_score"]),
                    "evidence": analysis["evidence"],
                    "llm_explanation": submission.llm_explanation,
                    "recommended_action": submission.recommended_action,
                }

            except Exception:
                # Log the real error server-side; show the user something
                # calm instead of a raw traceback string during a demo.
                logger.exception("Checker analysis failed")
                error = "Something went wrong while analyzing this message. Please try again."

    return render(request, "checker.html", {"result": result, "error": error})