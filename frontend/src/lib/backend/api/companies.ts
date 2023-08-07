import { BaseAPI, type Result } from '../base_api';
import type { Company } from '../models/companies';

interface CompanyResponse {
	company: Company;
}

interface CompaniesResponse {
	companies: Company[];
}

interface CompanyCreate {
	name: string;
}

export class CompaniesAPI extends BaseAPI {
	async getCompanies(): Promise<Result<Company[]>> {
		const result = (await this.fetchApi('/companies', 'GET')) as Result<CompaniesResponse>;
		if (result.ok) {
			return { ok: true, value: result.value.companies };
		}
		return result;
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
