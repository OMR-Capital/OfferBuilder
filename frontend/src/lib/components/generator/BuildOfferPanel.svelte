<script lang="ts">
	import { OfferTplsAPI } from '$lib/backend/api/offer_tpls';
	import type { OfferTpl } from '$lib/backend/models/offer_tpls';
	import Panel from '$lib/components/common/Panel.svelte';
	import Button, { Icon, Label } from '@smui/button';
	import CircularLoader from '../common/CircularLoader.svelte';
	import Snackbar from '../common/Snackbar.svelte';
	import type { OfferContext } from './types';

	export let token: string;
	export let offerTpl: OfferTpl | null = null;
	export let offerContext: OfferContext;

	const offerTplsApi = new OfferTplsAPI(token);

	let offerCreating = false;

	async function buildOffer() {
		if (!offerTpl) {
			snackbar.show('Не выбран шаблон');
		} else if (!offerContext.agent) {
			snackbar.show('Не выбран контр-агент');
		} else if (!offerContext.company) {
			snackbar.show('Не выбрана организация');
		} else if (!offerContext.offerType) {
			snackbar.show('Не выбран тип документа');
		} else if (!offerContext.offerData) {
			snackbar.show('Не введены данные документа');
		} else {
			offerCreating = true;
			offerContext.date = new Date().toDateString();

			const result = await offerTplsApi.buildOffer(offerTpl.offer_tpl_id, offerContext);
			if (!result.ok) {
				snackbar.show('Ошибка при создании документа');
			} else {
				snackbar.show('Документ успешно создан');
				const blob = result.value;
				const url = window.URL.createObjectURL(blob);
				const a = document.createElement('a');
				a.href = url;
				a.download = offerTpl.name + '.docx';
				document.body.appendChild(a);
				a.click();
				a.remove();
			}
			offerCreating = false;
		}
	}

	let snackbar: Snackbar;
</script>

<Panel title="Создание КП">
	<div class="build-btn-container">
		{#if offerCreating}
			<CircularLoader size="small" />
		{:else}
			<Button variant="outlined" on:click={buildOffer}>
				<Icon class="material-icons">note_add</Icon>
				<Label>Создать документ</Label>
			</Button>
		{/if}
	</div>
    {JSON.stringify(offerContext)}
</Panel>

<Snackbar bind:this={snackbar} />

<style>
	.build-btn-container {
		display: flex;
		flex-direction: row;
		align-items: flex-start;
	}
</style>
