<script lang="ts">
	import Chip, { Set, Text } from '@smui/chips';
	import { Label } from '@smui/common';
	import Panel from '../../common/Panel.svelte';
	import GeneralTable from './GeneralTable.svelte';
	import WastesTable from './WastesTable.svelte';
	import { OfferType, type GeneralRow, type WasteRow } from '../types';

	export let token: string;
	export let offerData: WasteRow[] | GeneralRow[] = [];
	export let offerType: OfferType = OfferType.Wastes;
	export let offerTotal: number = 0;

	let wasteRows: WasteRow[] = [];
	let generalRows: GeneralRow[] = [];
	$: offerData = offerType === OfferType.Wastes ? wasteRows : generalRows;
</script>

<Panel title="Данные КП">
	<div class="offer-type-container">
		<Label>Тип КП:</Label>
		<Set chips={Object.values(OfferType)} let:chip choice bind:selected={offerType}>
			<Chip {chip}>
				<Text>{chip}</Text>
			</Chip>
		</Set>
	</div>
	<div class="items-table-container">
		{#if offerType === OfferType.Wastes}
			<WastesTable {token} bind:wasteRows bind:totalPrice={offerTotal}/>
		{:else}
			<GeneralTable {token} bind:generalRows bind:totalPrice={offerTotal} />
		{/if}
	</div>
</Panel>

<style>
	.offer-type-container {
		display: flex;
		flex-direction: row;
		justify-content: flex-start;
		align-items: center;
		gap: 1rem;
		margin-bottom: 1rem;
	}
</style>
