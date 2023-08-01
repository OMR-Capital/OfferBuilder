<script lang="ts">
	import { OfferTplsAPI } from '$lib/backend/api/offer_tpls';
	import { OffersAPI } from '$lib/backend/api/offers';
	import { FileFormat } from '$lib/backend/models/docx';
	import type { OfferTpl } from '$lib/backend/models/offer_tpls';
	import type { Offer } from '$lib/backend/models/offers';
	import Panel from '$lib/components/common/Panel.svelte';
	import { user } from '$lib/stores';
	import Button, { Icon, Label } from '@smui/button';
	import CircularLoader from '../common/CircularLoader.svelte';
	import Snackbar from '../common/Snackbar.svelte';
	import type { OfferContext } from './types';

	export let token: string;
	export let offerTpl: OfferTpl | null = null;
	export let offerContext: OfferContext;

	const offerTplsApi = new OfferTplsAPI(token);
	const offersApi = new OffersAPI(token);

	let createdOffer: Offer | null = null;

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
			offerContext.author = $user;
			offerContext.date = new Date().toLocaleDateString('ru-RU', {
				year: 'numeric',
				month: 'long',
				day: 'numeric'
			});

			const result = await offerTplsApi.buildOffer(offerTpl.offer_tpl_id, offerContext);
			if (!result.ok) {
				snackbar.show('Ошибка при создании документа');
			} else {
				createdOffer = result.value;
				snackbar.show('Документ успешно создан');
			}
			offerCreating = false;
		}
	}

	let snackbar: Snackbar;
</script>

<Panel title="Создание КП">
	<div class="build-btn-container">
		{#if offerCreating}
			<CircularLoader />
		{:else if createdOffer !== null}
			<Button variant="outlined" on:click={buildOffer}>
				<Icon class="material-icons">note_add</Icon>
				<Label>Создать еше раз</Label>
			</Button>
			<div class="btns-splitter" />
			<Button
				variant="outlined"
				href={offersApi.getDownloadUrl(createdOffer.offer_id)}
				download={createdOffer.name + '.docx'}
			>
				<Icon class="material-icons">description</Icon>
				<Label>Скачать DOCX</Label>
			</Button>
			<Button
				variant="outlined"
				href={offersApi.getDownloadUrl(createdOffer.offer_id, FileFormat.pdf)}
				download={createdOffer.name + '.pdf'}
			>
				<Icon class="material-icons">picture_as_pdf</Icon>
				<Label>Скачать PDF</Label>
			</Button>
		{:else}
			<Button variant="outlined" on:click={buildOffer}>
				<Icon class="material-icons">note_add</Icon>
				<Label>Создать документ</Label>
			</Button>
		{/if}
	</div>
</Panel>

<Snackbar bind:this={snackbar} />

<style>
	.build-btn-container {
		display: flex;
		flex-wrap: wrap;
		gap: 2rem;
	}

	.btns-splitter {
		width: 2px;
		height: 2rem;
		background-color: rgba(0, 0, 0, 0.12);
	}

	@media (max-width: 600px) {
		.btns-splitter {
			height: 2px;
			width: 100%;
		}
	}
</style>
