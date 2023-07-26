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

	let snackbar: Snackbar;

	const offerTplsApi = new OfferTplsAPI(token);

	export let selectedOfferTpl: OfferTpl | null = null;
	let offerTpls: OfferTpl[] = [];
	let offerTplsLoading = false;

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
				{#if selectedOfferTpl != null}
					<Button
						variant="outlined"
						href={offerTplsApi.getDownloadUrl(selectedOfferTpl.offer_tpl_id)}
						download={selectedOfferTpl ? selectedOfferTpl.name + '.docx' : ''}
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
