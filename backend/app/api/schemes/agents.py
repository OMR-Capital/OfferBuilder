"""Schemes of agents API."""


from pydantic import BaseModel

from app.models.agent import Agent


class AgentResponse(BaseModel):
    """Agent response scheme."""

    agent: Agent
