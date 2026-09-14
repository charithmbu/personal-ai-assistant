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
