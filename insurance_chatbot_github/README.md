# Insurance Enquiry Chatbot

A beginner-friendly, rule-based Python chatbot that demonstrates basic Natural Language Processing (NLP) concepts:
- Intent identification
- Entity extraction (policy type, claim type, date and support service)
- General insurance policy information
- Claim process and document checklists
- Renewal and support guidance
- Conversation context for follow-up questions

## Requirements

- Python 3.9 or newer
- No third-party packages are required

## Run locally

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run:

   ```bash
   python insurance_chatbot.py
   ```

   On some Windows installations, use:

   ```bash
   py insurance_chatbot.py
   ```

4. Type a question, for example:
   - `hello`
   - `show me health insurance policy`
   - `what is the premium for life insurance`
   - `how do I file a motor insurance claim`
   - `what documents do I need for travel insurance`
   - `I need customer care`
5. Type `bye` to exit.

## Run in GitHub Codespaces

1. Sign in to GitHub and create a new repository.
2. Upload `insurance_chatbot.py` and this `README.md` to the repository.
3. Open the repository's main page.
4. Click **Code** → **Codespaces** → **Create codespace on main**. If Codespaces is unavailable for your account, run the project locally instead.
5. Wait for the browser-based VS Code editor to open.
6. Open **Terminal** → **New Terminal**.
7. Run:

   ```bash
   python insurance_chatbot.py
   ```

8. Type your questions in the terminal panel. Use `bye`, `exit`, or `quit` to stop.

## Important data note

The premiums, coverage amounts and claim-settlement ratios in this demonstration are sample values carried over from the starter project. They have not been verified as current offers or insurer statistics. Do not use them for actual insurance decisions. Replace them with verified, dated information from official insurer documents before presenting this as a real-world service.

## Limitations

This is a keyword-based educational chatbot, not an AI model trained on insurance conversations. It does not connect to an insurer, retrieve live quotes, submit claims, or provide personalised financial/legal advice. Its date recognition is basic and does not validate calendar dates.
