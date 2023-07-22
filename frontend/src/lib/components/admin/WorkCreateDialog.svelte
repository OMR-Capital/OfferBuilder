<script lang="ts">
	import { WorksAPI } from '$lib/backend/api/works';
	import type { Work } from '$lib/backend/models/works';
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

	const worksApi = new WorksAPI(token);

	let name = '';

	let workCreated = false;
	let workCreating = false;
	let createdWork: Work | null = null;
	let createError: string | null = null;

	async function createWork() {
		if (!name) return;

		workCreating = true;
		const result = await worksApi.createWork({ name });
		if (result.ok) {
			createdWork = result.value;
			onCreate();
		} else {
			createError = result.error.message;
		}
		workCreated = true;
		workCreating = false;
	}

	async function closeHandler() {
		name = '';
		workCreated = false;
		createdWork = null;
		createError = null;
	}
</script>

<Dialog bind:open title="Новая услуга" {closeHandler}>
	{#if workCreating}
		<CircularLoader size="large" />
	{:else if !workCreated}
		<DialogBlock title="Наименование">
			<Textfield
				variant="outlined"
				bind:value={name}
				label="Наименование"
				style="width: 100%"
				invalid={!name}
			>
				<HelperText persistent slot="helper">
					{#if !name}
						Наименование не может быть пустым
					{/if}
				</HelperText>
			</Textfield>
		</DialogBlock>
	{:else if createdWork}
		<p>Услуга <strong>{createdWork.name}</strong> добавлена.</p>
	{:else}
		<p>Ошибка: {createError}</p>
	{/if}
	<div class="dialog-footer">
		{#if !workCreated}
			<Button
				on:click={() => {
					open = false;
				}}
			>
				<Label>Отмена</Label>
			</Button>
			<Button variant="raised" on:click={createWork}>
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
