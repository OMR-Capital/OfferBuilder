<script lang="ts">
	import Snackbar, { Label } from '@smui/snackbar';

	let snackbar: Snackbar;
	let message = 'Hello, world!';

	export function show(message_: string) {
		message = message_;
		snackbar.open();
	}
</script>

<Snackbar bind:this={snackbar} class="demo-success">
	<Label>{message}</Label>
</Snackbar>
