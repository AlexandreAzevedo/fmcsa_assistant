import streamlit as st
import time
from src.rag_engine import FMCSAAssistant

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="FMCSA AI Assistant",
    page_icon="🚛",
    layout="centered"
)

# --- HEADER ---
st.title("🚛 FMCSA Regulation Assistant")
st.markdown("Ask questions about **Federal Motor Carrier Safety Administration** regulations.")
st.divider()

# --- INITIALIZATION ---
# We use @st.cache_resource so we only load the DB/LLM once, not every time you type.
@st.cache_resource
def get_assistant():
    return FMCSAAssistant(db_path="./data/chroma_db")

try:
    assistant = get_assistant()
except Exception as e:
    st.error(f"❌ Failed to load system: {e}")
    st.stop()

# --- CHAT HISTORY ---
# Initialize session state to keep track of the conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- USER INPUT ---
if prompt := st.chat_input("Ex: What are the HOS limits for property carriers?"):
    # 1. Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Generate Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Consulting the regulations..."):
            # Call your backend engine
            response = assistant.ask(prompt)
            
            # Format the answer
            answer_text = response["answer"]
            sources_text = "\n\n**📚 Sources:**\n" + "\n".join([f"- {s}" for s in response["sources"]])
            
            full_response = answer_text + sources_text
            st.markdown(full_response)
            
    # 3. Save Assistant Message to History
    st.session_state.messages.append({"role": "assistant", "content": full_response})