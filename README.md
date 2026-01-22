# Tessan Medical Chatbot

A general public medical chatbot assistant defined for Tessan. This bot serves as a first-line information tool, providing general health information, managing medical red flags, and proposing teleconsultations when appropriate.

## Features

- **Medical Assistance**: Answers general health questions (symptoms, meanings, general advice).
- **Safety First**: Detects emergencies (Red Flags) and redirects to emergency services (15/112).
- **Zero Diagnosis**: Strictly refrains from diagnosing or prescribing.
- **Teleconsultation Integration**: Systematically proposes teleconsultation for non-emergency medical queries.
- **Powered by Google Gemini**: Uses the Gemini 1.5 Flash model for high-quality, cost-effective responses.

## Prerequisites

- **Python**: 3.10 or higher
- **Poetry**: For dependency management
- **Google Gemini API Key**: [Get one here](https://aistudio.google.com/app/apikey)

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd Tessan Medical Chatbot
    ```

2.  **Install Dependencies** (using Poetry):
    ```bash
    poetry install
    ```

3.  **Environment Setup**:
    - Create a `.env` file in the root directory (copy the template below or usage `.env` created by the setup).
    - Add your Google Gemini API Key:
      ```env
      GEMINI_API_KEY=your_actual_api_key_here
      ```

## Usage

Run the chatbot using Poetry:

```bash
poetry run python chatbot.py
```

The bot will launch in the terminal. Type your health-related questions to interact. Type `quit`, `exit`, or `q` to stop.

## Architecture

- **`chatbot.py`**: Main application script. Handles user input, API communication, and conversation loop.
- **`chatbot_system_prompt.txt`**: Contains the strict system instructions (Role, Tone, Safety Rules). (Located in artifacts folder or project root depending on your setup).
- **`pyproject.toml`**: Dependency configuration.

## Development

To add new dependencies:
```bash
poetry add <package_name>
```

## License

[Add License Here]
