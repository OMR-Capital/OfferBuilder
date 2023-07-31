<script lang="ts">
	import { OfferTplsAPI } from '$lib/backend/api/offer_tpls';
	import type { OfferTpl } from '$lib/backend/models/offer_tpls';
	import OfferTplCreateDialog from '$lib/components/admin/OfferTplCreateDialog.svelte';
	import CircularLoader from '$lib/components/common/CircularLoader.svelte';
	import IconButton from '$lib/components/common/IconButton.svelte';
	import Snackbar from '$lib/components/common/Snackbar.svelte';
	import Accordion, { Panel as AccordionPanel, Content, Header } from '@smui-extra/accordion';
	import Button, { Icon } from '@smui/button';
	import DataTable, { Body, Cell, Head, Row } from '@smui/data-table';
	import LinearProgress from '@smui/linear-progress';
	import { onMount } from 'svelte';
	import Panel from '../common/Panel.svelte';
	export let token: string;

	let snackbar: Snackbar;

	const offerTplsApi = new OfferTplsAPI(token);

	let offerTpls: OfferTpl[] = [];
	let offerTplsLoaded = false;

	async function updateOfferTpls() {
		offerTplsLoaded = false;
		const result = await offerTplsApi.getOfferTpls();
		if (result.ok) {
			offerTpls = result.value;
		} else {
			snackbar.show(result.error.message);
		}
		offerTplsLoaded = true;
	}

	let offerTplDeleting: Record<string, boolean> = {};
	$: {
		offerTpls.map((offerTpl) => {
			offerTplDeleting[offerTpl.offer_tpl_id] = false;
		});
	}

	async function deleteOfferTpl(offer_tpl_id: string) {
		offerTplDeleting[offer_tpl_id] = true;
		const result = await offerTplsApi.deleteOfferTpl(offer_tpl_id);
		if (result.ok) {
			updateOfferTpls();
		} else {
			snackbar.show(result.error.message);
		}
		offerTplDeleting[offer_tpl_id] = false;
	}

	let createDialogOpen = false;

	onMount(updateOfferTpls);
</script>

<Panel title="Шаблоны договоров">
	<Accordion>
		<AccordionPanel>
			<Header>
				<div class="info-header">
					<Icon class="material-icons">info_outlined</Icon>
					Инструкция по созданию шаблонов
				</div>
			</Header>
			<Content>
				<p>Для создания шаблона договора необходимо:</p>
				<ol>
					<li>
						Создать документ в формате <b>docx</b> с помощью Microsoft Word или аналогичной программы.
					</li>
					<li>
						В документе можно указать поля, которые будут заменены на введенные значения.
					</li>
					<li>
						Поля должны быть в формате <b>&lbrace;&lbrace; field_name &rbrace;&rbrace;</b>, где
						<b>field_name</b> - название поля. Доступные поля:
						<ul>
							<li>
								Название организации: <b>&lbrace;&lbrace; company.name &rbrace;&rbrace;</b>
							</li>
							<li>
								Контр-агент:
								<ol>
									<li>Полное название: <b>&lbrace;&lbrace; agent.fullname &rbrace;&rbrace;</b></li>
									<li>
										Сокращенное название: <b>&lbrace;&lbrace; agent.shortname &rbrace;&rbrace;</b>
									</li>
									<li>ИНН: <b>&lbrace;&lbrace; agent.inn &rbrace;&rbrace;</b></li>
									<li>ФИО директора: <b>&lbrace;&lbrace; agent.management &rbrace;&rbrace;</b></li>
								</ol>
							</li>
							<li>
								Тип предложения: <b>&lbrace;&lbrace; offerType &rbrace;&rbrace;</b>
							</li>
							<li>
								Данные коммерческого предложения: <b>&lbrace;&lbrace; offerData &rbrace;&rbrace;</b>

								Поля внутри строк предложения:
								<ul>
									<li>Порядковый номер: <b>&lbrace;&lbrace; item.num &rbrace;&rbrace;</b></li>
									<li>Название: <b>&lbrace;&lbrace; item.name &rbrace;&rbrace;</b></li>
									<li>
										Код ФККО (Только в КП на отходы): <b
											>&lbrace;&lbrace; item.name &rbrace;&rbrace;</b
										>
									</li>
									<li>Единица измерения: <b>&lbrace;&lbrace; item.unit &rbrace;&rbrace;</b></li>
									<li>Цена: <b>&lbrace;&lbrace; item.price &rbrace;&rbrace;</b></li>
									<li>Количество: <b>&lbrace;&lbrace; item.amount &rbrace;&rbrace;</b></li>
									<li>Сумма: <b>&lbrace;&lbrace; item.sum &rbrace;&rbrace;</b></li>
								</ul>
							</li>
                            <li>
                                Общая стоимость предложения: <b>&lbrace;&lbrace; offerTotal &rbrace;&rbrace;</b>
                            </li>
							<li>
								Автор документа: <b>&lbrace;&lbrace; author.name &rbrace;&rbrace;</b>
							</li>
                            <li>
								Дата создания: <b>&lbrace;&lbrace; date &rbrace;&rbrace;</b>
							</li>
						</ul>
					</li>
					<li>Сохранить документ.</li>
					<li>Загрузить документ в систему.</li>
				</ol>

				<p>После загрузки документа он будет доступен для выбора при создании договора.</p>

				<p>
					Вы можете использовать документы <b>"Пример - КП на отходы"</b> и <b>"Пример - Общее КП"</b> в качестве
					шаблоны, скопировав нужные части оттуда.
				</p>
			</Content>
		</AccordionPanel>
	</Accordion>
	<div class="table-container">
		<DataTable table$aria-label="Список шаблонов" style="width: 100%;">
			<Head>
				<Row>
					<Cell>ID</Cell>
					<Cell>Название</Cell>
					<Cell />
					<Cell />
				</Row>
			</Head>
			<Body>
				{#each offerTpls as offerTpl}
					<Row>
						<Cell>{offerTpl.offer_tpl_id}</Cell>
						<Cell style="width: 100%">{offerTpl.name}</Cell>
						<Cell>
							{#if offerTplDeleting[offerTpl.offer_tpl_id]}
								<CircularLoader size="small" />
							{:else}
								<IconButton onClick={() => deleteOfferTpl(offerTpl.offer_tpl_id)} icon="delete" />
							{/if}
						</Cell>
						<Cell>
							<IconButton
								href={offerTplsApi.getDownloadUrl(offerTpl.offer_tpl_id)}
								download={offerTpl.name + '.docx'}
								icon="download"
							/>
						</Cell>
					</Row>
				{/each}
			</Body>
			<LinearProgress
				indeterminate
				bind:closed={offerTplsLoaded}
				aria-label="Загрузка..."
				slot="progress"
			/>
		</DataTable>
	</div>
	<div class="add-offerTpl-container">
		<Button
			variant="outlined"
			on:click={() => {
				createDialogOpen = true;
			}}
		>
			<Icon class="material-icons">add_circle_outlined</Icon>
			Добавить шаблон
		</Button>
	</div>
</Panel>

<Snackbar bind:this={snackbar} />

<OfferTplCreateDialog {token} bind:open={createDialogOpen} onCreate={updateOfferTpls} />

<style>
	.info-header {
		display: flex;
		align-items: center;
	}
</style>
