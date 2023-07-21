import type { Result } from './utils';
import { fetchApi, fetchFile } from './utils';

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

	async fetchFile(
		path: string,
		method: string,
		json?: object,
		headers: object = {}
	): Promise<Result<Blob>> {
		return await fetchFile(path, method, this.token, json, headers);
	}
}
