import type { Result } from './utils';
import { fetchApi } from './utils';

export class BaseAPI {
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
		return await fetchApi(path, method, this.token, json, headers);
	}
}
