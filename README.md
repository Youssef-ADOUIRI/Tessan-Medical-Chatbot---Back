# Tessan Medical Chatbot

A general public medical chatbot assistant defined for Tessan. This bot serves as a first-line information tool, providing general health information, managing medical red flags, and proposing teleconsultations when appropriate.

## Features

- **Medical Assistance**: Answers general health questions (symptoms, meanings, general advice).
- **Safety First**: Detects emergencies (Red Flags) and redirects to emergency services (15/112).
- **Zero Diagnosis**: Strictly refrains from diagnosing or prescribing.
- **Teleconsultation Integration**: Systematically proposes teleconsultation for non-emergency medical queries.
- **Powered by Google Gemini**: Uses the Gemini 2.5 Flash model for high-quality, cost-effective responses.

## Prerequisites

- **Python**: 3.10 or higher
- **Poetry**: For dependency management (Optional)
- **Google Gemini API Key**: [Get one here](https://aistudio.google.com/app/apikey)

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Youssef-ADOUIRI/Tessan-Medical-Chatbot---Back.git
    cd Tessan Medical Chatbot
    ```

2.  **Install Dependencies** (using Poetry):
    ```bash
    poetry install
    ```

3.  **Environment Setup**:
    - Create a `.env` file in the root directory.
    - Add your Google Gemini API Key:
      ```env
      GEMINI_API_KEY=your_actual_api_key_here
      ```

## Usage

Run the chatbot using Poetry:

```bash
poetry run python chatbot.py
```
or
```bash
python chatbot.py
```

The bot will launch in the terminal. Type your health-related questions to interact. Type `quit`, `exit`, or `q` to stop.

## Architecture

- **`chatbot.py`**: Main application script. Handles user input, API communication, and conversation loop.
- **`system_prompt_template.yaml`**: Contains the strict system instructions (Role, Tone, Safety Rules) and Few-Shot examples.
- **`pyproject.toml`**: Dependency configuration.

### System Flow
The architecture relies on a **Secure Orchestrator** that filters each user input via an **Intent Detector** to classify the request (Symptom, Admin, Emergency). If a symptom is identified, the request first passes through a **Medical Security Module** (based on strict rules and "Red Flags" keywords) before querying the LLM. The generated response is then analyzed by the **Suggestion Module**, which conditionally injects the teleconsultation proposal (prompt rule). Finally, a **Monitoring & Logging** system audits interactions in real-time to track response refusals and detect potential hallucinations, ensuring continuous medical compliance.


## System Prompt & Logic

The behavior of the chatbot is governed by a strict system prompt defined in `system_prompt_template.yaml`.

### Role & Tone
- **Role**: Tessan Medical Assistant.
- **Tone**: Professional, reassuring, objective, and French-speaking.

### Critical Safety Rules
1.  **Zero Diagnosis**: Never diagnose specific conditions.
2.  **No Prescriptions**: No medication suggestions.
3.  **Red Flags**: Immediate referral to 15/112 for emergencies.

### Logic for Mandatory Closing Phrase
The phrase *"Souhaitez-vous passer en téléconsultation maintenant ?"* is **STRICTLY CONDITIONAL**:
- **USED ONLY IF**:
    1.  **Risk Detected**: Symptoms require medical attention.
    2.  **Conclusion**: The conversation is naturally ending.
- **FORBIDDEN IF**:
    - Greeting ("Bonjour").
    - Simple clarification questions.

### Examples (Few-Shot)

**Standard Greeting (No Closure)**:
> **User**: Bonjour
> **Assistant**: Bonjour ! Je suis l'assistant médical Tessan. Comment puis-je vous aider aujourd'hui ?

**Medical Risk (With Closure)**:
> **User**: J'ai mal au ventre depuis ce matin.
> **Assistant**: Les douleurs abdominales peuvent avoir de nombreuses causes... Si la douleur persiste... un avis médical est nécessaire.
> **Souhaitez-vous passer en téléconsultation maintenant ?**

**Emergency (Red Flag)**:
> **User**: Je saigne beaucoup ...
> **Assistant**: ATTENTION : C'est une SITUATION D'URGENCE. Appelez le 15 ou 112...
