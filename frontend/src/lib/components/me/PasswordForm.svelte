<script lang="ts">
	import { UsersAPI } from '$lib/backend/api/users';
	import CircularLoader from '$lib/components/common/CircularLoader.svelte';
	import { user } from '$lib/stores';
	import Button from '@smui/button';
	import Tooltip, { Wrapper } from '@smui/tooltip';

	export let token: string;

	const userApi = new UsersAPI(token);

	let password: string | null = null;
	let passwordUpdating = false;

	async function regenPassword() {
		passwordUpdating = true;
		const result = await userApi.regenMyPassword();
		if (result.ok) {
			password = result.value;
		}
		passwordUpdating = false;
	}
</script>

<div class="password-form-container">
	<form on:submit|preventDefault={regenPassword}>
		{#if password}
			<p>Ваш новый пароль: <strong>{password}</strong></p>
		{:else if passwordUpdating}
			<CircularLoader />
		{:else}
			<Wrapper>
				<Button variant="outlined" style="width: 100%" type="submit">Обновить пароль</Button>
				<Tooltip>Пароль генерируется автоматически</Tooltip>
			</Wrapper>
		{/if}
		<input
			bind:value={$user.login}
			type="text"
			name="username"
			id="username"
			autocomplete="username"
			style="display: none"
		/>
		<input
			bind:value={password}
			type="password"
			name="new-password"
			id="new-password"
			autocomplete="new-password"
			style="display: none"
		/>
	</form>
</div>

<style>
	.password-form-container {
		width: 100%;
	}
</style>
