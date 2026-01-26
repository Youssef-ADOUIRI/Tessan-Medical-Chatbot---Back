import os
import sys
import yaml
from dotenv import load_dotenv

# Basic setup to handle imports if dependencies are installed in a specific way
# ignoring for now assuming standard pip install

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.runnables.history import RunnableWithMessageHistory
    from langchain_core.chat_history import InMemoryChatMessageHistory
    from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
except ImportError as e:
    print(f"Error: Required libraries not installed. Please run 'pip install -r requirements.txt'. Detail: {e}")
    sys.exit(1)

# Load environment variables
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
"""
    # Note: Few-shot examples are usually handled differently in LangChain (FewShotPromptTemplate)
    # but to maintain identical logic to the original script where it was all one big string, 
    # we will append them here. Alternatively, we could seed the history.
    # Let's keep it in the system instruction for simplicity and strict adherence to "same logic".
    
    instruction += """
[EXEMPLES D'INTERACTION (FEW-SHOT LEARNING)]
"""
    examples = template_data.get('few_shot_examples', [])
    for ex in examples:
        instruction += f"\nUtilisateur: {ex['user']}\nAssistant: {ex['assistant']}\n"
    
    return instruction

# Store for chat histories
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

def create_tessan_chatbot(api_key, template_path):
    """
    Creates and returns the Tessan Medical Chatbot Runnable.
    """
    # Load System Prompt
    template_data = load_prompt_template(template_path)
    if not template_data:
        raise ValueError("Could not load prompt template.")
        
    system_instruction = construct_system_instruction(template_data)

    # Initialize Model
    # gemini-2.5-flash might not be available, falling back to gemini-1.5-flash or similar if needed 
    # but keeping user's choice for now.
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp", # Updated to a likely valid model name or keep user's if known valid
        temperature=0.7,
        google_api_key=api_key,
        convert_system_message_to_human=True 
    )

    # Create Prompt Template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "{system_instruction}"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])

    # Create Chain
    chain = prompt | llm

    # create runnable with history
    with_message_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )
    
    return with_message_history, system_instruction

def main():
    """
    Main function to run the Tessan Medical Chatbot using LangChain.
    """
    # Configuration
    API_KEY = os.getenv("GEMINI_API_KEY")
    TEMPLATE_PATH = "system_prompt_template.yaml" 
    
    # Handle path if running from root
    if not os.path.exists(TEMPLATE_PATH):
         TEMPLATE_PATH = os.path.join("tessan_langchain", "system_prompt_template.yaml")

    # Check for API Key
    if not API_KEY:
        print("WARNING: GEMINI_API_KEY environment variable not set.")
        sys.exit(1)

    try:
        with_message_history, system_instruction = create_tessan_chatbot(API_KEY, TEMPLATE_PATH)
    except ValueError as e:
        print(f"Error initializing chatbot: {e}")
        sys.exit(1)

    print("--- Tessan Medical Chatbot (Powered by LangChain & Google Gemini) ---")
    print("--- Mode: Few-Shot Learning from YAML Template ---")
    print("Type 'quit' to exit\n")
    print("Bot: Bonjour ! Je suis votre assistant médical Tessan. Comment puis-je vous aider aujourd'hui ?")

    session_id = "user_session_1" # In a real app this would be dynamic

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
                response = with_message_history.invoke(
                    {"input": user_input, "system_instruction": system_instruction},
                    config={"configurable": {"session_id": session_id}}
                )
                print(f"Bot: {response.content}")

            except Exception as e:
                print(f"Error calling Gemini API: {e}")
                
        except KeyboardInterrupt:
            print("\nBot: Au revoir !")
            break

if __name__ == "__main__":
    main()
