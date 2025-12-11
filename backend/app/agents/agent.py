"""Task Management Agent using OpenAI Agents SDK with OpenRouter.

Uses OpenAIChatCompletionsModel with OpenRouter's OpenAI-compatible endpoint.
Supports Qwen and other open-source models via OpenRouter for unlimited free access.
"""

from uuid import UUID
from sqlalchemy.orm import Session
from agents import Agent

from app.agents.tools import TASK_TOOLS, TaskContext
from app.agents.openrouter_client import create_openrouter_model


def create_task_agent(user_id: UUID, db_session: Session) -> Agent[TaskContext]:
    """Create a task management agent using OpenRouter with Qwen models.

    Uses OpenAIChatCompletionsModel explicitly configured with OpenRouter API.
    Supports unlimited free requests with Qwen models.

    Args:
        user_id: UUID of the user
        db_session: Database session for task operations

    Returns:
        Agent configured to manage tasks via natural language

    Environment:
        Requires OPENROUTER_API_KEY to be set
        Optional: OPENROUTER_MODEL (default: qwen/qwen-2.5-72b-instruct)
    """

    # Create OpenRouter ChatCompletionsModel with Qwen
    openrouter_model = create_openrouter_model()

    # Create agent with ChatCompletionsModel
    agent = Agent[TaskContext](
        name="Task Manager",
        instructions="""You are a helpful AI assistant for task management.
You help users create, update, delete, and retrieve tasks through natural conversation.

Guidelines:
- Ask for clarification if task details are missing
- Confirm destructive actions (delete)
- Be friendly and conversational
- Explain what you did in simple terms
- Suggest priorities based on urgency (low, medium, high, urgent)

IMPORTANT for update_task tool:
- ALWAYS pass the full user query in the 'full_query' parameter
- This allows the tool to intelligently detect status changes like "mark as done" or "start task"
- This allows the tool to intelligently detect title changes like "rename to X" or "call it Y"
- Examples:
  * User says "mark milk as done" → pass full_query="mark milk as done"
  * User says "rename milk to groceries" → pass full_query="rename milk to groceries"
  * User says "start the project task" → pass full_query="start the project task"
- Always extract the task identifier (task_id) from the user's message""",
        model=openrouter_model,
        tools=TASK_TOOLS,
    )

    return agent
