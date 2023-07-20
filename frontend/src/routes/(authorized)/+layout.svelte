<script lang="ts">
	import { UsersAPI } from '$lib/backend/api/users';
	import CircularLoader from '$lib/components/CircularLoader.svelte';
	import { user } from '$lib/stores';
	import { onMount } from 'svelte';
	import PageWithNavbar from './PageWithNavbar.svelte';

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
			throw result.error;
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
