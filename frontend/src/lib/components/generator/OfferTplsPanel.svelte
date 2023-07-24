<script lang="ts">
	import { OfferTplsAPI } from '$lib/backend/api/offer_tpls';
	import type { OfferTpl } from '$lib/backend/models/offer_tpls';
	import Button, { Icon } from '@smui/button';
	import { Label } from '@smui/common';
	import Select, { Option } from '@smui/select';
	import { onMount } from 'svelte';
	import CircularLoader from '../common/CircularLoader.svelte';
	import Panel from '../common/Panel.svelte';
	import Snackbar from '../common/Snackbar.svelte';

	export let token: string;

	type Fruit = { id: number; label: string; price: number };
	let fruits: Fruit[] = [
		{ id: 1, label: 'Apple', price: 35 },
		{ id: 2, label: 'Orange', price: 38 },
		{ id: 3, label: 'Banana', price: 28 },
		{ id: 4, label: 'Mango', price: 25 }
	];

	let valueA: Fruit | null = null;

	let snackbar: Snackbar;

	const offerTplsApi = new OfferTplsAPI(token);

	export let selectedOfferTpl: OfferTpl | null = null;
	let offerTpls: OfferTpl[] = [];
	let offerTplsLoading = false;
	let fileDownloading = false;

	async function updateOfferTpls() {
		offerTplsLoading = true;
		const result = await offerTplsApi.getOfferTpls();
		if (result.ok) {
			offerTpls = result.value;
		} else {
			snackbar.show(result.error.message);
		}
		offerTplsLoading = false;
	}

	function getOfferTplKey(offerTpl: OfferTpl | null): string {
		return offerTpl ? offerTpl.offer_tpl_id : '';
	}

	async function downloadOfferTpl() {
		if (selectedOfferTpl == null) return;

		fileDownloading = true;
		const result = await offerTplsApi.downloadOfferTpl(selectedOfferTpl.offer_tpl_id);
		fileDownloading = false;
		if (result.ok) {
			const blob = result.value;
			const url = window.URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = selectedOfferTpl.name + '.docx';
			document.body.appendChild(a);
			a.click();
			a.remove();
		} else {
			snackbar.show(result.error.message);
		}
	}

	onMount(updateOfferTpls);
</script>

<Panel title="Шаблон документа">
	{#if offerTplsLoading}
		<CircularLoader size="large" />
	{:else}
		<div class="offerTpl-selection-container">
			<Select label="Шаблон" key={getOfferTplKey} bind:value={selectedOfferTpl}>
				{#each offerTpls as offerTpl (getOfferTplKey(offerTpl))}
					<Option value={offerTpl}>{offerTpl.name}</Option>
				{/each}
			</Select>

			<div class="download-btn-container">
				{#if fileDownloading}
					<CircularLoader size="small" />
				{:else}
					<Button
						variant="outlined"
						disabled={selectedOfferTpl == null}
						on:click={downloadOfferTpl}
					>
						<Icon class="material-icons">download_outlined</Icon>
						<Label>Скачать выбранный шаблон</Label>
					</Button>
				{/if}
			</div>
		</div>
	{/if}
</Panel>

<Snackbar bind:this={snackbar} />

<style>
	.offerTpl-selection-container {
		display: flex;
		flex-direction: column;
		gap: 2rem;
	}

    .download-btn-container {
        display: flex;
        justify-content: flex-start;
    }
</style>
