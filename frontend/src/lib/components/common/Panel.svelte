<script lang="ts">
	import Card from '@smui/card';
	import { Content } from '@smui/dialog';

	export let title: string;
</script>

<Card>
	<Content>
        <div class="content-container">
            <h5>{title}</h5>
            <slot />
        </div>
	</Content>
</Card>

<style>
    .content-container {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        padding: 1rem;
    }
</style>
