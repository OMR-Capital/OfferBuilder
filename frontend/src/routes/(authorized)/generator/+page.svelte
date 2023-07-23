<script lang="ts">
	import type { Company } from '$lib/backend/models/companies.js';
	import CompaniesPanel from '$lib/components/generator/CompaniesPanel.svelte';

	export let data;

	let company: Company | undefined = undefined;
</script>

<!--
<h1>Generator</h1>
<p>template</p>
<p>organization</p>
<p>contr-agent</p>
<p>type</p>
<p>wastes and works table</p>
<p>add item</p>
<p>generate</p> -->

<div class="panels-container">
	<CompaniesPanel token={data.token} bind:selectedCompany={company} />
</div>
