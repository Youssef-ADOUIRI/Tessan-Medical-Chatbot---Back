import streamlit as st
import os
import time
from dotenv import load_dotenv
from chatbot_langchain import create_tessan_chatbot, get_session_history
from langchain_core.messages import HumanMessage, AIMessage

# Configure Streamlit page
st.set_page_config(
    page_title="Tessan Medical Chatbot",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Custom CSS for Tessan branding
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #1e1f20;
    }
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
    }
    .stChatMessage[data-testid="user-message"] {
        background-color: #e6f7ff;
    }
    .stChatMessage[data-testid="assistant-message"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
    }
    h1 {
        color: #007bff; /* Tessan Blue-ish */
    }
</style>
""", unsafe_allow_html=True)

def initialize_chat():
    """Initializes the chatbot chain and session state."""
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add initial greeting
        st.session_state.messages.append({"role": "assistant", "content": "Bonjour ! Je suis votre assistant médical Tessan. Comment puis-je vous aider aujourd'hui ?"})

    if "session_id" not in st.session_state:
        st.session_state.session_id = f"session_{int(time.time())}"

    if "chatbot" not in st.session_state:
        api_key = os.getenv("GEMINI_API_KEY")
        # Go up one level to find the template if running from tessan_langchain folder, 
        # or check current directory
        template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "system_prompt_template.yaml"))
        if not os.path.exists(template_path):
             template_path = "system_prompt_template.yaml"

        if not api_key:
            st.error("API Key not found! Please check your .env file.")
            return

        try:
            chain, system_instruction = create_tessan_chatbot(api_key, template_path)
            st.session_state.chatbot = chain
            st.session_state.system_instruction = system_instruction
        except Exception as e:
            st.error(f"Failed to initialize chatbot: {e}")

initialize_chat()

# Sidebar
with st.sidebar:
    st.image("https://cdn.prod.website-files.com/66b60a40346a2a32aeadb205/66eaee3ef7106d4749605217_2631f0d5289f460fa1d9f9176078fb6f_Thumbnail%20tessan.webp", width=150) # Placeholder or actual logo URL if public
    st.title("Tessan Chatbot")
    st.markdown("---")
    st.write("Ce prototype utilise **Google Gemini** et **LangChain** pour simuler un assistant médical.")
    
    if st.button("Nouvelle conversation"):
        st.session_state.messages = []
        st.session_state.session_id = f"session_{int(time.time())}"
        st.session_state.messages.append({"role": "assistant", "content": "Bonjour ! Je suis votre assistant médical Tessan. Comment puis-je vous aider aujourd'hui ?"})
        st.session_state.pop("chatbot", None) # Re-init might be overkill but ensures fresh start
        st.rerun()

# Main Chat Interface
st.title("🩺 Assistant Médical Tessan")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Écrivez votre message ici..."):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        if "chatbot" in st.session_state:
            try:
                # Stream the response if possible, or just invoke
                # RunnableWithMessageHistory doesn't always make streaming easy without async, 
                # but let's try standard invoke first for stability as per plan.
                
                # To show a "thinking" spinner
                with st.spinner("Réflexion en cours..."):
                    response = st.session_state.chatbot.invoke(
                        {"input": prompt, "system_instruction": st.session_state.system_instruction},
                        config={"configurable": {"session_id": st.session_state.session_id}}
                    )
                
                full_response = response.content
                message_placeholder.markdown(full_response)
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                st.error(f"Une erreur est survenue: {e}")
        else:
            st.error("Chatbot non initialisé.")
