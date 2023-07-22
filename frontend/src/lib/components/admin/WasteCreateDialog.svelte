<script lang="ts">
	import { WastesAPI } from '$lib/backend/api/wastes';
	import { validateFKKOCode, type Waste } from '$lib/backend/models/wastes';
	import Button from '@smui/button';
	import { Label } from '@smui/common';
	import Dialog from '../common/dialog/Dialog.svelte';
	import HelperText from '@smui/select/helper-text';
	import Textfield from '@smui/textfield';
	import CircularLoader from '$lib/components/common/CircularLoader.svelte';
	import DialogBlock from '../common/dialog/DialogBlock.svelte';

	export let token: string;
	export let open: boolean;
	export let onCreate: () => void;

	const wastesApi = new WastesAPI(token);

	let name = '';
	let fkko_code = '';

	let wasteCreated = false;
	let wasteCreating = false;
	let createdWaste: Waste | null = null;
	let createError: string | null = null;

	async function createWaste() {
		if (!name || !validateFKKOCode(fkko_code)) return;

		wasteCreating = true;
		const result = await wastesApi.createWaste({ name, fkko_code });
		if (result.ok) {
			createdWaste = result.value;
			onCreate();
		} else {
			createError = result.error.message;
		}
		wasteCreated = true;
		wasteCreating = false;
	}

	async function closeHandler() {
		name = '';
		fkko_code = '';
		wasteCreated = false;
		createdWaste = null;
		createError = null;
	}
</script>

<Dialog bind:open title="Новый отход" {closeHandler}>
	{#if wasteCreating}
		<CircularLoader size="large" />
	{:else if !wasteCreated}
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
		<DialogBlock title="Код ФККО">
			<Textfield
				variant="outlined"
				bind:value={fkko_code}
				label="Код ФККО"
				style="width: 100%"
				invalid={!validateFKKOCode(fkko_code)}
			>
				<HelperText persistent slot="helper">
					{#if !validateFKKOCode(fkko_code)}
						Код ФККО должен состоять из цифр и пробелов
					{/if}
				</HelperText>
			</Textfield>
		</DialogBlock>
	{:else if createdWaste}
		<p>Отход <strong>{createdWaste.name}</strong> добавлен.</p>
		<div>
			<p>Код ФККО: <strong>{createdWaste.fkko_code}</strong></p>
		</div>
	{:else}
		<p>Ошибка: {createError}</p>
	{/if}
	<div class="dialog-footer">
		{#if !wasteCreated}
			<Button
				on:click={() => {
					open = false;
				}}
			>
				<Label>Отмена</Label>
			</Button>
			<Button variant="raised" on:click={createWaste}>
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
