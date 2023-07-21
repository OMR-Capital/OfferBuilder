<script lang="ts">
	import { UserRole } from '$lib/backend/models/users';
	import { user } from '$lib/stores';
	import Card, { Content } from '@smui/card';
	import UsersPanel from '$lib/components/admin/UsersPanel.svelte';
	import CompaniesPanel from '$lib/components/admin/CompaniesPanel.svelte';
	import WastesPanel from '$lib/components/admin/WastesPanel.svelte';
	import WorksPanel from '$lib/components/admin/WorksPanel.svelte';

	export let data;
</script>

{#if $user.role == UserRole.Admin}
    <Card>
        <Content>
            <div class="panels-container">
                <UsersPanel token={data.token} />
                <CompaniesPanel token={data.token} />
                <WastesPanel token={data.token} />
                <WorksPanel token={data.token} />
            </div>
        </Content>
    </Card>
{:else}
    <Card>
        <Content>Доступ запрещен</Content>
    </Card>
{/if}

<style>
    .panels-container {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        gap: 4rem;
    }
</style>