<script>
	import Textfield from '@smui/textfield';
	import Button, { Label } from '@smui/button';
	import Card, { Content } from '@smui/card';
	import { auth } from '$lib/backend';

	let username = '';
	let password = '';
	let authFailed = false;

	async function login() {
		const token = await auth(username, password).catch(() => {
			authFailed = true;
		});
		if (token) {
            authFailed = false;
            document.cookie = `token=${token}; path=/`;
			window.location.href = '/me';
		} else {
            authFailed = true;
        }
	}
</script>

<div class="auth-container">
	<Card padded>
		<Content>
			<div class="auth-content">
				<div class="auth-content__item auth-title">
					<h6>Авторизация</h6>
				</div>
				<div class="auth-content__item">
					<Textfield label="Логин" bind:value={username} style="width: 100%;" />
				</div>
				<div class="auth-content__item">
					<Textfield label="Пароль" type="password" bind:value={password} style="width: 100%;" />
				</div>
				<div class="auth-content__item">
					<Button variant="outlined" on:click={login} style="width: 100%;">
						<Label>Войти</Label>
					</Button>
				</div>
				{#if authFailed}
					<div class="auth-content__item">
						<p style="color: red;">Неверный логин или пароль</p>
					</div>
				{/if}
			</div>
		</Content>
	</Card>
</div>

<style>
	.auth-container {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100vh;
	}

	.auth-title {
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.auth-content {
		display: flex;
		flex-direction: column;
		align-items: center;
		width: min(20rem, 100vw);
	}

	.auth-content__item {
		margin-bottom: 2rem;
		width: 100%;
	}

	.auth-content__item:last-child {
		margin-bottom: 0;
	}
</style>
