<script lang="ts">
	import { CompaniesAPI } from '$lib/backend/api/companies';
	import type { Company } from '$lib/backend/models/companies';
	import { onMount } from 'svelte';
	import CircularLoader from '../common/CircularLoader.svelte';
	import Panel from '../common/Panel.svelte';
	import Snackbar from '../common/Snackbar.svelte';
	import Select, { Option } from '@smui/select';

	export let token: string;

	let snackbar: Snackbar;

	const companiesApi = new CompaniesAPI(token);

	export let selectedCompany: Company = {
		company_id: '',
		name: ''
	};
	let companies: Company[] = [];
	let companiesLoading = false;

	async function updateCompanies() {
		companiesLoading = true;
		const result = await companiesApi.getCompanies();
		if (result.ok) {
			companies = result.value.companies;
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
		<Select label="Организация" bind:value={selectedCompany}>
			{#each companies as company (company.company_id)}
				<Option value={company}>{company.name}</Option>
			{/each}
		</Select>
	{/if}
</Panel>

<Snackbar bind:this={snackbar} />
