<script lang="ts">
	import { UserRole } from '$lib/backend/models/users';
	import { user } from '$lib/stores';
	import Card, { Content } from '@smui/card';
	import UsersPanel from '../../../lib/components/admin/UsersPanel.svelte';

    export let data;
</script>

{#if $user.role == UserRole.Admin}
	<Card>
		<Content>
			<div class="panels-contatiner">
				<UsersPanel token={data.token}/>
			</div>
		</Content>
	</Card>
{:else}
	<Card>
		<Content>Доступ запрещен</Content>
	</Card>
{/if}
