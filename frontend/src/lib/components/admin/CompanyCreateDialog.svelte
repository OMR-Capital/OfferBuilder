<script lang="ts">
	import { CompaniesAPI } from '$lib/backend/api/companies';
	import type { Company } from '$lib/backend/models/companies';
	import CircularLoader from '$lib/components/common/CircularLoader.svelte';
	import Button from '@smui/button';
	import { Label } from '@smui/common';
	import HelperText from '@smui/select/helper-text';
	import Textfield from '@smui/textfield';
	import Dialog from '../common/dialog/Dialog.svelte';
	import DialogBlock from '../common/dialog/DialogBlock.svelte';

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

<Dialog bind:open title="Новая организация" {closeHandler}>
	{#if companyCreating}
		<CircularLoader size="large" />
	{:else if !companyCreated}
        <DialogBlock title="Название">
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
        </DialogBlock>
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
</Dialog>

<style>
	.dialog-footer {
		display: flex;
		flex-direction: row;
		justify-content: flex-end;
		gap: 1rem;
	}
</style>
