import type { Agent } from '$lib/backend/models/agents';
import type { Company } from '$lib/backend/models/companies';
import type { User } from '$lib/backend/models/users';

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
	num: number;
	name: string;
	fkko_code: string;
	unit: Unit;
	price: number;
	amount: number;
	sum: number;
}

export interface GeneralRow {
	num: number;
	name: string;
	unit: Unit;
	price: number;
	amount: number;
	sum: number;
}

export interface OfferContext {
    author?: User;
	agent?: Agent;
	offerType?: OfferType;
    offerData?: WasteRow[] | GeneralRow[];
    offerTotal?: number;
	company?: Company;
    date?: string;
}
