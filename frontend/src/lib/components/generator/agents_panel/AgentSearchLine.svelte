<script lang="ts">
	import { AgentsAPI } from '$lib/backend/api/agents';
	import { normalizeINN, type Agent } from '$lib/backend/models/agents';
	import Autocomplete from '@smui-extra/autocomplete';
	import { Text } from '@smui/list';
	import CircularLoader from '$lib/components/common/CircularLoader.svelte';

	export let token: string;
	export let selectedAgent: Agent | null = null;

	const agentsApi = new AgentsAPI(token);

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
</script>

<Autocomplete
	label="ИНН"
	style="width: 100%;"
	textfield$style="width: 100%;"
	search={searchAgent}
	getOptionLabel={getAgentLabel}
	bind:value={selectedAgent}
>
	<Text
		slot="loading"
		style="display: flex; width: 100%; justify-content: flex-start; align-items: center;"
	>
		<CircularLoader size="small" />
	</Text>
	<Text slot="error">ИНН должен содержать 10 или 12 цифр</Text>
	<Text slot="no-matches">Ничего не найдено</Text>
</Autocomplete>
