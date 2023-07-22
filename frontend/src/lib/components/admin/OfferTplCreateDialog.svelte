<script lang="ts">
	import { OfferTplsAPI } from '$lib/backend/api/offer_tpls';
	import type { OfferTpl } from '$lib/backend/models/offer_tpls';
	import CircularLoader from '$lib/components/common/CircularLoader.svelte';
	import Button from '@smui/button';
	import { Label } from '@smui/common';
	import Dialog, { Content, Title } from '@smui/dialog';
	import HelperText from '@smui/select/helper-text';
	import Textfield from '@smui/textfield';
	import FileLoader from '../common/FileLoader.svelte';

	export let token: string;
	export let open: boolean;
	export let onCreate: () => void;

	const allowedExtensions = ['doc', 'docx'];

	const offerTplsApi = new OfferTplsAPI(token);

	let name = '';
	let offer_tpl_file = '';

	let offerTplCreated = false;
	let offerTplCreating = false;
	let createdOfferTpl: OfferTpl | null = null;
	let createError: string | null = null;

	async function createOfferTpl() {
		if (!name || !offer_tpl_file) return;

		offerTplCreating = true;
		const result = await offerTplsApi.createOfferTpl({ name, offer_tpl_file });
		if (result.ok) {
			createdOfferTpl = result.value;
			onCreate();
		} else {
			createError = result.error.message;
		}
		offerTplCreated = true;
		offerTplCreating = false;
	}

	async function closeHandler() {
		name = '';
		offerTplCreated = false;
		createdOfferTpl = null;
		createError = null;
	}
</script>

<Dialog
	bind:open
	selection
	aria-labelledby="dialog-title"
	aria-describedby="dialog-content"
	on:SMUIDialog:closed={closeHandler}
>
	<Title id="dialog-title">Новый шаблон</Title>
	<Content id="dialog-content">
		<div class="dialog-content">
			{#if offerTplCreating}
                <CircularLoader size="large" />
			{:else if !offerTplCreated}
				<div class="name-container">
					<Label style="margin-bottom: 1rem;"><strong>Название</strong></Label>
					<Textfield
						variant="outlined"
						bind:value={name}
						label="Наименование"
						style="width: 100%"
						invalid={!name}
					>
						<HelperText persistent slot="helper">
							{#if !name}
								Название не может быть пустым
							{/if}
						</HelperText>
					</Textfield>
				</div>
				<div class="file-container">
					<FileLoader bind:base64Data={offer_tpl_file} {allowedExtensions} />
				</div>
			{:else if createdOfferTpl}
				<p>Шаблон <strong>{createdOfferTpl.name}</strong> добавлен.</p>
			{:else}
				<p>Ошибка: {createError}</p>
			{/if}
			<div class="dialog-footer">
				{#if !offerTplCreated}
					<Button
						on:click={() => {
							open = false;
						}}
					>
						<Label>Отмена</Label>
					</Button>
					<Button variant="raised" on:click={createOfferTpl}>
						<Label>Создать</Label>
					</Button>
				{:else}
					<Button
						variant="raised"
						on:click={() => {
							open = false;
						}}
					>
						<Label>Закрыть</Label>
					</Button>
				{/if}
			</div>
		</div>
	</Content>
</Dialog>

<style>
	.dialog-content {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		padding: 2rem;
		width: min(20rem, 100vw);
	}

	.name-container {
		display: flex;
		flex-direction: column;
	}

	.dialog-footer {
		display: flex;
		flex-direction: row;
		justify-content: flex-end;
		gap: 1rem;
	}
</style>
