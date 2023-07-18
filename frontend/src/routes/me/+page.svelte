<script lang="ts">
	import { UsersAPI } from '$lib/backend/api/users.js';
	import Card, { Content } from '@smui/card';

	export let data;

    const usersApi = new UsersAPI(data.token);
</script>

<div class="user-container">
	<Card padded>
		<Content>
			<div class="user-content">
				{#await usersApi.getMyUser()}
                <div class="user-content__item">
                    <p>Загрузка...</p>
                </div>
				{:then user}
                    <div class="user-content__item user-title">
                        <h6>{user.name}</h6>
                    </div>
                    <div class="user-content__item">
                        <p>Роль: {user.role}</p>
                    </div>
                    <div class="user-content__item">
                        <p>Логин: {user.uid}</p>
                    </div>
				{:catch error}
					<div class="user-content__item">
						<p>{error}</p>
					</div>
				{/await}
			</div>
		</Content>
	</Card>
</div>

<style>
	.user-container {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100vh;
	}

	.user-title {
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.user-content {
		display: flex;
		flex-direction: column;
		align-items: center;
		width: min(20rem, 100vw);
	}

	.user-content__item {
		margin-bottom: 2rem;
		width: 100%;
	}

	.user-content__item:last-child {
		margin-bottom: 0;
	}
</style>
