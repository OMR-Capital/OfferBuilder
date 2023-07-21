<script lang="ts">
	import { WastesAPI } from '$lib/backend/api/wastes';
	import type { Waste } from '$lib/backend/models/wastes';
	import CircularLoader from '$lib/components/common/CircularLoader.svelte';
	import IconButton from '$lib/components/common/IconButton.svelte';
	import Snackbar from '$lib/components/common/Snackbar.svelte';
	import Button, { Icon } from '@smui/button';
	import DataTable, { Body, Cell, Head, Row } from '@smui/data-table';
	import LinearProgress from '@smui/linear-progress';
	import { onMount } from 'svelte';
	import WasteCreateDialog from './WasteCreateDialog.svelte';

	export let token: string;

	let snackbar: Snackbar;

	const wastesApi = new WastesAPI(token);

	let wastes: Waste[] = [];
	let wastesLoaded = false;

	async function updateWastes() {
		wastesLoaded = false;
		const result = await wastesApi.getWastes();
		if (result.ok) {
			wastes = result.value;
		} else {
			snackbar.show(result.error.message);
		}
		wastesLoaded = true;
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
			updateWastes();
		} else {
			snackbar.show(result.error.message);
		}
		wasteDeleting[waste_id] = false;
	}

	let createDialogOpen = false;

	onMount(updateWastes);
</script>

<div>
	<h5>Отходы</h5>
	<div class="table-container">
		<DataTable table$aria-label="Список отходов" style="width: 100%;">
			<Head>
				<Row>
					<Cell>ID</Cell>
					<Cell>Наименование</Cell>
					<Cell>Код ФККО</Cell>
					<Cell />
				</Row>
			</Head>
			<Body>
				{#each wastes as waste}
					<Row>
						<Cell>{waste.waste_id}</Cell>
						<Cell style="width: 100%">{waste.name}</Cell>
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
		</DataTable>
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

	<Snackbar bind:this={snackbar} />

	<WasteCreateDialog {token} bind:open={createDialogOpen} onCreate={updateWastes} />
</div>

<style>
	.table-container {
		padding-top: 2rem;
	}

	.add-waste-container {
		padding-top: 2rem;
	}
</style>
