from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from my_assistant.memory import search_memory,save_memory,erase_all_memories

def get_current_datetime(timezone: str) -> str:
    """Returns the current date and time for a given timezone."""

    try:
        current_time = datetime.now(ZoneInfo(timezone))

        return current_time.strftime(
            "%A, %B %d, %Y at %I:%M %p"
        )

    except ZoneInfoNotFoundError:
        return (
            f"I couldn't find the timezone '{timezone}'. "
            "Please provide a valid IANA timezone, "
            "such as 'Asia/Kolkata', 'Asia/Tokyo', "
            "or 'America/New_York'."
        )

def calculator(a: float, b: float, operation: str) -> float:
    """This Performs the basic arithmetic operations"""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            return "Cannot divide by zero."
        return a / b
    return "Invalid Operation."

def search_long_term_memory(query: str) -> str:
    """Search the user's long-term memories for information relevant to the query."""

    results = search_memory(query)

    if not results:
        return "No relevant memories found."

    memories = ["Relevant memories:"]

    for i, result in enumerate(results, start=1):
        memories.append(
            f"{i}.\n"
            f"Text: {result.payload['text']}\n"
            f"Type: {result.payload['type']}\n"
            f"Created: {result.payload['created_at']}\n"
            f"Metadata: {result.payload['metadata']}\n"
            f"Similarity: {result.score}"
        )

    return "\n\n".join(memories)

from my_assistant.memory import save_memory


def save_long_term_memory(
    text: str,
    memory_type: str = "general",
    metadata: dict | None = None,
) -> str:
    """Save useful, long-term information about the user to long-term memory."""

    save_memory(
        text=text,
        memory_type=memory_type,
        metadata=metadata,
    )

    return "Memory saved successfully."


def erase_long_term_memory() -> str:
    """Erase all long-term memories. Use only when the user explicitly asks to forget all stored memories."""

    erase_all_memories()

    return "All long-term memories have been erased."