<script lang="ts">
	import { UserRole } from '$lib/backend/models/users';
	import { user } from '$lib/stores';
	import Card, { Content } from '@smui/card';
	import UsersPanel from '$lib/components/admin/UsersPanel.svelte';
	import CompaniesPanel from '$lib/components/admin/CompaniesPanel.svelte';
	import WastesPanel from '$lib/components/admin/WastesPanel.svelte';
	import WorksPanel from '$lib/components/admin/WorksPanel.svelte';
	import OfferTplsPanel from '$lib/components/admin/offer_tpls_panel/OfferTplsPanel.svelte';
	import OffersPanel from '$lib/components/admin/OffersPanel.svelte';

	export let data;
</script>

{#if $user.role == UserRole.Admin || $user.role == UserRole.Superuser}
    <div class="panels-container">
        <UsersPanel token={data.token} />
        <CompaniesPanel token={data.token} />
        <WastesPanel token={data.token} />
        <WorksPanel token={data.token} />
        <OfferTplsPanel token={data.token} />
        <OffersPanel token={data.token} />
    </div>
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