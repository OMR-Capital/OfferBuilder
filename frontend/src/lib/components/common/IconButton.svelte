<script lang="ts">
	import IconButton from '@smui/icon-button';

	export let icon: string;
    export let onClick: () => void;
</script>

<IconButton {...$$restProps} on:click={onClick} class="material-icons">{icon}</IconButton>
