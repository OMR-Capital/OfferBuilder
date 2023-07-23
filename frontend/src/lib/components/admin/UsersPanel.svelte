<script lang="ts">
	import { UsersAPI } from '$lib/backend/api/users';
	import type { User } from '$lib/backend/models/users';
	import UserCreateDialog from '$lib/components/admin/UserCreateDialog.svelte';
	import CircularLoader from '$lib/components/common/CircularLoader.svelte';
	import IconButton from '$lib/components/common/IconButton.svelte';
	import Snackbar from '$lib/components/common/Snackbar.svelte';
	import { userRoleName } from '$lib/texts';
	import Button, { Icon } from '@smui/button';
	import DataTable, { Body, Cell, Head, Row } from '@smui/data-table';
	import LinearProgress from '@smui/linear-progress';
	import { onMount } from 'svelte';
	import Panel from '../common/Panel.svelte';

	export let token: string;

	let snackbar: Snackbar;

	const usersApi = new UsersAPI(token);

	let users: User[] = [];
	let usersLoaded = false;

	async function updateUsers() {
		usersLoaded = false;
		const result = await usersApi.getUsers();
		if (result.ok) {
			users = result.value;
		} else {
			snackbar.show(result.error.message);
		}
		usersLoaded = true;
	}

	let userDeleting: Record<string, boolean> = {};
	$: {
		users.map((user) => {
			userDeleting[user.uid] = false;
		});
	}

	async function deleteUser(uid: string) {
		userDeleting[uid] = true;
		const result = await usersApi.deleteUser(uid);
		if (result.ok) {
			updateUsers();
		} else {
			snackbar.show(result.error.message);
		}
		userDeleting[uid] = false;
	}

	let createDialogOpen = false;

	onMount(updateUsers);
</script>

<Panel title="Пользователи">
	<div class="table-container">
		<DataTable table$aria-label="Список пользователей" style="width: 100%;">
			<Head>
				<Row>
					<Cell>ID</Cell>
					<Cell>Имя</Cell>
					<Cell>Логин</Cell>
					<Cell>Роль</Cell>
					<Cell />
				</Row>
			</Head>
			<Body>
				{#each users as user}
					<Row>
						<Cell>{user.uid}</Cell>
						<Cell style="width: 100%">{user.name}</Cell>
						<Cell>{user.login}</Cell>
						<Cell>{userRoleName(user.role)}</Cell>
						<Cell>
							{#if userDeleting[user.uid]}
								<CircularLoader size="small" />
							{:else}
								<IconButton onClick={() => deleteUser(user.uid)} icon="delete" />
							{/if}
						</Cell>
					</Row>
				{/each}
			</Body>
			<LinearProgress
				indeterminate
				bind:closed={usersLoaded}
				aria-label="Загрузка..."
				slot="progress"
			/>
		</DataTable>
	</div>
	<div class="add-user-container">
		<Button
			variant="outlined"
			on:click={() => {
				createDialogOpen = true;
			}}
		>
			<Icon class="material-icons">add_circle_outlined</Icon>
			Добавить пользователя
		</Button>
	</div>
</Panel>

<Snackbar bind:this={snackbar} />

<UserCreateDialog {token} bind:open={createDialogOpen} onCreate={updateUsers} />
