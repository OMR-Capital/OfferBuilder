"""Agents API."""

from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends

from app.api.dependencies import get_agent_service, get_current_user
from app.api.exceptions.agents import AgentNotFound
from app.api.schemes.agents import AgentResponse
from app.core.agents import (
    AgentNotFoundError,
    AgentsService,
    BadAgentDataError,
)
from app.models.user import User

router = APIRouter(prefix='/agents', tags=['agents'])


@router.get('/{inn}')
async def get_agents(
    inn: str,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[AgentsService, Depends(get_agent_service)],
) -> AgentResponse:
    """Get agent by INN.

    Args:
        inn (str): Agent INN.
        user (User): Authorized user model.
        service (AgentsService): Agents service.

    Raises:
        AgentNotFound: If agent with given INN does not exist.

    Returns:
        AgentResponse: Agent response scheme.
    """
    try:
        agent = service.get_agent(inn)
    except (AgentNotFoundError, BadAgentDataError):
        raise AgentNotFound()

    return AgentResponse(agent=agent)
