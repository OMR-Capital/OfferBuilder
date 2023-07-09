"""Agents utilities.

Agents are target companies in offers.

This module provide methods for getting agents data from API by inn code
See https://dadata.ru/api/find-party/
"""

from http import HTTPStatus
from typing import Any, Optional

import requests

from app.core.config import AGENTS_API_KEY
from app.models.agent import Agent

API_URL_BASE = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs'

# Json parsing requires lot of variables
# flake8: noqa: WPS210
def get_agent_from_api_data(agent_data: dict[str, Any]) -> Optional[Agent]:
    """Get agent data from API response.

    Args:
        agent_data (dict[str, Any]): Agent data from API response

    Returns:
        Optional[Agent]: Agent data
    """
    name = agent_data.get('name')
    fullname = name.get('full') if name else None
    shortname = name.get('short_with_opf') if name else None
    inn = agent_data.get('inn')
    management_data = agent_data.get('management')
    management = management_data.get('name') if management_data else None

    if not (fullname and shortname and inn):
        return None

    return Agent(
        fullname=fullname,
        shortname=shortname,
        inn=inn,
        management=management,
    )


def get_agent(inn: str) -> Optional[Agent]:
    """Get agent data from API by inn code.

    See https://dadata.ru/api/find-party/ for API details.

    Args:
        inn (str): INN code of agent

    Returns:
        Optional[Agent]: Agent data or None if agent not found
    """
    url = '{url_base}/findById/party'.format(url_base=API_URL_BASE)
    headers = {
        'Authorization': 'Token {api_key}'.format(api_key=AGENTS_API_KEY),
    }
    json = {'query': inn}
    agent_data_response = requests.post(
        url,
        headers=headers,
        json=json,
        timeout=5,
    )
    if agent_data_response.status_code != HTTPStatus.OK:
        return None

    response_json = agent_data_response.json()

    agents = response_json.get('suggestions')
    if not agents:
        return None

    agent_data = agents[0]['data']
    return get_agent_from_api_data(agent_data)
