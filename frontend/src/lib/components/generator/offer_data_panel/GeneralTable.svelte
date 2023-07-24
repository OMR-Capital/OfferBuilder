<script lang="ts">
	import { WastesAPI } from '$lib/backend/api/wastes';
	import { WorksAPI } from '$lib/backend/api/works';
	import type { Waste } from '$lib/backend/models/wastes';
	import type { Work } from '$lib/backend/models/works';
	import Snackbar from '$lib/components/common/Snackbar.svelte';
	import Button, { Icon } from '@smui/button';
	import DataTable, { Body, Cell, Head, Row } from '@smui/data-table';
	import LinearProgress from '@smui/linear-progress';
	import { onMount } from 'svelte';
	import AddWasteRowDialog from './AddWasteRowDialog.svelte';
	import type { GeneralRow, WasteRow } from '../types';
	import AddGeneralRowDialog from './AddGeneralRowDialog.svelte';

	export let token: string;

	export let generalRows: GeneralRow[] = [];

	const wastesApi = new WastesAPI(token);
	const worksApi = new WorksAPI(token);

	let availableWastes: Waste[] = [];
	let availableWorks: Work[] = [];

	let dataLoaded = false;

	async function updateWastes() {
		const result = await wastesApi.getWastes();
		if (result.ok) {
			availableWastes = result.value;
		} else {
			snackbar.show(result.error.message);
		}
	}

	async function updateWorks() {
		const result = await worksApi.getWorks();
		if (result.ok) {
			availableWorks = result.value;
		} else {
			snackbar.show(result.error.message);
		}
	}

	let addRowDialogOpen = false;

	let snackbar: Snackbar;

	onMount(async () => {
		dataLoaded = false;
		await Promise.all([updateWastes(), updateWorks()]);
		dataLoaded = true;
	});
</script>

<div class="wastes-table">
	<div class="table-container">
		<DataTable table$aria-label="Данные КП" style="width: 100%;">
			<Head>
				<Row>
					<Cell style="width: 30%">Наименование</Cell>
					<Cell>Ед. изм.</Cell>
					<Cell numeric>Цена за ед. изм.</Cell>
					<Cell numeric>Кол-во</Cell>
					<Cell numeric>Сумма</Cell>
				</Row>
			</Head>
			<Body>
				{#each generalRows as generalRow}
					<Row>
						<Cell>{generalRow.name}</Cell>
						<Cell>{generalRow.unit}</Cell>
						<Cell numeric>{generalRow.price} руб/{generalRow.unit}</Cell>
						<Cell numeric>{generalRow.amount} {generalRow.unit}</Cell>
						<Cell numeric>{generalRow.sum} руб</Cell>
					</Row>
				{/each}
			</Body>
			<LinearProgress
				indeterminate
				bind:closed={dataLoaded}
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

<AddGeneralRowDialog
	bind:open={addRowDialogOpen}
	{availableWastes}
    {availableWorks}
	onConfirm={(wasteRow) => {
        generalRows = [...generalRows, wasteRow];
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
