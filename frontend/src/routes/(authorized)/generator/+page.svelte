<script lang="ts">
	import type { Agent } from '$lib/backend/models/agents';
	import type { OfferTpl } from '$lib/backend/models/offer_tpls';
	import AgentsPanel from '$lib/components/generator/AgentsPanel.svelte';
	import CompaniesPanel from '$lib/components/generator/CompaniesPanel.svelte';
	import OfferDataPanel from '$lib/components/generator/offer_data_panel/OfferDataPanel.svelte';
	import type {
		GeneralRow,
		OfferType,
		WasteRow
	} from '$lib/components/generator/offer_data_panel/types';
	import OfferTplsPanel from '$lib/components/generator/OfferTplsPanel.svelte';

	export let data;

	let offerTpl: OfferTpl | null = null;
	let companyName: string | null = null;
	let agent: Agent;
	let offerType: OfferType;
	let offerData: WasteRow[] | GeneralRow[] = [];
</script>

<!--
<h1>Generator</h1>
+ <p>template</p>
+ <p>organization</p>
+ <p>contr-agent</p>
+ <p>type</p>
+ <p>wastes and works table</p>
+ <p>add item</p>
<p>generate</p> -->

<div class="panels-container">
	<OfferTplsPanel token={data.token} bind:selectedOfferTpl={offerTpl} />
	<CompaniesPanel token={data.token} bind:selectedCompanyName={companyName} />
	<AgentsPanel token={data.token} bind:agent />
	<OfferDataPanel token={data.token} bind:offerType bind:offerData />
</div>

<style>
	.panels-container {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		gap: 4rem;
	}
</style>
