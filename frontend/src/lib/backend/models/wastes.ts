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

export function normalizeName(name: string): string {
	return name
		.toLowerCase()
		.replace(/[^\w а-яё]/g, ' ')
}

export function normalizeFKKOCode(fkko_code: string): string {
    return fkko_code.replace(/ /g, '');
}
