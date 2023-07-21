import { BaseAPI } from '../base_api';
import type { Waste } from '../models/wastes';
import type { Result } from '../utils';

interface WasteResponse {
	waste: Waste;
}

interface WastesResponse {
	wastes: Waste[];
}

interface WasteCreate {
	name: string;
	fkko_code: string;
}

export class WastesAPI extends BaseAPI {
	async getWastes(): Promise<Result<Waste[]>> {
		const result = (await this.fetchApi('/wastes', 'GET')) as Result<WastesResponse>;
		if (result.ok) {
			return { ok: true, value: result.value.wastes };
		}
		return result;
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
