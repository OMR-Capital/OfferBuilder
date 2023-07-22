<script lang="ts">
	import { Label } from '@smui/common';

	export let title: string;
</script>

<div class="dialog-block">
	<div class="block-title">
		<Label>{title}</Label>
	</div>
	<slot />
</div>

<style>
	.block-title {
		margin-bottom: 1rem;
	}
</style>
