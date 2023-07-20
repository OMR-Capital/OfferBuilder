<script lang="ts">
	import { page } from '$app/stores';
	import { UserRole } from '$lib/backend/models/users';
	import { user } from '$lib/stores';
	import TopAppBar, { Row, Section, Title, AutoAdjust } from '@smui/top-app-bar';
	import Button, { Label } from '@smui/button';
	import IconButton from '$lib/components/IconButton.svelte';

	let topAppBar: TopAppBar;
</script>

<TopAppBar bind:this={topAppBar} variant="fixed">
	<Row>
		<Section>
			<IconButton onClick={() => {}} icon="description" />
		</Section>
		<Section align="end" toolbar>
			{#if $page.route.id == '/(authorized)/me'}
				<Button href="/generator">
					<Label>Генератор</Label>
				</Button>
			{:else}
				<Button href="/me">
					<Label>Мой профиль</Label>
				</Button>
			{/if}
			{#if $user.role == UserRole.Admin}
				<Button href="/admin">
					<Label>Управление</Label>
				</Button>
			{/if}
		</Section>
	</Row>
</TopAppBar>
<AutoAdjust {topAppBar}>
	<div class="page-content">
		<slot />
	</div>
</AutoAdjust>

<style>
	/* Hide everything above this component. */
	:global(#smui-app),
	:global(body),
	:global(html) {
		display: block !important;
		height: auto !important;
		width: auto !important;
		position: static !important;
	}

	.page-content {
		padding: 4rem;
	}
</style>
