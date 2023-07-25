import { BaseAPI } from '../base_api';
import type { OfferTpl } from '../models/offer_tpls';
import type { Result } from '../utils';

interface OfferTplResponse {
	offer_tpl: OfferTpl;
}

interface OfferTplsResponse {
	offer_tpls: OfferTpl[];
}

interface OfferTplCreate {
	name: string;
	offer_tpl_file: string;
}

export class OfferTplsAPI extends BaseAPI {
	async getOfferTpls(): Promise<Result<OfferTpl[]>> {
		const result = (await this.fetchApi('/offer_tpls', 'GET')) as Result<OfferTplsResponse>;
		if (result.ok) {
			return { ok: true, value: result.value.offer_tpls };
		}
		return result;
	}

	async deleteOfferTpl(offerTplId: string): Promise<Result<OfferTpl>> {
		const result = (await this.fetchApi(
			`/offer_tpls/${offerTplId}`,
			'DELETE'
		)) as Result<OfferTplResponse>;
		if (result.ok) {
			return { ok: true, value: result.value.offer_tpl };
		}
		return result;
	}

	async createOfferTpl(offerTplData: OfferTplCreate): Promise<Result<OfferTpl>> {
		const result = (await this.fetchApi(
			`/offer_tpls`,
			'POST',
			offerTplData
		)) as Result<OfferTplResponse>;
		if (result.ok) {
			return { ok: true, value: result.value.offer_tpl };
		}
		return result;
	}
	async downloadOfferTpl(offerTplId: string): Promise<Result<Blob>> {
		const result = await this.fetchFile(`/offer_tpls/${offerTplId}/download`, 'GET');
		return result;
	}

	async buildOffer(offerTplId: string, context: object): Promise<Result<Blob>> {
		const result = await this.fetchFile(`/offer_tpls/${offerTplId}/build`, 'POST', { context });
		if (result.ok) {
			return { ok: true, value: result.value };
		}
		return result;
	}
}
