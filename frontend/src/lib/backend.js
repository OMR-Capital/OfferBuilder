const BACKEND_URL = '/api';

/**
 * @type {string | null}
 */
let authToken = null;

/**
 * Set auth token.
 *
 * @param {string} token
 */
export function setToken(token) {
	authToken = token;
}

/**
 * Get auth token.
 *
 * @returns {string | null}
 */
export function getToken() {
	return authToken;
}

/**
 * Send request with auth token.
 *
 * @param {string} url
 * @param {object} options
 * @param {string} options.method
 * @param {BodyInit} options.body
 * @param {HeadersInit} options.headers
 */
export async function request(url, options) {
	let token = getToken();
	if (!token) {
		throw new Error('No auth token');
	}

	options.headers = options.headers || {};
	// @ts-ignore
	options.headers['Authorization'] = 'Bearer ' + token;

	let response = await fetch(url, {
		method: options.method,
		body: options.body,
		headers: options.headers
	});
	return response;
}

/**
 * Authorize user via OAuth2
 *
 * @param {string} username
 * @param {string} password
 *
 * @returns {Promise<{ token: string }>}
 */
export async function auth(username, password) {
	let url = BACKEND_URL + '/auth/token';

	let formData = new FormData();
	formData.append('grant_type', '');
	formData.append('client_id', '');
	formData.append('client_secret', '');
	formData.append('username', username);
	formData.append('password', password);

	let response = await fetch(url, {
		method: 'POST',
		body: formData
    });

    if (response.status == 401) {
        throw new Error('Invalid username or password');
    } else if (response.status != 200) {
        throw new Error('Unknown error');
    }

	let json = await response.json();
	/**
	 * @type {string}
	 */
	let token = json.access_token;
	setToken(token);

	return { token };
}
