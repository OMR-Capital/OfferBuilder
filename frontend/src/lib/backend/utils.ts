const BACKEND_URL = '/api';

export class HTTPError {
	constructor(public message: string, public status: number) {}
}

export type Result<T> = { ok: true; value: T } | { ok: false; error: HTTPError };

interface AuthResponse {
	access_token: string;
}

/**
 * Authorize user via OAuth2
 */
export async function auth(username: string, password: string): Promise<{ token: string }> {
	const url = BACKEND_URL + '/auth/token';

	const formData = new FormData();
	formData.append('grant_type', '');
	formData.append('client_id', '');
	formData.append('client_secret', '');
	formData.append('username', username);
	formData.append('password', password);

	const response = await fetch(url, {
		method: 'POST',
		body: formData
	});

	if (response.status == 401) {
		throw new Error('Invalid username or password');
	} else if (response.status != 200) {
		throw new Error('Unknown error');
	}

	const result = (await response.json()) as AuthResponse;
	return { token: result.access_token };
}

/**
 * Fetch backend API with authorization token.
 */
export async function fetchApi(
	path: string,
	method: string,
	token: string,
	json?: object,
	headers: object = {}
): Promise<Result<object>> {
	const url = BACKEND_URL + path;

	const headers_ = {
		Authorization: 'Bearer ' + token,
		Accept: 'application/json',
		'Content-Type': 'application/json',
		...headers
	};

	const response = await fetch(url, {
		method,
		headers: headers_,
		body: json ? JSON.stringify(json) : undefined
	});

	if (response.status != 200) {
		return { ok: false, error: new HTTPError(response.statusText, response.status) };
	}
	const result = (await response.json()) as object;
	return { ok: true, value: result };
}
