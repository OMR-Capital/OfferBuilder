import type { Agent } from '$lib/backend/models/agents';
import type { Company } from '$lib/backend/models/companies';

export enum OfferType {
	Wastes = 'На отходы',
	General = 'Общее'
}

export enum Unit {
	CubeMetres = 'м3',
	Tonnes = 'тн',
	Pieces = 'шт'
}

export interface WasteRow {
	name: string;
	fkko_code: string;
	unit: Unit;
	price: number;
	amount: number;
	sum: number;
}

export interface GeneralRow {
	name: string;
	unit: Unit;
	price: number;
	amount: number;
	sum: number;
}

export interface OfferContext {
	offerType?: OfferType;
	agent?: Agent;
	offerData?: WasteRow[] | GeneralRow[];
	company?: Company;
	date?: string;
}
