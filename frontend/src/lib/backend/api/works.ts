import { BaseAPI, type Result } from '../base_api';
import type { Work } from '../models/works';

interface WorkResponse {
	work: Work;
}

interface WorksResponse {
	works: Work[];
}

interface WorkCreate {
	name: string;
}

export class WorksAPI extends BaseAPI {
	async getWorks(): Promise<Result<Work[]>> {
		const result = (await this.fetchApi('/works', 'GET')) as Result<WorksResponse>;
		if (result.ok) {
			return { ok: true, value: result.value.works };
		}
		return result;
	}

	async createWork(workData: WorkCreate): Promise<Result<Work>> {
		const result = (await this.fetchApi('/works', 'POST', workData)) as Result<WorkResponse>;
		if (result.ok) {
			return { ok: true, value: result.value.work };
		}
		return result;
	}

	async deleteWork(work_id: string): Promise<Result<Work>> {
		const result = (await this.fetchApi(`/works/${work_id}`, 'DELETE')) as Result<WorkResponse>;
		if (result.ok) {
			return { ok: true, value: result.value.work };
		}
		return result;
	}
}
