const BACKEND_URL = '/api';


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
	return { token };
}


/**
 * Fetch backend API with authorization token.
 *
 * @param {string} path - relative API endpoint path
 * @param {string} token - Authorization token
 * @param {object} [options] - fetch options
 * @param {string} [options.method]
 * @param {Record<string, any>} [options.body]
 * @param {Record<string, string>} [options.headers]
 * @param {boolean} [options.json]
 * @param {boolean} [options.formData]
 * @param {boolean} [options.raw]
 */
export async function fetchApi(path, token, options = {}) {
    let url = BACKEND_URL + path;

    let headers = options.headers || {};
    headers['Authorization'] = 'Bearer ' + token;
    headers['Accept'] = 'application/json';

    let body;
    if (options.formData ) {
        body = new FormData();
        for (let key in options.body) {
            body.append(key, options.body[key]);
        }
    } else if (options.json) {
        headers['Content-Type'] = 'application/json';
        body = JSON.stringify(options.body);
    }

    let response = await fetch(url, {
        method: options.method || 'GET',
        headers: headers,
        body: body,
    });

    if (response.status == 401) {
        throw new Error('Unauthorized');
    } else if (response.status != 200) {
        throw new Error('Unknown error');
    }

    if (options.raw) {
        return response;
    }

    let json = await response.json();
    return json;
}
