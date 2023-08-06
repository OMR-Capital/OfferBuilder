<script>
	import AuthForm from '$lib/components/auth/AuthCard.svelte';

	export let data;
</script>

<div class="auth-container">
	<AuthForm tokenExpireMinutes={data.tokenExpireMinutes} />
</div>

<style>
	.auth-container {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100vh;
	}
</style>
