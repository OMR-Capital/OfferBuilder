import { browser } from '$app/environment';

/**
 * Set a cookie with a given name and value and expiration days.
 */
export function setCookie(name: string, value: any, expirationMinutes: number) {
	if (!browser) {
		return false;
    }

	const date = new Date();
	date.setTime(date.getTime() + expirationMinutes * 60 * 1000);
	const expires = 'expires=' + date.toUTCString();
	document.cookie = name + '=' + value + ';' + expires + ';path=/';
	return true;
}
