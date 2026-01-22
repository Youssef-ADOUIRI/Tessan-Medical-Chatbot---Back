
import os
import sys
import yaml

# Try to import google-genai, handle if not installed
try:
    from google import genai
    from dotenv import load_dotenv
except ImportError:
    print("Error: Required libraries not installed. Please run 'poetry install'")
    sys.exit(1)

# Load environment variables from .env file
load_dotenv()

def load_prompt_template(filepath):
    """Loads the system prompt template from a YAML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data
    except FileNotFoundError:
        print(f"Error: Prompt template file not found at {filepath}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None

def construct_system_instruction(template_data):
    """Constructs the full system prompt string from the YAML data."""
    if not template_data:
        return ""

    instruction = f"""[RÔLE]
{template_data.get('role', '')}

[TON SOUHAITÉ]
{template_data.get('tone', '')}

[RÈGLES DE SÉCURITÉ]
{template_data.get('safety_rules', '')}

[PHRASE DE CLÔTURE OBLIGATOIRE]
{template_data.get('mandatory_closing', '')}

[EXEMPLES D'INTERACTION (FEW-SHOT LEARNING)]
"""
    
    examples = template_data.get('few_shot_examples', [])
    for ex in examples:
        instruction += f"\nUtilisateur: {ex['user']}\nAssistant: {ex['assistant']}\n"
    
    return instruction

def main():
    """
    Main function to run the Tessan Medical Chatbot using Google GenAI SDK.
    """
    # Configuration
    API_KEY = os.getenv("GEMINI_API_KEY")
    TEMPLATE_PATH = r"C:\Users\YOUSSEF\Documents\GitHub\Tessan Medical Chatbot\system_prompt_template.yaml"

    # Check for API Key
    if not API_KEY:
        print("WARNING: GEMINI_API_KEY environment variable not set.")
        print("The chatbot cannot function without an API key.")
        print("Please set it in the .env file or via environment variables.")
        sys.exit(1)

    # Configure Gemini Client
    client = genai.Client(api_key=API_KEY)

    # Load and Construct System Prompt
    template_data = load_prompt_template(TEMPLATE_PATH)
    if not template_data:
        sys.exit(1)
        
    system_instruction = construct_system_instruction(template_data)

    # Initialize Chat Session
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=genai.types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7,
        )
    )

    print("--- Tessan Medical Chatbot (Powered by Google Gemini GenAI SDK) ---")
    print("--- Mode: Few-Shot Learning from YAML Template ---")
    print("Type 'quit' to exit\n")
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
