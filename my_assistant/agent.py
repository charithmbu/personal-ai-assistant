from google.adk.agents.llm_agent import Agent
from .tools import get_current_datetime
root_agent = Agent(
    model='gemini-3.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction="""
    You are a helpful personal assistant.
    
     When the user asks for the current date or time,
    use the get_current_datetime tool.
    """,
    tools=[get_current_datetime],
)
