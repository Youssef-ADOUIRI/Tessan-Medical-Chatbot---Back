
import os
import sys

# Try to import google-generativeai, handle if not installed
try:
    import google.generativeai as genai
    from dotenv import load_dotenv
except ImportError:
    print("Error: Required libraries not installed. Please run 'poetry install'")
    sys.exit(1)

# Load environment variables from .env file
load_dotenv()

def load_system_prompt(filepath):
    """Loads the system prompt from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: System prompt file not found at {filepath}")
        return None

def main():
    """
    Main function to run the Tessan Medical Chatbot using Google Gemini API.
    """
    # Configuration
    API_KEY = os.getenv("GEMINI_API_KEY")
    SYSTEM_PROMPT_PATH = r"C:\Users\YOUSSEF\.gemini\antigravity\brain\8539b388-c816-48ea-8a5c-3742725767c0\chatbot_system_prompt.txt"

    # Check for API Key
    if not API_KEY:
        print("WARNING: GEMINI_API_KEY environment variable not set.")
        print("The chatbot cannot function without an API key.")
        print("Please set it in the .env file or via environment variables.")
        # For demonstration purposes, we might want to continue or exit.
        # Here we exit to be safe as this is a "production-ready" draft.
        sys.exit(1)

    # Configure Gemini
    genai.configure(api_key=API_KEY)

    # Load System Prompt
    system_prompt_content = load_system_prompt(SYSTEM_PROMPT_PATH)
    if not system_prompt_content:
        sys.exit(1)

    # Initialize Model
    # 'gemini-1.5-flash' is a good balance of speed and cost/free tier availability
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_prompt_content
    )

    # Start Chat Session
    chat = model.start_chat(history=[])

    print("--- Tessan Medical Chatbot (Powered by Google Gemini) ---")
    print("Type 'quit' to exit")
    print("Bot: Bonjour ! Je suis votre assistant médical Tessan. Comment puis-je vous aider aujourd'hui ?")

    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Bot: Au revoir et prenez soin de vous !")
                break

            if not user_input.strip():
                continue

            # Call LLM
            try:
                response = chat.send_message(user_input)
                bot_response = response.text
                print(f"Bot: {bot_response}")

            except Exception as e:
                print(f"Error calling Gemini API: {e}")
                
        except KeyboardInterrupt:
            print("\nBot: Au revoir !")
            break

if __name__ == "__main__":
    main()
