<script lang="ts">
	import { CompaniesAPI } from '$lib/backend/api/companies';
	import type { Company } from '$lib/backend/models/companies';
	import CircularLoader from '$lib/components/CircularLoader.svelte';
	import IconButton from '$lib/components/IconButton.svelte';
	import Snackbar from '$lib/components/Snackbar.svelte';
	import Button, { Icon } from '@smui/button';
	import DataTable, { Body, Cell, Head, Row } from '@smui/data-table';
	import LinearProgress from '@smui/linear-progress';
	import { onMount } from 'svelte';
	import CompanyCreateDialog from '$lib/components/admin/CompanyCreateDialog.svelte';

	export let token: string;

	let snackbar: Snackbar;

	const companiesApi = new CompaniesAPI(token);

	let companies: Company[] = [];
	let companiesLoaded = false;

	async function updateCompanies() {
		companiesLoaded = false;
		const result = await companiesApi.getCompanies();
		if (result.ok) {
			companies = result.value;
		} else {
			snackbar.show(result.error.message);
		}
		companiesLoaded = true;
	}

	let companyDeleting: Record<string, boolean> = {};
	$: {
		companies.map((company) => {
			companyDeleting[company.company_id] = false;
		});
	}

	async function deleteCompany(company_id: string) {
		companyDeleting[company_id] = true;
		const result = await companiesApi.deleteCompany(company_id);
		if (result.ok) {
			updateCompanies();
		} else {
			snackbar.show(result.error.message);
		}
		companyDeleting[company_id] = false;
	}

	let createDialogOpen = false;

	onMount(updateCompanies);
</script>

<div>
	<h5>Организации</h5>
	<div class="table-container">
		<DataTable table$aria-label="Список организаций" style="width: 100%;">
			<Head>
				<Row>
					<Cell>ID</Cell>
					<Cell>Название</Cell>
					<Cell />
				</Row>
			</Head>
			<Body>
				{#each companies as company}
					<Row>
						<Cell>{company.company_id}</Cell>
						<Cell style="width: 100%">{company.name}</Cell>
						<Cell>
							{#if companyDeleting[company.company_id]}
								<CircularLoader size="small" />
							{:else}
								<IconButton onClick={() => deleteCompany(company.company_id)} icon="delete" />
							{/if}
						</Cell>
					</Row>
				{/each}
			</Body>
			<LinearProgress
				indeterminate
				bind:closed={companiesLoaded}
				aria-label="Загрузка..."
				slot="progress"
			/>
		</DataTable>
	</div>
	<div class="add-company-container">
		<Button
			variant="outlined"
			on:click={() => {
				createDialogOpen = true;
			}}
		>
			<Icon class="material-icons">add_circle_outlined</Icon>
			Добавить организацию
		</Button>
	</div>

	<Snackbar bind:this={snackbar} />

	<CompanyCreateDialog {token} bind:open={createDialogOpen} onCreate={updateCompanies} />
</div>

<style>
	.table-container {
		padding-top: 2rem;
	}

	.add-company-container {
		padding-top: 2rem;
	}
</style>
