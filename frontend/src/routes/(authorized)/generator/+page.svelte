<script lang="ts">
	import type { Company } from '$lib/backend/models/companies';
	import type { OfferTpl } from '$lib/backend/models/offer_tpls';
	import CompaniesPanel from '$lib/components/generator/CompaniesPanel.svelte';
	import OfferTplsPanel from '$lib/components/generator/OfferTplsPanel.svelte';

	export let data;

	let offerTpl: OfferTpl | null = null;
	let companyName: string | undefined = undefined;
</script>

<!--
<h1>Generator</h1>
+ <p>template</p>
+ <p>organization</p>
<p>contr-agent</p>
<p>type</p>
<p>wastes and works table</p>
<p>add item</p>
<p>generate</p> -->

<div class="panels-container">
	<OfferTplsPanel token={data.token} bind:selectedOfferTpl={offerTpl} />
	<CompaniesPanel token={data.token} bind:selectedCompanyName={companyName} />
</div>

<style>
    .panels-container {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        gap: 4rem;
    }
</style>
