<script lang="ts">
	import { WastesAPI } from '$lib/backend/api/wastes';
	import { validateFKKOCode, type Waste } from '$lib/backend/models/wastes';
	import Button from '@smui/button';
	import { Label } from '@smui/common';
	import Dialog, { Content, Title } from '@smui/dialog';
	import HelperText from '@smui/select/helper-text';
	import Textfield from '@smui/textfield';
	import CircularLoader from '$lib/components/common/CircularLoader.svelte';

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

<Dialog
	bind:open
	selection
	aria-labelledby="dialog-title"
	aria-describedby="dialog-content"
	on:SMUIDialog:closed={closeHandler}
>
	<Title id="dialog-title">Новый отход</Title>
	<Content id="dialog-content">
		<div class="dialog-content">
			{#if wasteCreating}
				<div class="loader-container">
					<CircularLoader size="large" />
				</div>
			{:else if !wasteCreated}
				<div class="name-container">
					<Label style="margin-bottom: 1rem;"><strong>Наименование</strong></Label>
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
				</div>
				<div class="fkko_code-container">
					<Label style="margin-bottom: 1rem;"><strong>Код ФККО</strong></Label>
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
				</div>
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

	.fkko_code-container {
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
