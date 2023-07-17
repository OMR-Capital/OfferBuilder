import { browser } from '$app/environment';

/**
 * Set a cookie with a given name and value and expiration days.
 */
export function setCookie(name: string, value: any, expirationHours: number) {
	if (!browser) {
		return false;
    }

	const date = new Date();
	date.setTime(date.getTime() + expirationHours * 24 * 60 * 60 * 1000);
	const expires = 'expires=' + date.toUTCString();
	document.cookie = name + '=' + value + ';' + expires + ';path=/';
	return true;
}
