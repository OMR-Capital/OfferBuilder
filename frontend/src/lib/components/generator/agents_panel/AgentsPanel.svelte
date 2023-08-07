<script lang="ts">
	import { AgentsAPI } from '$lib/backend/api/agents';
	import { normalizeINN, type Agent } from '$lib/backend/models/agents';
	import Panel from '$lib/components/common/Panel.svelte';
	import { Label } from '@smui/common';
	import Textfield from '@smui/textfield';
	import AgentSearchLine from './AgentSearchLine.svelte';

	export let token: string;
	export let agent: Agent = { inn: '', fullname: '', shortname: '', management: '' };

	const agentsApi = new AgentsAPI(token);

	let foundAgent: Agent | null = null;
	$: updateAgent(foundAgent);

	let searchCounter = 0;

	async function searchAgent(inn: string): Promise<Agent[] | false> {
		const normalizedInn = normalizeINN(inn);
		if (!normalizedInn) {
			throw new Error('Invalid INN');
		}

		const myCounter = ++searchCounter;
		if (myCounter !== searchCounter) {
			return false;
		}

		const result = await agentsApi.getAgent(normalizedInn);
		if (result.ok) {
			return [result.value];
		}
		return [];
	}

	function getAgentLabel(agent: Agent | null) {
		return agent ? agent.fullname : '';
	}

	function updateAgent(newAgent: Agent | null) {
		console.log('updateAgent', newAgent);
		if (newAgent) {
			agent = newAgent;
		}
	}
</script>

<Panel title="Контр-агент">
	<div class="agent-panel">
		<div class="agent-search-container">
			<div class="block-title">
				<Label>Найдите по ИНН</Label>
			</div>
			<AgentSearchLine bind:selectedAgent={foundAgent} {token} />
		</div>
		<div class="agent-input-container">
			<div class="block-title">
				<Label>Или введите вручную</Label>
			</div>
			<div class="agent-fields-container">
				<div class="fields-row">
					<Textfield style="width: 100%;" label="ИНН" bind:value={agent.inn} />
					<Textfield style="width: 100%;" label="Название" bind:value={agent.fullname} />
				</div>
				<div class="fields-row">
					<Textfield style="width: 100%;" label="Руководитель" bind:value={agent.management} />
				</div>
			</div>
		</div>
	</div>
</Panel>

<style>
	.agent-panel {
		display: flex;
		flex-direction: column;
		gap: 2rem;
	}

	.block-title {
		margin-bottom: 0.5rem;
	}

	.agent-search-container {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.agent-input-container {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.agent-fields-container {
		display: flex;
		flex-direction: column;
		gap: 2rem;
	}

	.fields-row {
		display: flex;
		flex-direction: row;
		gap: 4rem;
	}
</style>
