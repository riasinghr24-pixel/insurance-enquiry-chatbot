"""
Insurance Enquiry Chatbot
A simple rule-based Python chatbot for general insurance enquiries.

Important:
- Premiums, coverage amounts, and claim-settlement ratios below are sample/demo values.
- Replace them with verified information from an insurer before real-world use.
- This chatbot provides general information, not financial, legal, or insurance advice.
"""

import re

POLICIES = {
    "health": {
        "name": "Health Insurance",
        "premium": 8500,
        "coverage": 500000,
        "tenure": "1 year (renewable)",
        "claim_settlement_ratio": "98%",
    },
    "life": {
        "name": "Life Insurance (Term Plan)",
        "premium": 12000,
        "coverage": 5000000,
        "tenure": "20 years",
        "claim_settlement_ratio": "99%",
    },
    "motor": {
        "name": "Motor Insurance",
        "premium": 6000,
        "coverage": 300000,
        "tenure": "1 year (renewable)",
        "claim_settlement_ratio": "96%",
    },
    "travel": {
        "name": "Travel Insurance",
        "premium": 1500,
        "coverage": 200000,
        "tenure": "Trip duration",
        "claim_settlement_ratio": "94%",
    },
    "home": {
        "name": "Home Insurance",
        "premium": 4000,
        "coverage": 1000000,
        "tenure": "1 year (renewable)",
        "claim_settlement_ratio": "95%",
    },
}

INTENTS = {
    "GREETING": [
        "hello", "hi", "hey", "good morning", "good afternoon", "good evening"
    ],
    "POLICY": [
        "policy", "policies", "plan", "plans", "coverage",
        "types of insurance", "which insurance", "insurance options"
    ],
    "PREMIUM_INFO": [
        "premium", "price", "cost", "how much", "installment", "emi"
    ],
    "CLAIM_PROCESS": [
        "claim", "file a claim", "how to claim", "raise a claim", "claim process"
    ],
    "DOCUMENTS": [
        "documents", "document", "papers", "kyc", "id proof", "required documents"
    ],
    "RENEWAL": ["renew", "renewal", "expiring", "expiry", "due date"],
    "SUPPORT": [
        "agent", "customer care", "help", "complaint", "contact",
        "branch", "talk to someone", "helpline"
    ],
    "GOODBYE": ["bye", "goodbye", "exit", "quit", "thank you"],
}

CLAIM_TYPES = [
    "natural calamity", "reimbursement", "cashless", "accidental",
    "theft", "fire", "medical"
]
SERVICES = ["customer care", "helpline", "agent", "branch", "complaint"]

CLAIM_PROCESS_STEPS = {
    "health": [
        "Inform the insurer/TPA as soon as possible and follow the policy's notification rules.",
        "For cashless treatment, check whether the hospital is in the insurer's network.",
        "For reimbursement, retain bills and proof of payment.",
        "Submit the claim form and requested medical records/bills.",
        "The insurer reviews the claim according to the policy terms.",
    ],
    "motor": [
        "Inform the insurer promptly after the incident.",
        "Contact the police where required, such as for theft or certain accidents.",
        "Follow the insurer's survey and repair authorisation process.",
        "Keep the registration certificate, driving licence, policy and repair documents ready.",
        "The insurer reviews the claim according to the policy terms.",
    ],
    "life": [
        "The nominee/claimant should notify the insurer.",
        "Complete the claim intimation or claim form.",
        "Provide the death certificate, policy details, claimant ID and other requested documents.",
        "The insurer verifies the submission and may request further information.",
        "The insurer communicates its decision under the policy terms.",
    ],
    "travel": [
        "Contact the insurer or assistance provider as soon as practical.",
        "Keep receipts and supporting records, such as medical or police reports when relevant.",
        "Submit the claim form and documents requested for the event.",
        "The insurer reviews the claim under the policy terms.",
    ],
    "home": [
        "Notify the insurer promptly after damage or loss.",
        "Contact the police where relevant, such as for theft or burglary.",
        "Take photographs and retain purchase bills, repair estimates and other evidence.",
        "Cooperate with any surveyor or inspection arranged by the insurer.",
        "The insurer reviews the claim under the policy terms.",
    ],
}

REQUIRED_DOCUMENTS = {
    "health": [
        "Identity proof", "Policy details/copy", "Medical reports",
        "Hospital bills and discharge summary, if applicable"
    ],
    "motor": [
        "Vehicle registration certificate (RC)", "Driving licence",
        "Policy details/copy", "Repair estimate and bills", "Police report if applicable"
    ],
    "life": [
        "Death certificate", "Policy details/copy", "Claimant/nominee identity proof",
        "Bank details", "Completed claim form"
    ],
    "travel": [
        "Policy details/copy", "Passport and travel documents where relevant",
        "Bills/receipts", "Medical or police report if applicable"
    ],
    "home": [
        "Policy details/copy", "Photographs of damage",
        "Purchase bills/repair estimates", "Police report if applicable"
    ],
}


def contains_phrase(text, phrase):
    """Match a phrase without accidentally matching it inside another word."""
    pattern = r"(?<!\w)" + re.escape(phrase.lower()) + r"(?!\w)"
    return re.search(pattern, text.lower()) is not None


def identify_intent(user_text):
    text = user_text.lower().strip()
    # Prefer longer phrases first so a specific phrase is not overshadowed.
    for intent, keywords in INTENTS.items():
        for keyword in sorted(keywords, key=len, reverse=True):
            if contains_phrase(text, keyword):
                return intent
    return "UNKNOWN"


def extract_policy_type(user_text):
    text = user_text.lower()
    # Match specific policy names as well as the basic type words.
    aliases = {
        "health": ["health", "medical insurance"],
        "life": ["life", "term plan", "term insurance"],
        "motor": ["motor", "car insurance", "vehicle insurance", "bike insurance"],
        "travel": ["travel", "trip insurance"],
        "home": ["home", "house insurance", "property insurance"],
    }
    for policy, words in aliases.items():
        if any(contains_phrase(text, word) for word in words):
            return policy
    return None


def extract_claim_type(user_text):
    text = user_text.lower()
    for claim_type in sorted(CLAIM_TYPES, key=len, reverse=True):
        if contains_phrase(text, claim_type):
            return claim_type
    return None


def extract_date(user_text):
    match = re.search(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", user_text)
    if match:
        return match.group()
    text = user_text.lower()
    if contains_phrase(text, "today"):
        return "today"
    if contains_phrase(text, "tomorrow"):
        return "tomorrow"
    return None


def extract_service(user_text):
    text = user_text.lower()
    for service in sorted(SERVICES, key=len, reverse=True):
        if contains_phrase(text, service):
            return service
    return None


def print_policy_information(policy_type):
    info = POLICIES[policy_type]
    print("\nPolicy Information")
    print("------------------")
    print(f"Policy: {info['name']}")
    print(f"Indicative premium: ₹{info['premium']:,} per year")
    print(f"Illustrative coverage: ₹{info['coverage']:,}")
    print(f"Tenure: {info['tenure']}")
    print(f"Sample claim-settlement ratio: {info['claim_settlement_ratio']}")
    print("\nThese figures are demo data, not verified quotes or insurer statistics.")
    print("Check the actual policy wording and insurer's official information.")


def print_claim_process(policy_type, claim_type=None):
    print("\nClaim Process")
    print("-------------")
    if policy_type in CLAIM_PROCESS_STEPS:
        for number, step in enumerate(CLAIM_PROCESS_STEPS[policy_type], start=1):
            print(f"{number}. {step}")
    else:
        print("1. Notify the insurer promptly.")
        print("2. Check the policy wording and claim notification requirements.")
        print("3. Keep relevant supporting documents and receipts.")
        print("4. Submit the claim form and requested documents.")
        print("5. Follow up with the insurer for the claim decision.")
    if claim_type:
        print(f"Claim type mentioned: {claim_type.title()}")
    print("Exact steps and deadlines vary by insurer and policy.")


def print_document_information(policy_type):
    print("\nDocuments Checklist")
    print("-------------------")
    if policy_type in REQUIRED_DOCUMENTS:
        documents = REQUIRED_DOCUMENTS[policy_type]
    else:
        documents = [
            "Identity proof", "Policy details/copy", "Completed claim form",
            "Supporting bills, reports or evidence relevant to the claim"
        ]
    for document in documents:
        print(f"- {document}")
    print("This is a general checklist; confirm the exact requirements with the insurer.")


def print_renewal_information(policy_type=None, date=None):
    print("\nRenewal Information")
    print("-------------------")
    if policy_type:
        print(f"Policy type: {POLICIES[policy_type]['name']}")
    if date:
        print(f"Date mentioned: {date}")
    print("Check the policy schedule or insurer account for the exact expiry date.")
    print("Renewal windows and grace periods differ by policy; confirm them with the insurer.")
    print("Use the insurer's official website or customer support for renewal.")


def print_support_information(service=None):
    print("\nCustomer Support")
    print("----------------")
    if service == "agent":
        print("Contact the insurer through its official website to request an authorised advisor.")
    elif service == "branch":
        print("Use the insurer's official branch locator and search by city or PIN code.")
    elif service == "complaint":
        print("Register the complaint through the insurer's official grievance channel.")
        print("Keep the complaint/reference number for follow-up.")
    else:
        print("Use the contact details printed on your policy document or the insurer's official website.")
    print("Demo contact details are intentionally not provided.")


def chatbot_response(user_input, context):
    text = user_input.lower().strip()
    intent = identify_intent(text)
    policy_type = extract_policy_type(text)
    claim_type = extract_claim_type(text)
    date = extract_date(text)
    service = extract_service(text)

    if policy_type:
        context["policy_type"] = policy_type

    active_policy = policy_type or context.get("policy_type")

    if intent == "GREETING":
        print("\nBot: Hello! Welcome to the Insurance Enquiry Chatbot.")
        print("Bot: Ask me about policies, premiums, claims, documents, renewals or support.")
    elif intent == "POLICY":
        if active_policy:
            print_policy_information(active_policy)
        else:
            print("\nBot: Which policy are you interested in: health, life, motor, travel or home?")
            context["waiting_for"] = "POLICY"
    elif intent == "PREMIUM_INFO":
        if active_policy:
            info = POLICIES[active_policy]
            print(f"\nBot: The sample premium for {info['name']} is ₹{info['premium']:,} per year.")
            print("Bot: Actual premiums depend on the insurer, cover, eligibility and other factors.")
            print("Bot: The amount shown is illustrative, not a quote.")
        else:
            print("\nBot: Which policy's premium do you want to know: health, life, motor, travel or home?")
            context["waiting_for"] = "PREMIUM"
    elif intent == "CLAIM_PROCESS":
        if active_policy:
            print_claim_process(active_policy, claim_type)
        else:
            print("\nBot: Which policy is the claim for: health, life, motor, travel or home?")
            context["waiting_for"] = "CLAIM"
    elif intent == "DOCUMENTS":
        if active_policy:
            print_document_information(active_policy)
        else:
            print("\nBot: Which policy's documents do you need: health, life, motor, travel or home?")
            context["waiting_for"] = "DOCUMENTS"
    elif intent == "RENEWAL":
        print_renewal_information(active_policy, date)
    elif intent == "SUPPORT":
        print_support_information(service)
    elif intent == "GOODBYE":
        print("\nBot: Thank you for using the Insurance Enquiry Chatbot. Goodbye!")
    else:
        print("\nBot: Sorry, I could not understand that.")
        print("Bot: Try asking about policies, premiums, claims, documents, renewal or support.")

    print("\n--- NLP Analysis ---")
    print(f"Intent: {intent}")
    if policy_type:
        print(f"Policy entity: {policy_type}")
    if claim_type:
        print(f"Claim entity: {claim_type}")
    if date:
        print(f"Date entity: {date}")
    if service:
        print(f"Service entity: {service}")
    print("--------------------")
    return intent


def start_chatbot():
    context = {"policy_type": None, "waiting_for": None}
    print("=" * 48)
    print("       INSURANCE ENQUIRY CHATBOT")
    print("=" * 48)
    print("Ask about policies, premiums, claims, documents, renewals or support.")
    print("Type 'bye', 'exit' or 'quit' to stop.")

    while True:
        try:
            user_input = input("\nCustomer: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Chatbot stopped. Goodbye!")
            break

        if not user_input:
            print("Bot: Please type a question.")
            continue

        if user_input.lower() in {"bye", "exit", "quit"}:
            print("Bot: Thank you for using the Insurance Enquiry Chatbot. Goodbye!")
            break

        waiting_for = context.get("waiting_for")
        if waiting_for:
            policy_type = extract_policy_type(user_input)
            if not policy_type:
                print("Bot: Please choose health, life, motor, travel or home.")
                continue

            context["policy_type"] = policy_type
            context["waiting_for"] = None

            if waiting_for == "POLICY":
                print_policy_information(policy_type)
            elif waiting_for == "PREMIUM":
                info = POLICIES[policy_type]
                print(f"Bot: The sample premium for {info['name']} is ₹{info['premium']:,} per year.")
                print("These figures are illustrative demo values, not a quote.")
            elif waiting_for == "CLAIM":
                print_claim_process(policy_type)
            elif waiting_for == "DOCUMENTS":
                print_document_information(policy_type)
            continue

        chatbot_response(user_input, context)


if __name__ == "__main__":
    start_chatbot()
