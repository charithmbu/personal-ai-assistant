# Personal AI Assistant

## Day 1

### What I Did

- Created the `personal-ai-assistant` project directory.
- Created and activated a Python virtual environment.
- Installed Google ADK and FastAPI.
- Created the first ADK agent: `my_assistant`.
- Accessed and tested the agent using `adk web`.
- Created `.env.example` without exposing secrets.
- Configured `.gitignore` to exclude `.env`, `.adk`, `__pycache__`, and `venv`.
- Prepared the project for GitHub.

### Commands Used

```bash
# Create project
mkdir personal-ai-assistant
cd personal-ai-assistant

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install google-adk
pip install fastapi

# Create ADK agent
adk create my_assistant

# Run ADK web interface
adk web

# Check Git status
git status

# Remove already-tracked files from Git
git rm --cached my_assistant/.env
git rm --cached -r my_assistant/.adk
git rm --cached -r my_assistant/__pycache__

# Stage changes
git add .
```

**## Day 2**

**### What I Did**

\- Created a date and time tool using Python's `datetime` and `zoneinfo` modules.
\- Added timezone support using IANA timezone names such as `Asia/Kolkata` and `America/New_York`.
\- Registered the `get_current_datetime` tool with the ADK agent.
\- Added a docstring and type hints to the tool and understood how ADK uses them to generate the tool/function schema.
\- Tested the tool with different timezones using ADK Web.
\- Added exception handling for invalid timezones using `ZoneInfoNotFoundError`.
\- Explored the ADK Web Events tab to understand agent events, tool calls, and tool responses.
\- Explored the ADK Web Traces tab to understand invocations, traces, spans, latency, and internal LLM calls.
\- Understood that a tool-using request can involve multiple LLM calls: one to decide to call the tool and another to generate the final response using the tool result.
\- Explored token usage in ADK Web, including prompt tokens, candidate tokens, thought tokens, and total tokens.
\- Examined the model request context and understood how previous conversation history, tool definitions, function calls, and function responses are included in the context sent to the model.
\- Learned about context compaction and how it can summarize older conversation history to reduce the amount of context sent to the model.

**### Tool Implemented**

\- get_current_datetime(timezone: str) -> str:
