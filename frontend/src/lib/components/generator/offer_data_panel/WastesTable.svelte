<script lang="ts">
	import Snackbar from '$lib/components/common/Snackbar.svelte';
	import Button, { Icon } from '@smui/button';
	import DataTable, { Body, Cell, Head, Row } from '@smui/data-table';
	import type { WasteRow } from '../types';
	import AddWasteRowDialog from './AddWasteRowDialog.svelte';

	export let token: string;

	export let wasteRows: WasteRow[] = [];
	$: nextRowNumber = wasteRows.length + 1;

	export let totalPrice: number = 0;
	$: {
		totalPrice = 0;
		for (const row of wasteRows) {
			totalPrice += row.sum;
		}
	}

	let addRowDialogOpen = false;

	let snackbar: Snackbar;
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
		</DataTable>
		<div class="offer-total-container">
			<b>Итого:</b>
			<span>{totalPrice} руб</span>
		</div>
		<div>
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
</div>

<AddWasteRowDialog
    {token}
	bind:open={addRowDialogOpen}
	bind:rowNumber={nextRowNumber}
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

	.offer-total-container {
		display: flex;
		flex-direction: row;
		justify-content: flex-end;
		align-items: center;
		gap: 1rem;
		margin-right: 1rem;
		height: 2rem;
	}
</style>
