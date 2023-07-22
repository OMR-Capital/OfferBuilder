<script lang="ts">
	import Dialog, { Content, Title } from '@smui/dialog';

	export let open: boolean;
	export let title: string;
	export let closeHandler: () => void;
</script>

<Dialog
	bind:open
	selection
	aria-labelledby="dialog-title"
	aria-describedby="dialog-content"
	on:SMUIDialog:closed={closeHandler}
>
	<Title id="dialog-title">{title}</Title>
	<Content id="dialog-content">
		<div class="dialog-content">
			<slot />
		</div>
	</Content>
</Dialog>

<style>
	.dialog-content {
		display: flex;
		flex-direction: column;
		gap: 2rem;
		padding: 2rem;
		width: min(20rem, 100vw);
	}
</style>
