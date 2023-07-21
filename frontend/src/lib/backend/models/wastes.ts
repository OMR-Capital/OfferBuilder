export interface Waste {
	waste_id: string;
	name: string;
	fkko_code: string;
}

/**
 * FKKO code should be an any combination of numbers and spaces
 */
export function validateFKKOCode(fkko_code: string): boolean {
	return /^(\d| )+$/.test(fkko_code);
}
