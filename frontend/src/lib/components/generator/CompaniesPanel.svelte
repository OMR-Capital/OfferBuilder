<script lang="ts">
	import { CompaniesAPI } from '$lib/backend/api/companies';
	import type { Company } from '$lib/backend/models/companies';
	import Autocomplete from '@smui-extra/autocomplete';
	import { onMount } from 'svelte';
	import CircularLoader from '../common/CircularLoader.svelte';
	import Panel from '../common/Panel.svelte';
	import Snackbar from '../common/Snackbar.svelte';

	export let token: string;

	let snackbar: Snackbar;

	const companiesApi = new CompaniesAPI(token);

	export let selectedCompanyName: string | undefined = undefined;
	let companies: Company[] = [];
	let companiesLoading = false;

	async function updateCompanies() {
		companiesLoading = true;
		const result = await companiesApi.getCompanies();
		if (result.ok) {
			companies = result.value;
		} else {
			snackbar.show(result.error.message);
		}
		companiesLoading = false;
	}

	function getCompanyLabel(company: Company | null) {
		return company ? `${company.name}` : '';
	}

	onMount(updateCompanies);
</script>

<Panel title="Организация">
	{#if companiesLoading}
		<CircularLoader size="large" />
	{:else}
		<Autocomplete
			label="Организация"
			style="width: 100%;"
			textfield$style="width: 100%;"
			combobox
			options={companies}
			getOptionLabel={getCompanyLabel}
			bind:value={selectedCompanyName}
		/>
	{/if}
</Panel>

<Snackbar bind:this={snackbar} />
