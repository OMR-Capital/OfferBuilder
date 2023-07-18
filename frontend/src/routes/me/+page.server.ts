import { redirect } from '@sveltejs/kit';

export async function load({ cookies }) {
	const token = cookies.get('token');
	if (!token) {
		throw redirect(307, '/auth');
	}
	return {
		token: token
	};
}
