import { BaseAPI, type Result } from '../base_api';
import type { Work } from '../models/works';
import { asUrlParams, defaultPaginationParams, type PaginationParams } from '../pagination';

interface WorkResponse {
	work: Work;
}

interface WorksResponse {
    works: Work[];
    last: string | null;
}

interface WorkCreate {
	name: string;
}

export class WorksAPI extends BaseAPI {
    async getWorks(
		pagination: PaginationParams = defaultPaginationParams
    ): Promise<Result<WorksResponse>> {
		const url = `/works?${asUrlParams(pagination)}`;
	    return (await this.fetchApi(url, 'GET')) as Result<WorksResponse>;
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
