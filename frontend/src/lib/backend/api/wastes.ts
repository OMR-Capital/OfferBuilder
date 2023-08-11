import { BaseAPI, type Result } from '../base_api';
import type { Waste } from '../models/wastes';
import { asUrlParams, defaultPaginationParams, type PaginationParams } from '../pagination';

interface WasteResponse {
	waste: Waste;
}

export interface WastesResponse {
	wastes: Waste[];
	last: string | null;
}

interface WasteCreate {
	name: string;
	fkko_code: string;
}

interface WastesFilter {
	name?: string;
	name_contains?: string;
	fkko_code?: string;
	fkko_code_prefix?: string;
}

function filterToURLParams(filter: WastesFilter): string {
	const params = [];
	if (filter.name) {
		params.push(`name=${filter.name}`);
	}
	if (filter.name_contains) {
		params.push(`name_contains=${filter.name_contains}`);
	}
	if (filter.fkko_code) {
		params.push(`fkko_code=${filter.fkko_code}`);
	}
	if (filter.fkko_code_prefix) {
		params.push(`fkko_code_prefix=${filter.fkko_code_prefix}`);
	}
	return params.join('&');
}

export class WastesAPI extends BaseAPI {
	async getWastes(
		pagination: PaginationParams = defaultPaginationParams,
		filter: WastesFilter | null = null
	): Promise<Result<WastesResponse>> {
		let url = `/wastes?${asUrlParams(pagination)}`;
		if (filter) {
			url += `&${filterToURLParams(filter)}`;
		}
		return (await this.fetchApi(url, 'GET')) as Result<WastesResponse>;
	}

	async createWaste(wasteData: WasteCreate): Promise<Result<Waste>> {
		const result = (await this.fetchApi('/wastes', 'POST', wasteData)) as Result<WasteResponse>;
		if (result.ok) {
			return { ok: true, value: result.value.waste };
		}
		return result;
	}

	async deleteWaste(waste_id: string): Promise<Result<Waste>> {
		const result = (await this.fetchApi(`/wastes/${waste_id}`, 'DELETE')) as Result<WasteResponse>;
		if (result.ok) {
			return { ok: true, value: result.value.waste };
		}
		return result;
	}
}
