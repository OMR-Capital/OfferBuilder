export interface Agent {
	fullname: string;
	shortname: string;
	inn: string;
	management: string;
}

/**
 * INN should be an any combination of numbers and spaces.
 * Spaces will be removed.
 */
export function normalizeINN(inn: string): string | null {
    inn = inn.replace(/ /g, '');
	if (!/^\d{10}|\d{12}$/.test(inn)) {
		return null;
    }
    return inn;
}
