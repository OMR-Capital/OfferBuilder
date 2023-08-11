import { BaseAPI, type Result } from '../base_api';
import { FileFormat } from '../models/docx';
import type { Offer } from '../models/offers';
import { asUrlParams, defaultPaginationParams, type PaginationParams } from '../pagination';

interface OfferResponse {
	offer: Offer;
}

export interface OffersResponse {
	offers: Offer[];
    last: string | null;
}

export class OffersAPI extends BaseAPI {
    async getOffers(
        pagination: PaginationParams = defaultPaginationParams
    ): Promise<Result<OffersResponse>> {
        const url = `/offers?${asUrlParams(pagination)}`;
		return (await this.fetchApi(url, 'GET')) as Result<OffersResponse>;
	}

	async deleteOffer(offerId: string): Promise<Result<Offer>> {
		const result = (await this.fetchApi(`/offers/${offerId}`, 'DELETE')) as Result<OfferResponse>;
		if (result.ok) {
			return { ok: true, value: result.value.offer };
		}
		return result;
	}

	getDownloadUrl(offerId: string, fileFormat: FileFormat = FileFormat.docx): string {
		return `${BaseAPI.baseUrl}/offers/${offerId}/download?file_format=${fileFormat}`;
	}
}
