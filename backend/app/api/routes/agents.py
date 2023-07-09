"""Agents API."""

from fastapi import APIRouter

from app.api.exceptions.agents import AgentNotFound
from app.api.schemes.agents import AgentResponse
from app.core.agents import get_agent

router = APIRouter(prefix='/agents', tags=['agents'])


@router.get('/{inn}')
async def get_agents(inn: str) -> AgentResponse:
    """Get agent by INN.

    Args:
        inn (str): Agent INN.

    Raises:
        AgentNotFound: If agent with given INN does not exist.

    Returns:
        AgentResponse: Agent response scheme.
    """
    agent = get_agent(inn)
    if not agent:
        raise AgentNotFound()

    return AgentResponse(agent=agent)
