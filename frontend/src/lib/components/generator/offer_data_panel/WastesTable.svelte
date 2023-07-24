<script lang="ts">
	import { WastesAPI } from '$lib/backend/api/wastes';
	import type { Waste } from '$lib/backend/models/wastes';
	import Snackbar from '$lib/components/common/Snackbar.svelte';
	import Button, { Icon } from '@smui/button';
	import DataTable, { Body, Cell, Head, Row } from '@smui/data-table';
	import LinearProgress from '@smui/linear-progress';
	import { onMount } from 'svelte';
	import AddWasteRowDialog from './AddWasteRowDialog.svelte';
	import type { WasteRow } from './types';

	export let token: string;

	export let wasteRows: WasteRow[] = [];

	const wastesApi = new WastesAPI(token);

	let availableWastes: Waste[] = [];
	let wastesLoaded = false;

	async function updateWastes() {
		wastesLoaded = false;
		const result = await wastesApi.getWastes();
		if (result.ok) {
			availableWastes = result.value;
		} else {
			snackbar.show(result.error.message);
		}
		wastesLoaded = true;
	}

	let addRowDialogOpen = false;

	let snackbar: Snackbar;

	onMount(updateWastes);
</script>

<div class="wastes-table">
	<div class="table-container">
		<DataTable table$aria-label="Данные КП" style="width: 100%;">
			<Head>
				<Row>
					<Cell style="width: 30%">Наименование</Cell>
					<Cell>ФККО</Cell>
					<Cell>Ед. изм.</Cell>
					<Cell numeric>Цена за ед. изм.</Cell>
					<Cell numeric>Кол-во</Cell>
					<Cell numeric>Сумма</Cell>
				</Row>
			</Head>
			<Body>
				{#each wasteRows as wasteRow}
					<Row>
						<Cell>{wasteRow.name}</Cell>
						<Cell>{wasteRow.fkko_code}</Cell>
						<Cell>{wasteRow.unit}</Cell>
						<Cell numeric>{wasteRow.price} руб/{wasteRow.unit}</Cell>
						<Cell numeric>{wasteRow.amount} {wasteRow.unit}</Cell>
						<Cell numeric>{wasteRow.sum} руб</Cell>
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
	<div class="add-btn-container">
		<Button
			variant="outlined"
			on:click={() => {
				addRowDialogOpen = true;
			}}
		>
			<Icon class="material-icons">add_circle_outlined</Icon>
			Добавить элемент
		</Button>
	</div>
</div>

<AddWasteRowDialog
	bind:open={addRowDialogOpen}
	{availableWastes}
	onConfirm={(wasteRow) => {
		wasteRows = [...wasteRows, wasteRow];
	}}
/>

<Snackbar bind:this={snackbar} />

<style>
	.wastes-table {
		display: flex;
		flex-direction: column;
		height: 100%;
		gap: 2rem;
	}

	.table-container {
		flex-grow: 1;
	}
</style>
