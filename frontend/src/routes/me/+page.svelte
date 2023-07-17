<script>
	import Card, { Content } from '@smui/card';

	export let data;
</script>

<div class="user-container">
	<Card padded>
		<Content>
			<div class="user-content">
				<div class="user-content__item user-title">
					<h6>User</h6>
				</div>
				<div class="user-content__item">
					<p>{data.token}</p>
				</div>
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
