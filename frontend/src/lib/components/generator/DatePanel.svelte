<script lang="ts">
	import Panel from '../common/Panel.svelte';
	import Textfield from '@smui/textfield';

	export let date: string = '';

	let inputDate = new Date().toISOString().slice(0, 10);

	$: date = new Date(inputDate).toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
    });
</script>

<Panel title="Дата создания">
	<Textfield type="date" bind:value={inputDate} label="Дата создания" />
</Panel>
