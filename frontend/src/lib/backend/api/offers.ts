import { BaseAPI, type Result } from '../base_api';
import { FileFormat } from '../models/docx';
import type { Offer } from '../models/offers';

interface OfferResponse {
	offer: Offer;
}

interface OffersResponse {
	offers: Offer[];
}

export class OffersAPI extends BaseAPI {
	async getOffers(): Promise<Result<Offer[]>> {
		const result = (await this.fetchApi('/offers', 'GET')) as Result<OffersResponse>;
		if (result.ok) {
			return { ok: true, value: result.value.offers };
		}
		return result;
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
