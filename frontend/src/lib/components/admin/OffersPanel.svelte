<script lang="ts">
	import { OffersAPI } from '$lib/backend/api/offers';
	import { FileFormat } from '$lib/backend/models/docx';
	import type { Offer } from '$lib/backend/models/offers';
	import IconButton from '$lib/components/common/IconButton.svelte';
	import PaginatedTable from '$lib/components/common/PaginatedTable.svelte';
	import Snackbar from '$lib/components/common/Snackbar.svelte';
	import { Body, Cell, Head, Row } from '@smui/data-table';
	import LinearProgress from '@smui/linear-progress';
	import { onMount } from 'svelte';
	import Panel from '../common/Panel.svelte';

	export let token: string;

	let snackbar: Snackbar;

	const offersApi = new OffersAPI(token);

	let offers: Offer[] = [];
	let offersLoaded = false;

	const limit = 10;
	let last: string | null = null;
	let table: PaginatedTable;

	async function updateOffers(limit: number, last: string | null): Promise<string | null> {
		offersLoaded = false;
		const result = await offersApi.getOffers({ limit, last });
		offersLoaded = true;
		if (result.ok) {
			offers = result.value.offers;
			return result.value.last;
		} else {
			snackbar.show(result.error.message);
		}
		return null;
	}

	function getOfferDate(offer: Offer): string {
		const date = new Date(offer.created_at);
		return `${date.toLocaleDateString('ru-RU')} ${date.toLocaleTimeString('ru-RU')}`;
	}

	onMount(async () => {
		await table.firstPage();
	});
</script>

<Panel title="Созданные КП">
	<div class="table-container">
		<PaginatedTable bind:this={table} {limit} bind:last updateItems={updateOffers}>
			<Head slot="head">
				<Row>
					<Cell>ID</Cell>
					<Cell>Шаблон</Cell>
					<Cell>Дата создания</Cell>
					<Cell>Сотрудник</Cell>
					<Cell />
					<Cell />
				</Row>
			</Head>
			<Body slot="body">
				{#each offers as offer}
					<Row>
						<Cell>{offer.offer_id}</Cell>
						<Cell style="width: 100%;">{offer.name}</Cell>
						<Cell>{getOfferDate(offer)}</Cell>
						<Cell>{offer.created_by}</Cell>
						<Cell>
							<IconButton
								href={offersApi.getDownloadUrl(offer.offer_id)}
								download={offer.offer_id + '.docx'}
								icon="description"
							/>
						</Cell>
                        <Cell>
							<IconButton
								href={offersApi.getDownloadUrl(offer.offer_id, FileFormat.pdf)}
								download={offer.offer_id + '.pdf'}
								icon="picture_as_pdf"
							/>
						</Cell>
					</Row>
				{/each}
			</Body>
			<LinearProgress
				indeterminate
				bind:closed={offersLoaded}
				aria-label="Загрузка..."
				slot="progress"
			/>
		</PaginatedTable>
	</div>
</Panel>

<Snackbar bind:this={snackbar} />
