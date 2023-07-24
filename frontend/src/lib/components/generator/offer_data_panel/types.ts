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

export interface  GeneralRow {
    name: string;
    unit: Unit;
    price: number;
    amount: number;
    sum: number;
}
