<script lang="ts">
	import { page } from '$app/stores';
</script>

<svelte:head>
	{#if !$page.url.host.includes('localhost')}
		<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests" />
	{/if}
</svelte:head>

<slot />
