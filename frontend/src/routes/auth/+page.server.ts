import { env } from '$env/dynamic/private';

export async function load() {
    const tokenExpireMinutes = env['ACCESS_TOKEN_EXPIRE_MINUTES'];
	return {
		tokenExpireMinutes: tokenExpireMinutes ? parseInt(tokenExpireMinutes) : 60,
	};
}
