<script lang="ts">
	import { UsersAPI } from '$lib/backend/api/users';
	import { UserRole, type User } from '$lib/backend/models/users';
	import { userRoleName } from '$lib/texts';
	import Button from '@smui/button';
	import { Label } from '@smui/common';
	import Dialog, { Actions, Content, Title } from '@smui/dialog';
	import FormField from '@smui/form-field';
	import Radio from '@smui/radio';
	import HelperText from '@smui/select/helper-text';
	import Textfield from '@smui/textfield';
	import CircularLoader from '../CircularLoader.svelte';

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

<Dialog
	bind:open
	selection
	aria-labelledby="dialog-title"
	aria-describedby="dialog-content"
	on:SMUIDialog:closed={closeHandler}
>
	<Title id="dialog-title">Новый пользователь</Title>
	<Content id="dialog-content">
		<div class="dialog-content">
			{#if userCreating}
                <div class="loader-container">
                    <CircularLoader size="large"/>
                </div>
			{:else if !userCreated}
				<div class="name-container">
					<Label style="margin-bottom: 1rem;"><strong>Имя</strong></Label>
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
				</div>
				<div class="roles-container">
					<Label style="margin-bottom: 1rem;"><strong>Роль</strong></Label>
					{#each Object.values(UserRole) as role}
						<div class="role-row">
							<FormField>
								<Radio bind:group={selectedRole} value={role} />
								<span slot="label">{userRoleName(role)}</span>
							</FormField>
						</div>
					{/each}
				</div>
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

    .loader-container {
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
    }
</style>