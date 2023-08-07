import { goto } from '$app/navigation';

export class HTTPError {
	constructor(public message: string, public status: number) {}
}

export type Result<T> = { ok: true; value: T } | { ok: false; error: HTTPError };

export interface AuthResponse {
	access_token: string;
}

export class BaseAPI {
	public static baseUrl = '/api';

	private token: string;

	constructor(token: string) {
		this.token = token;
	}

	async fetchApi(
		path: string,
		method: string,
		json?: object,
		headers: object = {}
	): Promise<Result<object>> {
		const url = BaseAPI.baseUrl + path;

		const headers_ = {
			Authorization: 'Bearer ' + this.token,
			Accept: 'application/json',
			'Content-Type': 'application/json',
			...headers
		};

		const response = await fetch(url, {
			method,
			headers: headers_,
			body: json ? JSON.stringify(json) : undefined
		});

		let result: Result<object>;
		if (response.status != 200) {
			result = { ok: false, error: new HTTPError(response.statusText, response.status) };
		} else {
			const data = (await response.json()) as object;
			result = { ok: true, value: data };
		}

		if (!result.ok && result.error.status == 401) {
			goto('/auth');
		}
		return result;
	}

	static async auth(username: string, password: string): Promise<{ token: string }> {
		const url = BaseAPI.baseUrl + '/auth/token';

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
}
