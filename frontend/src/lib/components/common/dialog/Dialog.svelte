<script lang="ts">
	import Dialog, { Content, Header, Title } from '@smui/dialog';

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
	{...$$restProps}
>
	<Header>
		<Title id="title">{title}</Title>
	</Header>
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
		padding: 1rem 2rem 2rem 2rem;
		min-width: 30rem;
	}

	@media (max-width: 600px) {
		.dialog-content {
			width: auto;
		}
	}
</style>
