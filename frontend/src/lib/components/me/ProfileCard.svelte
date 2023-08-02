<script lang="ts">
	import { UsersAPI } from '$lib/backend/api/users';
	import type { User } from '$lib/backend/models/users';
	import CircularLoader from '$lib/components/common/CircularLoader.svelte';
	import { user } from '$lib/stores';
	import Card, { Content } from '@smui/card';
	import { onMount } from 'svelte';
	import LoginForm from './LoginForm.svelte';
	import NameForm from './NameForm.svelte';
	import PasswordForm from './PasswordForm.svelte';

	export let token: string;

	const userApi = new UsersAPI(token);

	async function updateUser(): Promise<User> {
		const result = await userApi.getMyUser();
		if (!result.ok) {
			throw result.error;
		} else {
			$user = result.value;
			return result.value;
		}
	}

	onMount(async () => {
		await updateUser();
	});
</script>

<Card padded>
	<Content>
		<div class="user-content">
			{#if !$user}
				{$user}
				<div class="user-content__item">
					<CircularLoader size="large" />
				</div>
			{:else}
				<div class="user-content__item user-title">
					<h6>{$user.name}</h6>
				</div>
				<NameForm {token} />
				<LoginForm {token} />
				<PasswordForm {token} />
			{/if}
		</div>
	</Content>
</Card>

<style>
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
		gap: 2rem;
	}
</style>
