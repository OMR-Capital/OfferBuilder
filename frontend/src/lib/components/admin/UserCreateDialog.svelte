<script lang="ts">
	import { UsersAPI } from '$lib/backend/api/users';
	import { UserRole, type User } from '$lib/backend/models/users';
	import CircularLoader from '$lib/components/common/CircularLoader.svelte';
	import { userRoleName } from '$lib/texts';
	import Button from '@smui/button';
	import { Label } from '@smui/common';
	import FormField from '@smui/form-field';
	import Radio from '@smui/radio';
	import HelperText from '@smui/select/helper-text';
	import Textfield from '@smui/textfield';
	import Dialog from '../common/dialog/Dialog.svelte';
	import DialogBlock from '../common/dialog/DialogBlock.svelte';

	export let token: string;
	export let open: boolean;
	export let onCreate: () => void;

	const usersApi = new UsersAPI(token);

	let name = '';
	let selectedRole = UserRole.Employee;

	let userCreated = false;
	let userCreating = false;
	let createdUser: User | null = null;
	let createdPassword: string | null = null;
	let createError: string | null = null;

	async function createUser() {
		if (!name) return;

		userCreating = true;
		const result = await usersApi.createUser({
			name: name,
			role: selectedRole
		});
		if (result.ok) {
			createdUser = result.value.user;
			createdPassword = result.value.password;
			onCreate();
		} else {
			createError = result.error.message;
		}
		userCreated = true;
		userCreating = false;
	}

	async function closeHandler() {
		name = '';
		selectedRole = UserRole.Employee;
		userCreated = false;
		createdUser = null;
		createdPassword = null;
		createError = null;
	}
</script>

<Dialog bind:open title="Новый пользователь" {closeHandler}>
	{#if userCreating}
		<CircularLoader size="large" />
	{:else if !userCreated}
		<DialogBlock title="Имя">
			<Textfield
				variant="outlined"
				bind:value={name}
				label="Имя"
				style="width: 100%"
				invalid={!name}
			>
				<HelperText persistent slot="helper">
					{#if !name}
						Имя не может быть пустым
					{/if}
				</HelperText>
			</Textfield>
		</DialogBlock>
		<DialogBlock title="Роль">
			<div class="roles-container">
				{#each Object.values(UserRole) as role}
					<div class="role-row">
						<FormField>
							<Radio bind:group={selectedRole} value={role} />
							<span slot="label">{userRoleName(role)}</span>
						</FormField>
					</div>
				{/each}
			</div>
		</DialogBlock>
	{:else if createdUser}
		<p>Пользователь <strong>{createdUser.name}</strong> создан.</p>
		<div>
			<p>Роль: <strong>{userRoleName(createdUser.role)}</strong></p>
			<p>Логин: <strong>{createdUser.login}</strong></p>
			<p>Пароль: <strong>{createdPassword}</strong></p>
		</div>
		<p>Не забудьте скопировать логин и пароль</p>
	{:else}
		<p>Ошибка: {createError}</p>
	{/if}
	<div class="dialog-footer">
		{#if !userCreated}
			<Button
				on:click={() => {
					open = false;
				}}
			>
				<Label>Отмена</Label>
			</Button>
			<Button variant="raised" on:click={createUser}>
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
	.roles-container {
		display: flex;
		flex-direction: column;
	}

	.role-row {
		display: flex;
		flex-direction: row;
		align-items: center;
	}

	.dialog-footer {
		display: flex;
		flex-direction: row;
		justify-content: flex-end;
		gap: 1rem;
	}
</style>
