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

interface WorksFilter {
	name?: string;
	name_contains?: string;
}

function filterToURLParams(filter: WorksFilter): string {
    const params = [];
    if (filter.name) {
        params.push(`name=${filter.name}`);
    }
    if (filter.name_contains) {
        params.push(`name_contains=${filter.name_contains}`);
    }
    return params.join('&');
}

export class WorksAPI extends BaseAPI {
	async getWorks(
		pagination: PaginationParams = defaultPaginationParams,
		filter: WorksFilter | null = null
	): Promise<Result<WorksResponse>> {
		let url = `/works?${asUrlParams(pagination)}`;
        if (filter) {
            url += `&${filterToURLParams(filter)}`;
        }
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
