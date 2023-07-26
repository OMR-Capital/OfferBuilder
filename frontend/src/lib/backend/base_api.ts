import type { Result } from './utils';
import { fetchApi, fetchFile } from './utils';
import { goto } from '$app/navigation';

export class BaseAPI {
    public baseUrl = '/api';
    
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
		const result = await fetchApi(path, method, this.token, json, headers);
		if (!result.ok && result.error.status == 401) {
			goto('/auth');
		}
		return result;
	}

	async fetchFile(
		path: string,
		method: string,
		json?: object,
		headers: object = {}
	): Promise<Result<Blob>> {
		const result = await fetchFile(path, method, this.token, json, headers);
		if (!result.ok && result.error.status == 401) {
			goto('/auth');
		}
		return result;
	}
}
