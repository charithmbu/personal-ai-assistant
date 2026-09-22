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

- Created a date and time tool using Python's `datetime` and `zoneinfo` modules.
- Added timezone support using IANA timezone names such as `Asia/Kolkata` and `America/New_York`.
- Registered the `get_current_datetime` tool with the ADK agent.
- Added a docstring and type hints to the tool and understood how ADK uses them to generate the tool/function schema.
- Tested the tool with different timezones using ADK Web.
- Added exception handling for invalid timezones using `ZoneInfoNotFoundError`.
- Explored the ADK Web Events tab to understand agent events, tool calls, and tool responses.
- Explored the ADK Web Traces tab to understand invocations, traces, spans, latency, and internal LLM calls.
- Understood that a tool-using request can involve multiple LLM calls: one to decide to call the tool and another to generate the final response using the tool result.
- Explored token usage in ADK Web, including prompt tokens, candidate tokens, thought tokens, and total tokens.
- Examined the model request context and understood how previous conversation history, tool definitions, function calls, and function responses are included in the context sent to the model.
- Learned about context compaction and how it can summarize older conversation history to reduce the amount of context sent to the model.

**### Tool Implemented**

- get_current_datetime(timezone: str) -> str:

### Day 3

- Added a `calculator` function to perform basic arithmetic operations such as addition, subtraction, multiplication, and division.
  ### Calculator Tool Execution Flow

```text
User enters a prompt
        │
        ▼
Example: "What is 25 × 40?"
        │
        ▼
   Root Agent
   (Gemini + ADK)
        │
        ▼
Understands the user's request
        │
        ▼
Identifies that a calculation
is required
        │
        ▼
Selects the `calculator` tool
        │
        ▼
ADK sends the required arguments
        │
        ▼
calculator(
    a = 25,
    b = 40,
    operation = "multiply"
)
        │
        ▼
Python executes the calculator function
        │
        ▼
      25 × 40
        │
        ▼
      Result = 1000
        │
        ▼
ADK sends the tool result
back to the Root Agent
        │
        ▼
Gemini generates the final response
        │
        ▼
User receives:
"The answer is 1000."
```

### Calculator Tool Flow

1. User enters a calculation prompt.
2. The Root Agent receives and understands the request.
3. The agent identifies that a calculation is required.
4. The agent selects the **Calculator Tool**.
5. ADK passes the required values and operation to the Python function.
6. The calculator function performs the requested operation.
7. The calculated result is returned to the agent.
8. The agent generates the final response and sends it to the user.

- Integrated the calculator function directly into `agent.py` as an ADK tool.
- Updated the date/time tool file name from `tools.py` to `dateTime.py`.
- Configured the root agent to use the calculator tool when the user requests calculations.

### Day 4

Built a persistent long-term memory system built with **Gemini Embeddings + Qdrant**.
It automatically stores useful information about the user, retrieves relevant memories when needed, and supports clearing all stored memories.

### Architecture

```text
                         User
                           │
                           ▼
                     Gemini Agent
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
           SAVE          SEARCH       ERASE ALL
             │             │              │
             ▼             ▼              ▼
       Gemini Embedding  Gemini Embedding │
             │             │              │
             └──────┬──────┘              │
                    ▼                     ▼
                  Qdrant              Qdrant
                    │
                    ▼
             Relevant Memories
                    │
                    ▼
              Gemini Agent
                    │
                    ▼
                  Answer
```

### Steps

- changed llm model to `gemini-3.5-flash-lite` because it provides high request limits.
- merged Calculator.py and dateTime.py into tools.py for better organization.
- updated personal_ai_assistant/.gitignore
- installed docker desktop
- pull "qdrant/qdrant" image using

```bash
docker pull qdrant/qdrant:latest
```

- create a container

```bash
docker run -d \
  --name qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  qdrant/qdrant:latest
```

- in dashboard click containers,you will find "qdrant/qdrant".click run
- now we can connect to qdrant which is a vector database using our backend logic placed in "memory.py"
- we configured qdrant to store 768 length vectors and used `cosine similarity` as our similarity metric
- we use qdrant_client for communicating with database and gemini_client for llm communication
- create_embedding() method takes text,connect with embedding model `gemini-embedding-2` and returns vector
- save_memory() method uses create_embedding() and saves the resulting vector along with id,payload into database
- every record in database is called point
- point structure
  ```text
  Point
  ├── ID              ← generated automatically
  ├── Vector          ← Gemini embedding
  └── Payload
    ├── text        ← required
    ├── type        ← required
    ├── created_at  ← generated by Python
    └── metadata    ← optional/flexible
  ```
- in payload metadata is optional.llm decides which fields to put in metadata based on user request context.
- search_memory() uses create_embedding() and create a vector for the query string,connects to database,and return top 10 similar semantic points.
- llm decides which point to use and answer the user query.
- erase_all_memories() function is use to delete the database and recreate it again.so previous memories are removed.
- But we dont add these functions directly as tools.we use wrapper functions in `tools.py` as tools
- llm doesnt want to deal with python objects.our tools need to return understandable outputs.this is the reason wrapup methods in `tools.py` are needed
- created `search_long_term_memory()`,`save_long_term_memory()`,`erase_long_term_memory()` in `tools.py`
- updated `agent.py` with required instruction prompt and included the above tools.
