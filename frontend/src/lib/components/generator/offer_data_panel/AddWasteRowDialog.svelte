<script lang="ts">
	import { WastesAPI } from '$lib/backend/api/wastes';
	import {
		normalizeFKKOCode,
		normalizeName,
		validateFKKOCode,
		type Waste
	} from '$lib/backend/models/wastes';
	import CircularLoader from '$lib/components/common/CircularLoader.svelte';
	import Dialog from '$lib/components/common/dialog/Dialog.svelte';
	import DialogBlock from '$lib/components/common/dialog/DialogBlock.svelte';
	import Autocomplete from '@smui-extra/autocomplete';
	import Button from '@smui/button';
	import Chip, { Set } from '@smui/chips';
	import { Label } from '@smui/common';
	import { Text } from '@smui/list';
	import Textfield from '@smui/textfield';
	import type { WasteRow } from '../types';
	import { Unit } from '../types';

	export let token: string;
	export let rowNumber: number;
	export let open = false;
	export let onConfirm: (wasteRow: WasteRow) => void;

	let wastesApi = new WastesAPI(token);

	let wasteRow: WasteRow = {
		num: rowNumber,
		name: '',
		fkko_code: '',
		unit: Unit.CubeMetres,
		price: 0,
		amount: 0,
		sum: 0
	};
	$: wasteRow.sum = wasteRow.price * wasteRow.amount;

	let selectedWaste: Waste | undefined = {
		waste_id: '',
		name: '',
		fkko_code: ''
	};

	$: updateWasteRow(selectedWaste);

	function updateWasteRow(newWaste: Waste | undefined) {
		if (newWaste) {
			wasteRow.name = newWaste.name;
			wasteRow.fkko_code = newWaste.fkko_code;
		}
	}

	let searchCounter = 0;

	async function searchWaste(query: string): Promise<Waste[] | false> {
		async function _searchWaste(query: string): Promise<Waste[] | false> {
			let wastes: Waste[] = [];
			if (validateFKKOCode(query)) {
				query = normalizeFKKOCode(query);
				const result = await wastesApi.getWastes(
					{ limit: 10, last: null },
					{ fkko_code_prefix: query }
				);
				if (result.ok) {
					wastes = result.value.wastes;
				}
			} else {
				query = normalizeName(query);
				const result = await wastesApi.getWastes(
					{ limit: 10, last: null },
					{ name_contains: query }
				);
				if (result.ok) {
					wastes = result.value.wastes;
				}
			}
			return wastes;
		}

		if (query.length < 3) return false;

		const myCounter = ++searchCounter;

		return new Promise((resolve) => {
			setTimeout(async () => {
				if (myCounter !== searchCounter) {
                    return;
                }
                const wastes = await _searchWaste(query);
                resolve(wastes);
			}, 500);
		});
	}

	function getWasteLabel(waste: Waste | undefined): string {
		if (!waste) return '';

		const wasteLabel = `${waste.name} (${waste.fkko_code})`;
		return wasteLabel;
	}

	async function closeHandler() {
		wasteRow = {
			num: rowNumber,
			name: '',
			fkko_code: '',
			unit: Unit.CubeMetres,
			price: 0,
			amount: 0,
			sum: 0
		};

		selectedWaste = {
			waste_id: '',
			name: '',
			fkko_code: ''
		};
	}
</script>

<Dialog fullscreen bind:open title="Добавление отхода" {closeHandler}>
	<DialogBlock title="Найдите">
		<Autocomplete
			label="Наименование или ФККО"
			style="width: 100%;"
			textfield$style="width: 100%;"
			search={searchWaste}
			getOptionLabel={getWasteLabel}
			bind:value={selectedWaste}
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
			<Textfield style="width: 100%;" label="Наименование" bind:value={wasteRow.name} />
			<Textfield style="width: 100%;" label="ФККО" bind:value={wasteRow.fkko_code} />
		</div>
	</DialogBlock>
	<DialogBlock title="Ед. изм.">
		<Set chips={Object.values(Unit)} let:chip choice bind:selected={wasteRow.unit}>
			<Chip {chip}>
				<Text>{chip}</Text>
			</Chip>
		</Set>
	</DialogBlock>
	<DialogBlock title="Цена за ед. изм.">
		<div class="price-container">
			<Textfield style="width: 100%;" type="number" input$min="0" bind:value={wasteRow.price} />
			<Label style="min-width: 3rem;">руб/{wasteRow.unit}</Label>
		</div>
	</DialogBlock>
	<DialogBlock title="Кол-во">
		<div class="amount-container">
			<Textfield style="width: 100%;" type="number" input$min="0" bind:value={wasteRow.amount} />
			<Label style="min-width: 3rem;">{wasteRow.unit}</Label>
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
				onConfirm(wasteRow);
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
