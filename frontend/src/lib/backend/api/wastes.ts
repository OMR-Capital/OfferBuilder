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

export class WastesAPI extends BaseAPI {
	async getWastes(
		pagination: PaginationParams = defaultPaginationParams
	): Promise<Result<WastesResponse>> {
		const url = `/wastes?${asUrlParams(pagination)}`;
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
