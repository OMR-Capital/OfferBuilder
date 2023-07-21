<script lang="ts">
	import { WorksAPI } from '$lib/backend/api/works';
	import type { Work } from '$lib/backend/models/works';
	import CircularLoader from '$lib/components/CircularLoader.svelte';
	import IconButton from '$lib/components/IconButton.svelte';
	import Snackbar from '$lib/components/Snackbar.svelte';
	import Button, { Icon } from '@smui/button';
	import DataTable, { Body, Cell, Head, Row } from '@smui/data-table';
	import LinearProgress from '@smui/linear-progress';
	import { onMount } from 'svelte';
	import WorkCreateDialog from './WorkCreateDialog.svelte';

	export let token: string;

	let snackbar: Snackbar;

	const worksApi = new WorksAPI(token);

	let works: Work[] = [];
	let worksLoaded = false;

	async function updateWorks() {
		worksLoaded = false;
		const result = await worksApi.getWorks();
		if (result.ok) {
			works = result.value;
		} else {
			snackbar.show(result.error.message);
		}
		worksLoaded = true;
	}

	let workDeleting: Record<string, boolean> = {};
	$: {
		works.map((work) => {
			workDeleting[work.work_id] = false;
		});
	}

	async function deleteWork(work_id: string) {
		workDeleting[work_id] = true;
		const result = await worksApi.deleteWork(work_id);
		if (result.ok) {
			updateWorks();
		} else {
			snackbar.show(result.error.message);
		}
		workDeleting[work_id] = false;
	}

	let createDialogOpen = false;

	onMount(updateWorks);
</script>

<div>
	<h5>Услуги</h5>
	<div class="table-container">
		<DataTable table$aria-label="Список услуг" style="width: 100%;">
			<Head>
				<Row>
					<Cell>ID</Cell>
					<Cell>Наименование</Cell>
					<Cell />
				</Row>
			</Head>
			<Body>
				{#each works as work}
					<Row>
						<Cell>{work.work_id}</Cell>
						<Cell style="width: 100%">{work.name}</Cell>
						<Cell>
							{#if workDeleting[work.work_id]}
								<CircularLoader size="small" />
							{:else}
								<IconButton onClick={() => deleteWork(work.work_id)} icon="delete" />
							{/if}
						</Cell>
					</Row>
				{/each}
			</Body>
			<LinearProgress
				indeterminate
				bind:closed={worksLoaded}
				aria-label="Загрузка..."
				slot="progress"
			/>
		</DataTable>
	</div>
	<div class="add-work-container">
		<Button
			variant="outlined"
			on:click={() => {
				createDialogOpen = true;
			}}
		>
			<Icon class="material-icons">add_circle_outlined</Icon>
			Добавить услугу
		</Button>
	</div>

	<Snackbar bind:this={snackbar} />

	<WorkCreateDialog {token} bind:open={createDialogOpen} onCreate={updateWorks} />
</div>

<style>
	.table-container {
		padding-top: 2rem;
	}

	.add-work-container {
		padding-top: 2rem;
	}
</style>
