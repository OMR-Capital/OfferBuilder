<script lang="ts">
	import { UsersAPI } from '$lib/backend/api/users';
	import type { User } from '$lib/backend/models/users';
	import CircularLoader from '$lib/components/CircularLoader.svelte';
	import IconButton from '$lib/components/IconButton.svelte';
	import Button from '@smui/button';
	import Tooltip, { Wrapper } from '@smui/tooltip';
	import Card, { Content } from '@smui/card';
	import Textfield from '@smui/textfield';
	import HelperText from '@smui/textfield/helper-text';
	import { onMount } from 'svelte';

	export let data;

	const userApi = new UsersAPI(data.token);

	let user: User;

	let name = '';
	let nameUpdated = false;
	let nameUpdating = false;
	let nameError = '';

	function resetName(user: User) {
		name = user.name;
		nameError = '';
		nameUpdated = false;
		nameUpdating = false;
	}

	let login = '';
	let loginUpdated = false;
	let loginUpdating = false;
	let loginError = '';

	function resetLogin(user: User) {
		login = user.login;
		loginError = '';
		loginUpdated = false;
		loginUpdating = false;
	}

	let password: string | null = null;

	async function initUser(): Promise<User> {
		const result = await userApi.getMyUser();
		if (!result.ok) {
			throw result.error;
		} else {
			user = result.value;
			resetName(user);
			resetLogin(user);
			return result.value;
		}
	}

	async function updateName() {
		if (name === user.name) {
			return;
		}
		nameUpdating = true;
		const result = await userApi.updateMyUser({ name });
		if (!result.ok) {
			nameError = result.error.message;
		} else {
			user = result.value;
			resetName(user);
			nameUpdated = true;
		}
		nameUpdating = false;
	}

	async function updateLogin() {
		if (login === user.login) {
			return;
		}
		loginUpdating = true;
		const result = await userApi.updateMyUser({ login });
		if (!result.ok) {
			loginError = result.error.message;
		} else {
			user = result.value;
			resetLogin(user);
			loginUpdated = true;
		}
		loginUpdating = false;
	}

	async function regenPassword() {
		const result = await userApi.regenMyPassword();
		if (!result.ok) {
			loginError = result.error.message;
		} else {
			password = result.value;
		}
	}

	onMount(async () => {
		await initUser();
	});
</script>

<div class="user-container">
	<Card padded>
		<Content>
			<div class="user-content">
				{#if !user}
					<div class="user-content__item">
						<CircularLoader size="large" />
					</div>
				{:else}
					<div class="user-content__item user-title">
						<h6>{user.name}</h6>
					</div>
					<div class="user-content__item">
						<Textfield bind:value={name} style="width: 100%">
							<HelperText slot="helper" persistent>
								{#if nameError}
									{nameError}
								{:else if name !== user.name}
									Нажмите кнопку, чтобы сохранить изменения
								{:else if nameUpdated}
									Изменения сохранены
								{:else}
									Вы можете изменить имя
								{/if}
							</HelperText>
							<svelte:fragment slot="trailingIcon">
								{#if name !== user.name && !nameUpdating}
									<IconButton onClick={updateName} icon="check" />
								{:else if nameUpdating}
									<CircularLoader size="small" />
								{/if}
							</svelte:fragment>
						</Textfield>
					</div>
					<div class="user-content__item">
						<Textfield bind:value={login} style="width: 100%">
							<HelperText slot="helper" persistent>
								{#if loginError}
									{loginError}
								{:else if login !== user.login}
									Нажмите кнопку, чтобы сохранить изменения
								{:else if loginUpdated}
									Изменения сохранены
								{:else}
									Вы можете изменить логин
								{/if}
							</HelperText>
							<svelte:fragment slot="trailingIcon">
								{#if login !== user.login && !loginUpdating}
									<IconButton onClick={updateLogin} icon="check" />
								{:else if loginUpdating}
									<CircularLoader size="small" />
								{/if}
							</svelte:fragment>
						</Textfield>
					</div>
					<div class="user-content__item">
						{#if password}
							<p>Ваш новый пароль: <strong>{password}</strong></p>
						{:else}
							<Wrapper>
								<Button variant="outlined" style="width: 100%" on:click={regenPassword}>
									Обновить пароль
								</Button>
								<Tooltip>Пароль генерируется автоматически</Tooltip>
							</Wrapper>
						{/if}
					</div>
				{/if}
			</div>
		</Content>
	</Card>
</div>

<style>
	.user-container {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100vh;
	}

	.user-title {
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.user-content {
		display: flex;
		flex-direction: column;
		align-items: center;
		width: min(20rem, 100vw);
	}

	.user-content__item {
		margin-bottom: 2rem;
		width: 100%;
	}

	.user-content__item:last-child {
		margin-bottom: 0;
	}
</style>
