<script lang="ts">
	import { UsersAPI } from '$lib/backend/api/users';
	import PageWithNavbar from '$lib/components/layout/PageWithNavbar.svelte';
	import CircularLoader from '$lib/components/common/CircularLoader.svelte';
	import { user } from '$lib/stores';
	import { redirect } from '@sveltejs/kit';
	import { onMount } from 'svelte';

	export let data;

	const usersApi = new UsersAPI(data.token);

	/**
	 * Get the current user from the backend.
	 * If the user is already in the store, return it.
	 * Otherwise, fetch it from the backend and store it.
	 *
	 * If page depends on relevant user data is should update userStore.
	 */
	onMount(async () => {
		if ($user) {
			return $user;
		}

		const result = await usersApi.getMyUser();
		if (!result.ok) {
			redirect(307, '/auth');
		} else {
			$user = result.value;
			return result.value;
		}
	});
</script>

{#if $user}
	<PageWithNavbar>
		<slot />
	</PageWithNavbar>
{:else}
	<div class="loader-container">
		<CircularLoader size="large" />
	</div>
{/if}

<style>
	.loader-container {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100vh;
	}
</style>
