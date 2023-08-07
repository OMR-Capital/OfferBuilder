<script lang="ts">
	import Button, { Label } from '@smui/button';

	export let href: string;
	export let label: string;
</script>

<Button {href} variant="unelevated">
	<Label>{label}</Label>
</Button>
