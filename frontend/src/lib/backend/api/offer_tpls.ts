import { BaseAPI, type Result } from '../base_api';
import { FileFormat } from '../models/docx';
import type { OfferTpl } from '../models/offer_tpls';
import type { Offer } from '../models/offers';
import { asUrlParams, defaultPaginationParams, type PaginationParams } from '../pagination';

interface OfferTplResponse {
	offer_tpl: OfferTpl;
}

export interface OfferTplsResponse {
	offer_tpls: OfferTpl[];
    last: string | null;
}

interface OfferTplCreate {
	name: string;
	offer_tpl_file: string;
}

interface BuiltOfferResponse {
	offer: Offer;
}

export class OfferTplsAPI extends BaseAPI {
    async getOfferTpls(
        pagination: PaginationParams = defaultPaginationParams
    ): Promise<Result<OfferTplsResponse>> {
        const url = `/offer_tpls?${asUrlParams(pagination)}`;
		return (await this.fetchApi(url, 'GET')) as Result<OfferTplsResponse>;
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

	async buildOffer(offerTplId: string, context: object): Promise<Result<Offer>> {
		const result = (await this.fetchApi(`/offer_tpls/${offerTplId}/build`, 'POST', {
			context
		})) as Result<BuiltOfferResponse>;
		if (result.ok) {
			return { ok: true, value: result.value.offer };
		}
		return result;
	}

	getDownloadUrl(offerTplId: string, filFormat: FileFormat = FileFormat.docx): string {
		return `${BaseAPI.baseUrl}/offer_tpls/${offerTplId}/download?format=${filFormat}`;
	}
}
