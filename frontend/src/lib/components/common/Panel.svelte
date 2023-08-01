<script lang="ts">
	import Card, { Content } from '@smui/card';

	export let title: string;
</script>

<Card>
	<Content>
        <h5 class="panel-title">{title}</h5>
		<div class="content-container">
			<slot />
		</div>
	</Content>
</Card>

<style>
    .panel-title {
        margin-bottom: 1rem;
    }

	.content-container {
		display: flex;
		flex-direction: column;
		gap: 2rem;
	}
</style>
