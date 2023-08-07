<script lang="ts">
	import { page } from '$app/stores';
	import { UserRole } from '$lib/backend/models/users';
	import IconButton from '$lib/components/common/IconButton.svelte';
	import { user } from '$lib/stores';
	import TopAppBar, { AutoAdjust, Row, Section } from '@smui/top-app-bar';
	import NavLink from './NavLink.svelte';

	let topAppBar: TopAppBar;
</script>

<TopAppBar bind:this={topAppBar} variant="fixed">
	<Row>
		<Section>
			<IconButton onClick={() => {}} icon="description" />
		</Section>
		<Section align="end" toolbar>
			{#if $page.route.id != '/(authorized)/generator'}
				<NavLink href="/generator" label="Генератор" />
			{/if}
			{#if $page.route.id != '/(authorized)/me'}
				<NavLink href="/me" label="Профиль" />
			{/if}
			{#if ($user.role == UserRole.Admin || $user.role == UserRole.Superuser) && $page.route.id != '/(authorized)/admin'}
				<NavLink href="/admin" label="Управление" />
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

	@media (max-width: 600px) {
		.page-content {
			padding: 0;
		}
	}
</style>
