<script lang="ts">
	import { WorksAPI } from '$lib/backend/api/works';
	import type { Work } from '$lib/backend/models/works';
	import CircularLoader from '$lib/components/common/CircularLoader.svelte';
	import IconButton from '$lib/components/common/IconButton.svelte';
	import Snackbar from '$lib/components/common/Snackbar.svelte';
	import Button, { Icon } from '@smui/button';
	import { Body, Cell, Head, Row } from '@smui/data-table';
	import LinearProgress from '@smui/linear-progress';
	import { onMount } from 'svelte';
	import PaginatedTable from '../common/PaginatedTable.svelte';
	import Panel from '../common/Panel.svelte';
	import WorkCreateDialog from './WorkCreateDialog.svelte';

	export let token: string;

	let snackbar: Snackbar;

	const worksApi = new WorksAPI(token);

	let works: Work[] = [];
	let worksLoaded = false;

	const limit = 10;
	let last: string | null = null;
	let table: PaginatedTable;

	async function updateWorks(limit: number, last: string | null): Promise<string | null> {
		worksLoaded = false;
		const result = await worksApi.getWorks();
		worksLoaded = true;
		if (result.ok) {
			works = result.value.works;
			return result.value.last;
		} else {
			snackbar.show(result.error.message);
		}
		return null;
	}

	let workDeleting: Record<string, boolean> = {};
	$: {
		works.map((work) => {
			workDeleting[work.work_id] = false;
		});
	}

	async function deleteWork(work_id: string) {
		workDeleting[work_id] = true;
		const result = await worksApi.deleteWork(work_id);
		if (result.ok) {
			await table.reloadPage();
		} else {
			snackbar.show(result.error.message);
		}
		workDeleting[work_id] = false;
	}

	let createDialogOpen = false;

	onMount(async () => {
		await table.firstPage();
	});
</script>

<Panel title="Услуги">
	<div class="table-container">
		<PaginatedTable bind:this={table} {limit} bind:last updateItems={updateWorks}>
			<Head slot="head">
				<Row>
					<Cell>ID</Cell>
					<Cell>Наименование</Cell>
					<Cell />
				</Row>
			</Head>
			<Body slot="body">
				{#each works as work}
					<Row>
						<Cell>{work.work_id}</Cell>
						<Cell style="width: 100%">{work.name}</Cell>
						<Cell>
							{#if workDeleting[work.work_id]}
								<CircularLoader size="small" />
							{:else}
								<IconButton onClick={() => deleteWork(work.work_id)} icon="delete" />
							{/if}
						</Cell>
					</Row>
				{/each}
			</Body>
			<LinearProgress
				indeterminate
				bind:closed={worksLoaded}
				aria-label="Загрузка..."
				slot="progress"
			/>
		</PaginatedTable>
	</div>
	<div class="add-work-container">
		<Button
			variant="outlined"
			on:click={() => {
				createDialogOpen = true;
			}}
		>
			<Icon class="material-icons">add_circle_outlined</Icon>
			Добавить услугу
		</Button>
	</div>
</Panel>

<Snackbar bind:this={snackbar} />

<WorkCreateDialog
	{token}
	bind:open={createDialogOpen}
	onCreate={async () => await table.reloadPage()}
/>
