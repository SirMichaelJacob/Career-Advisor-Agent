# Multi-Agent Career Advisor System using Google Agent Development Kit (ADK)

This project implements a **multi-agent AI pipeline** for providing personalized career advice and certification recommendations based on a user's CV (résumé).

Built with **Google's Agent Development Kit (ADK)** – an open-source Python framework for creating sophisticated, modular AI agents – this system demonstrates efficient orchestration of specialized agents using sequential and parallel workflows.

## Overview

The system processes a user's CV text as input and produces actionable career guidance through a series of specialized agents:

1. **CV Analyzer Agent**  
   Extracts key skills, experience, education, and qualifications from the provided CV text.

2. **Parallel Advisor Agents** (run concurrently for efficiency):  
   - **Career Advisor Agent** – Provides tailored career path suggestions, job market insights, and skill development recommendations.  
   - **Certification Advisor Agent** – Recommends up to 5 relevant certifications with explanations and estimated completion times.

3. **Summary Agent**  
   Combines the outputs into a clear, concise, and actionable final summary.

The advisors use a **web research tool** (powered by Google Search) to fetch up-to-date job market trends, salary data, or certification details when needed.

## Architecture

```
User Input (CV text)
       ↓
CV Analyzer Agent → saves "cv_analysis"
       ↓
ParallelAgent
   ├── Career Advisor Agent → uses web research → saves "career_advice"
   └── Certification Advisor Agent → uses web research → saves "certification_suggestions"
       ↓
Summary Agent → produces "final_summary"
       ↓
Final Response to User
```

- **SequentialAgent**: Controls the overall pipeline order.
- **ParallelAgent**: Runs career and certification advice simultaneously to reduce latency.
- **Shared State**: Outputs from earlier agents are automatically available to later ones via session state keys.

## Key Features

- Modular and extensible design – easy to add new specialist agents.
- Real-time web research capability via Google Search.
- Model flexibility using **LiteLLM** (supports Gemini, OpenAI, Anthropic, etc.).
- Local testing with ADK's built-in CLI and web UI.

## Prerequisites

- Python 3.10 or higher
- A Gemini API key (from [Google AI Studio](https://aistudio.google.com/app/apikey)) or any supported LLM provider key
- Install ADK:  
  ```bash
  pip install google-adk
  ```

## Setup

1. Create a project folder, e.g., `career_advisor_agent`.

2. Inside it, create a subfolder (e.g., `career_advisor`) containing:
   - `agent.py` (the provided code)
   - `__init__.py` with:  
     ```python
     from .agent import root_agent
     __all__ = ["root_agent"]
     ```

3. Create a `.env` file in the project root:
   ```
   API_KEY=your_gemini_or_other_api_key_here
   MODEL_NAME=gemini-1.5-flash    # Optional: default model
   BASE_URL=                      # Optional: for custom endpoints (e.g., LiteLLM proxy)
   ```

## Running the Agent

From the parent directory (one level above the agent folder):

- **Interactive Web UI** (recommended):
  ```bash
  adk web
  ```
  Open the browser URL shown → Select your agent → Paste the CV text and chat.

- **Command Line**:
  ```bash
  adk run career_advisor
  ```
  Then type your message (e.g., the full CV text).

**Example User Prompt**:
```
Here is my CV:

[Full CV text here]

Please analyze it and give me career advice.
```

The agent will respond with a professional summary including career recommendations and certification suggestions.

## Customization Ideas

- Add more tools (e.g., job search APIs).
- Use a stronger model for the summary agent (e.g., `gemini-1.5-pro`).
- Deploy to Vertex AI Agent Engine for production scaling.
- Extend with memory for multi-turn conversations about the same CV.

## Why This Design Works Well

- **Efficiency**: Parallel processing speeds up independent research tasks.
- **Accuracy**: Specialists focus on narrow domains, reducing hallucinations.
- **Maintainability**: Each agent is isolated and reusable.
- **Real-World Data**: Integrated web search keeps advice current.

Enjoy building smarter career guidance tools with ADK! If you enhance it (e.g., add salary estimation or interview prep agents), feel free to share. 🚀