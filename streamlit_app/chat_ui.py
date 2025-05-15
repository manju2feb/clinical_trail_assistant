import streamlit as st
import requests
import csv
import datetime

st.set_page_config(page_title="Clinical Trial Assistant", layout="wide")

st.title("Clinical Trial Assistant Chatbot")
st.markdown("Ask any question about ongoing clinical trials. Example: *What are the phase 3 cancer trials in the US?*")

# Store chat history in Streamlit session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
st.sidebar.header("🔍 Filters")

phase = st.sidebar.selectbox("Trial Phase", ["", "Phase 1", "Phase 2", "Phase 3", "Phase 4"])
country = st.sidebar.text_input("Location Country")
sponsor = st.sidebar.text_input("Sponsor Name")

filters = {}
if phase:
    filters["Phase"] = phase
if country:
    filters["LocationCountry"] = country
if sponsor:
    filters["Sponsor"] = sponsor


# User input
query = st.text_input("Your question:")

if query:
    with st.spinner("Thinking..."):
        try:
            # Send question and filters to FastAPI
            response = requests.post(
                "http://localhost:8000/ask",
                json={"question": query, "filters": filters}
            )
            result = response.json()

            answer = result.get("answer", "Sorry, no answer returned.")
            sources = result.get("sources", [])

            # Save to history
            st.session_state.chat_history.append((query, answer, sources))

            # Log to CSV
            def log_chat(question, answer):
                import csv, datetime
                log_path = "streamlit_app/chat_logs.csv"
                with open(log_path, "a", newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([datetime.datetime.now(), question, answer])

            log_chat(query, answer)

        except Exception as e:
            st.error(f"Error: {e}")


# Display chat history
for q, a, s in reversed(st.session_state.chat_history):
    st.markdown(f"**You:** {q}")
    st.markdown(f"**Assistant:** {a}")

    if s:
        with st.expander("Sources"):
            for i, meta in enumerate(s):
                st.markdown(f"**Source {i+1}**")
                for k, v in meta.items():
                    st.markdown(f"- **{k}**: {v}")

# def log_chat(question, answer):
#     log_path = "streamlit_app/chat_logs.csv"
#     with open(log_path, "a", newline='', encoding='utf-8') as f:
#         writer = csv.writer(f)
#         writer.writerow([datetime.datetime.now(), question, answer])

# log_chat(query, answer)
