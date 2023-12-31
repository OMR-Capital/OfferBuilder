<script lang="ts">
	import { WastesAPI } from '$lib/backend/api/wastes';
	import type { Waste } from '$lib/backend/models/wastes';
	import CircularLoader from '$lib/components/common/CircularLoader.svelte';
	import IconButton from '$lib/components/common/IconButton.svelte';
	import PaginatedTable from '$lib/components/common/PaginatedTable.svelte';
	import Snackbar from '$lib/components/common/Snackbar.svelte';
	import Button, { Icon } from '@smui/button';
	import { Body, Cell, Head, Row } from '@smui/data-table';
	import LinearProgress from '@smui/linear-progress';
	import { onMount } from 'svelte';
	import Panel from '../common/Panel.svelte';
	import WasteCreateDialog from './WasteCreateDialog.svelte';

	export let token: string;

	let snackbar: Snackbar;

	const wastesApi = new WastesAPI(token);

	let wastes: Waste[] = [];
	let wastesLoaded = false;

	const limit = 10;
	let last: string | null = null;
	let table: PaginatedTable;

	async function updateWastes(limit: number, last: string | null): Promise<string | null> {
		wastesLoaded = false;
		const result = await wastesApi.getWastes({ limit, last });
		wastesLoaded = true;
		if (result.ok) {
			wastes = result.value.wastes;
			return result.value.last;
		} else {
			snackbar.show(result.error.message);
		}
		return null;
	}

	let wasteDeleting: Record<string, boolean> = {};
	$: {
		wastes.map((waste) => {
			wasteDeleting[waste.waste_id] = false;
		});
	}

	async function deleteWaste(waste_id: string) {
		wasteDeleting[waste_id] = true;
		const result = await wastesApi.deleteWaste(waste_id);
		if (result.ok) {
			await table.reloadPage();
		} else {
			snackbar.show(result.error.message);
		}
		wasteDeleting[waste_id] = false;
	}

	let createDialogOpen = false;

	onMount(async () => {
		await table.firstPage();
	});
</script>

<Panel title="Отходы">
	<div class="table-container">
		<PaginatedTable bind:this={table} {limit} bind:last updateItems={updateWastes}>
			<Head slot="head">
				<Row>
					<Cell>ID</Cell>
					<Cell>Наименование</Cell>
					<Cell>Код ФККО</Cell>
					<Cell />
				</Row>
			</Head>
			<Body slot="body">
				{#each wastes as waste}
					<Row>
						<Cell>{waste.waste_id}</Cell>
						<Cell style="width: 100%;">{waste.name}</Cell>
						<Cell>{waste.fkko_code}</Cell>
						<Cell>
							{#if wasteDeleting[waste.waste_id]}
								<CircularLoader size="small" />
							{:else}
								<IconButton onClick={() => deleteWaste(waste.waste_id)} icon="delete" />
							{/if}
						</Cell>
					</Row>
				{/each}
			</Body>
			<LinearProgress
				indeterminate
				bind:closed={wastesLoaded}
				aria-label="Загрузка..."
				slot="progress"
			/>
		</PaginatedTable>
	</div>
	<div class="add-waste-container">
		<Button
			variant="outlined"
			on:click={() => {
				createDialogOpen = true;
			}}
		>
			<Icon class="material-icons">add_circle_outlined</Icon>
			Добавить отход
		</Button>
	</div>
</Panel>

<Snackbar bind:this={snackbar} />

<WasteCreateDialog
	{token}
	bind:open={createDialogOpen}
	onCreate={async () => await table.reloadPage()}
/>
