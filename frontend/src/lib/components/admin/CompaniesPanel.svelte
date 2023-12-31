<script lang="ts">
	import { CompaniesAPI } from '$lib/backend/api/companies';
	import type { Company } from '$lib/backend/models/companies';
	import CompanyCreateDialog from '$lib/components/admin/CompanyCreateDialog.svelte';
	import CircularLoader from '$lib/components/common/CircularLoader.svelte';
	import IconButton from '$lib/components/common/IconButton.svelte';
	import Snackbar from '$lib/components/common/Snackbar.svelte';
	import Button, { Icon } from '@smui/button';
	import { Body, Cell, Head, Row } from '@smui/data-table';
	import LinearProgress from '@smui/linear-progress';
	import { onMount } from 'svelte';
	import PaginatedTable from '../common/PaginatedTable.svelte';
	import Panel from '../common/Panel.svelte';

	export let token: string;

	let snackbar: Snackbar;

	const companiesApi = new CompaniesAPI(token);

	let companies: Company[] = [];
	let companiesLoaded = false;

	let limit = 10;
	let last: string | null = null;
	let table: PaginatedTable;

	async function updateCompanies(limit: number, last: string | null): Promise<string | null> {
		companiesLoaded = false;
		const result = await companiesApi.getCompanies({ limit, last });
		companiesLoaded = true;
		if (result.ok) {
			companies = result.value.companies;
			return result.value.last;
		} else {
			snackbar.show(result.error.message);
		}
		return null;
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
			await table.reloadPage();
		} else {
			snackbar.show(result.error.message);
		}
		companyDeleting[company_id] = false;
	}

	let createDialogOpen = false;

	onMount(async () => {
		await table.firstPage();
	});
</script>

<Panel title="Организации">
	<div class="table-container">
		<PaginatedTable bind:this={table} {limit} bind:last updateItems={updateCompanies}>
			<Head slot="head">
				<Row>
					<Cell>ID</Cell>
					<Cell>Название</Cell>
					<Cell />
				</Row>
			</Head>
			<Body slot="body">
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
		</PaginatedTable>
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
</Panel>

<Snackbar bind:this={snackbar} />

<CompanyCreateDialog
	{token}
	bind:open={createDialogOpen}
	onCreate={async () => await table.reloadPage()}
/>
