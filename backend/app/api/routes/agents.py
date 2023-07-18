"""Agents API."""

from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends

from app.api.dependencies import get_current_user
from app.api.exceptions.agents import AgentNotFound
from app.api.schemes.agents import AgentResponse
from app.core.agents import get_agent
from app.models.user import User

router = APIRouter(prefix='/agents', tags=['agents'])


@router.get('/{inn}')
async def get_agents(
    inn: str,
    user: Annotated[User, Depends(get_current_user)],
) -> AgentResponse:
    """Get agent by INN.

    Args:
        inn (str): Agent INN.
        user (User): Authorized user model.

    Raises:
        AgentNotFound: If agent with given INN does not exist.

    Returns:
        AgentResponse: Agent response scheme.
    """
    agent = get_agent(inn)
    if not agent:
        raise AgentNotFound()

    return AgentResponse(agent=agent)
