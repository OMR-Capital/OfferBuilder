import { BaseAPI, type Result } from '../base_api';
import type { Company } from '../models/companies';
import { asUrlParams, defaultPaginationParams, type PaginationParams } from '../pagination';

interface CompanyResponse {
	company: Company;
}

export interface CompaniesResponse {
	companies: Company[];
	last: string | null;
}

interface CompanyCreate {
	name: string;
}

export class CompaniesAPI extends BaseAPI {
	async getCompanies(
		pagination: PaginationParams = defaultPaginationParams
	): Promise<Result<CompaniesResponse>> {
		const url = `/companies?${asUrlParams(pagination)}`;
		return (await this.fetchApi(url, 'GET')) as Result<CompaniesResponse>;
	}

	async createCompany(companyData: CompanyCreate): Promise<Result<Company>> {
		const result = (await this.fetchApi(
			'/companies',
			'POST',
			companyData
		)) as Result<CompanyResponse>;
		if (result.ok) {
			return { ok: true, value: result.value.company };
		}
		return result;
	}

	async deleteCompany(companyId: string): Promise<Result<Company>> {
		const result = (await this.fetchApi(
			`/companies/${companyId}`,
			'DELETE'
		)) as Result<CompanyResponse>;
		if (result.ok) {
			return { ok: true, value: result.value.company };
		}
		return result;
	}
}
