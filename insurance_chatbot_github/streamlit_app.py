import contextlib
import io

import streamlit as st

import insurance_chatbot as bot

st.set_page_config(
    page_title="Insurance Assistant",
    page_icon="🛡️",
    layout="centered",
)

st.title("🛡️ Insurance Enquiry Assistant")
st.caption("Ask questions about policies, premiums, claims, documents and renewals.")
st.info(
    "This is an educational demonstration. Premiums, coverage amounts and "
    "claim ratios are sample data, not verified insurance offers."
)

# ---------- Session state ----------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! 👋 I'm your Insurance Enquiry Assistant. "
                "You can ask me about health, life, motor, travel or home insurance."
            ),
        }
    ]

if "bot_context" not in st.session_state:
    st.session_state.bot_context = {"policy_type": None, "waiting_for": None}


# ---------- Run the existing chatbot and capture its printed output ----------
def get_bot_reply(user_input, context):
    """Mirror the logic of start_chatbot(), but return the text instead of printing."""
    buffer = io.StringIO()
    text = user_input.strip()

    with contextlib.redirect_stdout(buffer):
        if not text:
            print("Bot: Please type a question.")

        elif text.lower() in {"bye", "exit", "quit"}:
            print("Bot: Thank you for using the Insurance Enquiry Chatbot. Goodbye!")

        elif context.get("waiting_for"):
            waiting_for = context["waiting_for"]
            policy_type = bot.extract_policy_type(text)

            if not policy_type:
                print("Bot: Please choose health, life, motor, travel or home.")
            else:
                context["policy_type"] = policy_type
                context["waiting_for"] = None

                if waiting_for == "POLICY":
                    bot.print_policy_information(policy_type)
                elif waiting_for == "PREMIUM":
                    info = bot.POLICIES[policy_type]
                    print(
                        f"Bot: The sample premium for {info['name']} is "
                        f"₹{info['premium']:,} per year."
                    )
                    print("These figures are illustrative demo values, not a quote.")
                elif waiting_for == "CLAIM":
                    bot.print_claim_process(policy_type)
                elif waiting_for == "DOCUMENTS":
                    bot.print_document_information(policy_type)

        else:
            bot.chatbot_response(text, context)

    output = buffer.getvalue().strip()

    # Separate the main answer from the NLP analysis block
    marker = "--- NLP Analysis ---"
    if marker in output:
        answer, analysis = output.split(marker, 1)
        analysis = marker + analysis
    else:
        answer, analysis = output, ""

    answer = "\n".join(
        line[5:] if line.startswith("Bot: ") else line
        for line in answer.splitlines()
    )
    return answer.strip(), analysis.strip()

# ---------- Show chat history ----------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.text(message["content"])
        else:
            st.write(message["content"])

        if message.get("analysis"):
            with st.expander("NLP analysis"):
                st.code(message["analysis"])

# ---------- Handle new input ----------
user_input = st.chat_input("Ask about insurance...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    answer, analysis = get_bot_reply(user_input, st.session_state.bot_context)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "analysis": analysis}
    )
    st.rerun()
