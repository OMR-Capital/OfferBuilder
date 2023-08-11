<script lang="ts">
	import Snackbar from '$lib/components/common/Snackbar.svelte';
	import Button, { Icon } from '@smui/button';
	import DataTable, { Body, Cell, Head, Row } from '@smui/data-table';
	import type { GeneralRow } from '../types';
	import AddGeneralRowDialog from './AddGeneralRowDialog.svelte';

	export let token: string;

	export let generalRows: GeneralRow[] = [];
	$: nextRowNumber = generalRows.length + 1;

	export let totalPrice: number = 0;
	$: {
		totalPrice = 0;
		for (const row of generalRows) {
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

<AddGeneralRowDialog
    {token}
	bind:open={addRowDialogOpen}
	bind:rowNumber={nextRowNumber}
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
