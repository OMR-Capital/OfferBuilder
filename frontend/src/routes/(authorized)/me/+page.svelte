<script lang="ts">
	import ProfileCard from '$lib/components/me/ProfileCard.svelte';

	export let data;
</script>

<div class="user-container">
	<ProfileCard token={data.token} />
</div>

<style>
	.user-container {
		display: flex;
		justify-content: center;
		align-items: center;
	}
</style>
