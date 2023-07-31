<script lang="ts">
	import type { Waste } from '$lib/backend/models/wastes';
	import type { Work } from '$lib/backend/models/works';
	import CircularLoader from '$lib/components/common/CircularLoader.svelte';
	import Dialog from '$lib/components/common/dialog/Dialog.svelte';
	import DialogBlock from '$lib/components/common/dialog/DialogBlock.svelte';
	import Autocomplete from '@smui-extra/autocomplete';
	import Button from '@smui/button';
	import Chip, { Set } from '@smui/chips';
	import { Label } from '@smui/common';
	import { Text } from '@smui/list';
	import Textfield from '@smui/textfield';
	import type { GeneralRow } from '../types';
	import { Unit } from '../types';

	export let availableWastes: Waste[];
	export let availableWorks: Work[];
	export let rowNumber: number;
	export let open = false;
	export let onConfirm: (generalRow: GeneralRow) => void;

	let generalRow: GeneralRow = {
		num: rowNumber,
		name: '',
		unit: Unit.CubeMetres,
		price: 0,
		amount: 0,
		sum: 0
	};
	$: generalRow.sum = generalRow.price * generalRow.amount;

	interface Item {
		name: string;
	}

	let selectedItem = { name: '' };

	$: updateGeneralRow(selectedItem);

	function updateGeneralRow(selectedItem: Item) {
		if (selectedItem) {
			generalRow.name = selectedItem.name;
		}
	}

	async function searchItem(query: string): Promise<(Waste | Work)[] | false> {
		if (!query) return false;
		const wastes = availableWastes.filter((waste) => {
			return waste.name.toLowerCase().includes(query.toLowerCase());
		});
		const works = availableWorks.filter((work) => {
			return work.name.toLowerCase().includes(query.toLowerCase());
		});
		[wastes, works];
		return [...wastes, ...works];
	}

	function getItemLabel(item: Waste | Work | undefined): string {
		return item ? item.name : '';
	}

	async function closeHandler() {
		generalRow = {
			num: rowNumber,
			name: '',
			unit: Unit.CubeMetres,
			price: 0,
			amount: 0,
			sum: 0
		};

		selectedItem = { name: '' };
	}
</script>

<Dialog bind:open title="Добавление отхода" {closeHandler}>
	<DialogBlock title="Найдите">
		<Autocomplete
			label="Наименование отхода или услуги"
			style="width: 100%;"
			textfield$style="width: 100%;"
			search={searchItem}
			getOptionLabel={getItemLabel}
			bind:value={selectedItem}
		>
			<Text
				slot="loading"
				style="display: flex; width: 100%; justify-content: flex-start; align-items: center;"
			>
				<CircularLoader size="small" />
			</Text>
			<Text slot="no-matches">Ничего не найдено</Text>
		</Autocomplete>
	</DialogBlock>
	<DialogBlock title="Или введите вручную">
		<div class="waste-input-container">
			<Textfield style="width: 100%;" label="Наименование" bind:value={generalRow.name} />
		</div>
	</DialogBlock>
	<DialogBlock title="Ед. изм.">
		<Set chips={Object.values(Unit)} let:chip choice bind:selected={generalRow.unit}>
			<Chip {chip}>
				<Text>{chip}</Text>
			</Chip>
		</Set>
	</DialogBlock>
	<DialogBlock title="Цена за ед. изм.">
		<div class="price-container">
			<Textfield style="width: 100%;" type="number" bind:value={generalRow.price} />
			<Label style="min-width: 3rem;">руб/{generalRow.unit}</Label>
		</div>
	</DialogBlock>
	<DialogBlock title="Кол-во">
		<div class="amount-container">
			<Textfield style="width: 100%;" type="number" bind:value={generalRow.amount} />
			<Label style="min-width: 3rem;">{generalRow.unit}</Label>
		</div>
	</DialogBlock>
	<div class="dialog-footer">
		<Button
			on:click={() => {
				closeHandler();
				open = false;
			}}
		>
			<Label>Отмена</Label>
		</Button>
		<Button
			variant="raised"
			on:click={() => {
				onConfirm(generalRow);
				closeHandler();
				open = false;
			}}
		>
			<Label>Добавить</Label>
		</Button>
	</div>
</Dialog>

<style>
	.waste-input-container {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.price-container {
		display: flex;
		flex-direction: row;
		align-items: center;
		gap: 2rem;
	}

	.amount-container {
		display: flex;
		flex-direction: row;
		align-items: center;
		gap: 2rem;
	}

	.dialog-footer {
		display: flex;
		flex-direction: row;
		justify-content: flex-end;
		gap: 1rem;
	}
</style>
