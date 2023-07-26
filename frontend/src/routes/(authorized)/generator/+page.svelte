<script lang="ts">
	import type { OfferTpl } from '$lib/backend/models/offer_tpls';
	import AgentsPanel from '$lib/components/generator/AgentsPanel.svelte';
	import BuildOfferPanel from '$lib/components/generator/BuildOfferPanel.svelte';
	import CompaniesPanel from '$lib/components/generator/CompaniesPanel.svelte';
	import OfferTplsPanel from '$lib/components/generator/OfferTplsPanel.svelte';
	import OfferDataPanel from '$lib/components/generator/offer_data_panel/OfferDataPanel.svelte';
	import type { OfferContext } from '$lib/components/generator/types.js';

	export let data;

	let offerTpl: OfferTpl | null = null;
	let offerContext: OfferContext = {};
</script>

<div class="panels-container">
	<OfferTplsPanel token={data.token} bind:selectedOfferTpl={offerTpl} />
	<CompaniesPanel token={data.token} bind:selectedCompany={offerContext.company} />
	<AgentsPanel token={data.token} bind:agent={offerContext.agent} />
	<OfferDataPanel
		token={data.token}
		bind:offerType={offerContext.offerType}
		bind:offerData={offerContext.offerData}
	/>
	<BuildOfferPanel token={data.token} bind:offerContext bind:offerTpl />
</div>

<style>
	.panels-container {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		gap: 4rem;
	}
</style>
