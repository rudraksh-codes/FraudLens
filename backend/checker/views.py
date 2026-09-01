from django.shortcuts import render

# Create your views here.



def checker(request):
    result = None
    if request.method == "POST":
        text = request.POST.get("text", "").strip() 




# # Your analysis pipeline
#         rule_result = check_rules(text)
#         ml_result = predict(text)
#         pattern_result = match_pattern(text)

#         score = calculate_score(
#             rule_result,
#             ml_result,
#             pattern_result
#         )

#         llm_result = get_llm_explanation(text)

#         # Save to database
#         submission = Submission.objects.create(
#             raw_text=text,
#             score=score,
#             matched_pattern=pattern_result["pattern"],
#             match_score=pattern_result["score"],
#             risk_level=get_risk_level(score),
#             llm_explaination=llm_result["explanation"],
#             recommended_action=llm_result["recommended_action"],
#         )

#         # Data for template
#         result = {
#             "risk_level": submission.risk_level,
#             "score": submission.score,
#             "category": (
#                 submission.matched_pattern.category
#                 if submission.matched_pattern
#                 else None
#             ),
#             "matched_pattern": (
#                 submission.matched_pattern.template_text
#                 if submission.matched_pattern
#                 else None
#             ),
#             "match_score": submission.match_score,
#             "evidence": rule_result["evidence"],
#             "llm_explanation": submission.llm_explaination,
#             "recommended_action": submission.recommended_action,
#         }
    result = {
    "risk_level": "HIGH",
    "score": 90,
    "category": "Bank / KYC",
    "matched_pattern": "Your KYC has expired. Update immediately or your account will be blocked.",
    "match_score": 89,
    "evidence": [
        "Urgency language detected",
        "Sensitive information (OTP) requested",
        "Suspicious URL detected",
        "Known scam pattern matched"
    ],
    "llm_explanation": "This message creates urgency, asks for sensitive banking information, and contains a suspicious link. It closely resembles a known KYC scam pattern.",
    "recommended_action": "Do not click the link or share your OTP, PIN, CVV, or other banking information."
    }



    context = dict(result = result)
    return render(request, "checker.html", context)


