from classifier import classify_and_reply, log_result
from dotenv import load_dotenv
load_dotenv()

sample_emails = [
    {
        "subject": "URGENT: Production server is down",
        "body": "Our main API is returning 500 errors. Customers are affected. Need immediate fix.",
        "sender": "cto@company.com"
    },
    {
        "subject": "Following up on last week's proposal",
        "body": "Hi, just checking in on the proposal I sent over. Let me know if you have questions.",
        "sender": "sales@vendor.com"
    },
    {
        "subject": "You've won a $500 gift card!",
        "body": "Click here to claim your prize. Limited time offer. Act now!",
        "sender": "noreply@sketchy.com"
    },
    {
        "subject": "Team lunch this Friday?",
        "body": "Hey, want to grab lunch with the team this Friday at noon? Let me know if you're in.",
        "sender": "colleague@company.com"
    },
    {
        "subject": "Invoice #4521 overdue - payment required",
        "body": "This is a reminder that invoice #4521 for $2,400 is now 15 days overdue. Please remit payment.",
        "sender": "billing@supplier.com"
    },
    {
        "subject": "Monthly newsletter - March 2026",
        "body": "Here's your monthly roundup of industry news and updates from our team.",
        "sender": "newsletter@techdigest.com"
    },
    {
        "subject": "Interview scheduled for Monday 10am",
        "body": "Hi, confirming your technical interview for Monday at 10am PST via Zoom. Link attached.",
        "sender": "hr@startup.com"
    },
    {
        "subject": "Bug report: login page broken on mobile",
        "body": "Several users have reported they cannot log in on iOS Safari. Issue started this morning.",
        "sender": "support@company.com"
    }
]

print("Processing emails...\n")
for email in sample_emails:
    result = classify_and_reply(email["subject"], email["body"], email["sender"])
    log_result(result)

print("\nDone! Open dashboard.py to see results.")
