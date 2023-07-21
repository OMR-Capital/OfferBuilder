<script lang="ts">
	import { CompaniesAPI } from '$lib/backend/api/companies';
	import type { Company } from '$lib/backend/models/companies';
	import Button from '@smui/button';
	import { Label } from '@smui/common';
	import Dialog, { Content, Title } from '@smui/dialog';
	import HelperText from '@smui/select/helper-text';
	import Textfield from '@smui/textfield';
	import CircularLoader from '$lib/components/common/CircularLoader.svelte';

	export let token: string;
	export let open: boolean;
	export let onCreate: () => void;

	const companiesApi = new CompaniesAPI(token);

	let name = '';

	let companyCreated = false;
	let companyCreating = false;
	let createdCompany: Company | null = null;
	let createError: string | null = null;

	async function createCompany() {
		if (!name) return;

		companyCreating = true;
		const result = await companiesApi.createCompany({ name: name });
		if (result.ok) {
			createdCompany = result.value;
			onCreate();
		} else {
			createError = result.error.message;
		}
		companyCreated = true;
		companyCreating = false;
	}

	async function closeHandler() {
		name = '';
		companyCreated = false;
		createdCompany = null;
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
	<Title id="dialog-title">Новая организация</Title>
	<Content id="dialog-content">
		<div class="dialog-content">
			{#if companyCreating}
				<div class="loader-container">
					<CircularLoader size="large" />
				</div>
			{:else if !companyCreated}
				<div class="name-container">
					<Label style="margin-bottom: 1rem;"><strong>Название</strong></Label>
					<Textfield
						variant="outlined"
						bind:value={name}
						label="Название"
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
			{:else if createdCompany}
				<p>Организация <strong>{createdCompany.name}</strong> добавлена.</p>
			{:else}
				<p>Ошибка: {createError}</p>
			{/if}
			<div class="dialog-footer">
				{#if !companyCreated}
					<Button
						on:click={() => {
							open = false;
						}}
					>
						<Label>Отмена</Label>
					</Button>
					<Button variant="raised" on:click={createCompany}>
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

	.loader-container {
		display: flex;
		flex-direction: row;
		justify-content: center;
		align-items: center;
	}
</style>
