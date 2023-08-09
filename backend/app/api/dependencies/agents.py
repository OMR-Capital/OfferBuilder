"""Agents dependencies."""

from app.core.agents import AgentsService


def get_agent_service() -> AgentsService:
    """Get agents service.

    Returns:
        AgentsService: Agents service.
    """
    return AgentsService()
