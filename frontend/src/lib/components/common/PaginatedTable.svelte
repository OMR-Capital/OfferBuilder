<script lang="ts">
	import DataTable, { Pagination } from '@smui/data-table';
	import IconButton from '@smui/icon-button';
	import { onMount } from 'svelte';

	export let currentPage = 0;
	export let limit: number;
	export let last: string | null = null;
	export let updateItems: (limit: number, last: string | null) => Promise<string | null>;

	let pagesLasts: (string | null)[] = [null];

	export async function firstPage() {
		currentPage = 0;
		last = await updateItems(limit, null);
		pagesLasts = [null, last];
	}

	export async function nextPage() {
		currentPage++;
		last = await updateItems(limit, last);
		pagesLasts.push(last);
	}

	export async function prevPage() {
		if (currentPage === 1) {
			firstPage();
		} else if (currentPage > 1) {
			currentPage--;
			pagesLasts.pop();
			const prevLast = pagesLasts[pagesLasts.length - 2];
			last = await updateItems(limit, prevLast);
		}
	}

    export async function reloadPage() {
        const prevLast = pagesLasts[pagesLasts.length - 2];
        const newLast = await updateItems(limit, prevLast);
        last = newLast;
        pagesLasts[pagesLasts.length - 1] = newLast;
    }

	onMount(firstPage);
</script>

<DataTable table$aria-label="Todo list" style="width: 100%;">
	<slot name="head" />
	<slot name="body" />
	<slot name="progress" slot="progress" />

	<Pagination slot="paginate">
		<svelte:fragment slot="total">
			Страница: {currentPage + 1}
		</svelte:fragment>

		<IconButton
			class="material-icons"
			action="first-page"
			title="В начало"
			on:click={firstPage}
			disabled={currentPage === 0}>first_page</IconButton
		>
		<IconButton
			class="material-icons"
			action="prev-page"
			title="Назад"
			on:click={prevPage}
			disabled={currentPage === 0}>chevron_left</IconButton
		>
		<IconButton
			class="material-icons"
			action="next-page"
			title="Далее"
			on:click={nextPage}
			disabled={last == null}>chevron_right</IconButton
		>
	</Pagination>
</DataTable>
