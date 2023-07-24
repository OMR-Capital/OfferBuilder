<script lang="ts">
	import { Label } from '@smui/common';

	export let title: string | null = null;
</script>

<div class="dialog-block">
	{#if title}
		<div class="block-title">
			<Label>{title}</Label>
		</div>
	{/if}
	<slot />
</div>

<style>
	.block-title {
		margin-bottom: 1rem;
	}
</style>
