import { BaseAPI } from '../base_api';
import type { Agent } from '../models/agents';
import type { Result } from '../utils';

interface AgentResponse {
	agent: Agent;
}

export class AgentsAPI extends BaseAPI {
	async getAgent(inn: string): Promise<Result<Agent>> {
		const result = (await this.fetchApi(`/agents/${inn}`, 'GET')) as Result<AgentResponse>;
		if (result.ok) {
			return { ok: true, value: result.value.agent };
		}
		return result;
	}
}
