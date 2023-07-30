import { BaseAPI } from '../base_api';
import { FileFormat } from '../models/docx';
import type { Offer } from '../models/offers';
import type { Result } from '../utils';

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

	async downloadOffer(offerId: string): Promise<Result<Blob>> {
		const result = await this.fetchFile(`/offers/${offerId}/download`, 'GET');
		return result;
	}

	getDownloadUrl(offerId: string, fileFormat: FileFormat = FileFormat.docx): string {
		return `${this.baseUrl}/offers/${offerId}/download?file_format=${fileFormat}`;
	}
}
