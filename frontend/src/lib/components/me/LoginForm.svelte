<script lang="ts">
	import { UsersAPI } from '$lib/backend/api/users';
	import CircularLoader from '$lib/components/common/CircularLoader.svelte';
	import IconButton from '$lib/components/common/IconButton.svelte';
	import { user } from '$lib/stores';
	import Textfield from '@smui/textfield';
	import HelperText from '@smui/textfield/helper-text';

	export let token: string;

	const userApi = new UsersAPI(token);

	let login = $user.login;
	let loginUpdated = false;
	let loginUpdating = false;
	let loginError = '';

	async function updateLogin() {
		if (login === $user.login) {
			return;
		}
		loginUpdating = true;
		const result = await userApi.updateMyUser({ login });
		if (!result.ok) {
			loginError = result.error.message;
		} else {
			$user = result.value;
			login = $user.login;
			loginUpdated = true;
		}
		loginUpdating = false;
	}
</script>

<div class="login-form-container">
	<form on:submit|preventDefault={updateLogin}>
		<Textfield
			style="width: 100%"
			label="Логин"
			type="text"
            input$name="username"
			input$autocomplete="username"
			bind:value={login}
		>
			<HelperText slot="helper" persistent>
				{#if loginError}
					{loginError}
				{:else if login !== $user.login}
					Нажмите кнопку, чтобы сохранить изменения
				{:else if loginUpdated}
					Изменения сохранены
				{:else}
					Вы можете изменить логин
				{/if}
			</HelperText>
			<svelte:fragment slot="trailingIcon">
				{#if login !== $user.login && !loginUpdating}
					<IconButton type="submit" icon="check" />
				{:else if loginUpdating}
					<CircularLoader size="small" />
				{/if}
			</svelte:fragment>
		</Textfield>
	</form>
</div>

<style>
	.login-form-container {
		width: 100%;
	}
</style>
