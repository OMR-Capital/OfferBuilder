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
	if (!/^(\d| )+$/.test(inn)) {
		return null;
	}
	return inn.replace(/ /g, '');
}
