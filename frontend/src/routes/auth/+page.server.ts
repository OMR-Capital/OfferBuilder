export async function load() {
	const tokenExpireMinutes = process.env.ACCESS_TOKEN_EXPIRE_MINUTES;
	return {
		tokenExpireMinutes: tokenExpireMinutes ? parseInt(tokenExpireMinutes) : 60
	};
}
