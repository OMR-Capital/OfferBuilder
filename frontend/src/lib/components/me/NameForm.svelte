<script lang="ts">
	import { UsersAPI } from '$lib/backend/api/users';
	import CircularLoader from '$lib/components/common/CircularLoader.svelte';
	import IconButton from '$lib/components/common/IconButton.svelte';
	import { user } from '$lib/stores';
	import Textfield from '@smui/textfield';
	import HelperText from '@smui/textfield/helper-text';

	export let token: string;

	const userApi = new UsersAPI(token);

	let name = $user.name;
	let nameUpdated = false;
	let nameUpdating = false;
	let nameError = '';

	async function updateName() {
		if (name === $user.name) {
			return;
		}
		nameUpdating = true;
		const result = await userApi.updateMyUser({ name });
		if (!result.ok) {
			nameError = result.error.message;
		} else {
			$user = result.value;
			name = $user.name;
			nameUpdated = true;
		}
		nameUpdating = false;
	}
</script>

<div class="name-form-container">
    <form on:submit|preventDefault={updateName}>
        <Textfield
            style="width: 100%"
            type="text"
            input$autocomplete="name"
            bind:value={name}
        >
            <HelperText slot="helper" persistent>
                {#if nameError}
                    {nameError}
                {:else if name !== $user.name}
                    Нажмите кнопку, чтобы сохранить изменения
                {:else if nameUpdated}
                    Изменения сохранены
                {:else}
                    Вы можете изменить имя
                {/if}
            </HelperText>
            <svelte:fragment slot="trailingIcon">
                {#if name !== $user.name && !nameUpdating}
                    <IconButton type="submit" icon="check" />
                {:else if nameUpdating}
                    <CircularLoader size="small" />
                {/if}
            </svelte:fragment>
        </Textfield>
    </form>
</div>

<style>
    .name-form-container {
        width: 100%;
    }
</style>
