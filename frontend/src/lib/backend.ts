const BACKEND_URL = '/api';

/**
 * Authorize user via OAuth2
 */
export async function auth(username: string, password: string): Promise<{ token: string }> {
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
	return { token: json.access_token };
}

/**
 * Fetch backend API with authorization token.
 */
export async function fetchApi(
	path: string,
	token: string,
    options: {
        method?: string;
        body?: Record<string, any>;
        headers?: Record<string, string>;
        formData?: boolean;
    } = {}
): Promise<any> {
	let url = BACKEND_URL + path;

	let headers = options.headers || {};
	headers['Authorization'] = 'Bearer ' + token;
	headers['Accept'] = 'application/json';

	let body;
	if (options.formData) {
		body = new FormData();
		for (let key in options.body) {
			body.append(key, options.body[key]);
		}
	} else {
		headers['Content-Type'] = 'application/json';
		body = JSON.stringify(options.body);
	}

	let response = await fetch(url, {
		method: options.method || 'GET',
		headers: headers,
		body: body
	});

	if (response.status == 401) {
		throw new Error('Unauthorized');
	} else if (response.status != 200) {
		throw new Error('Unknown error');
	}

	let json = await response.json();
	return json;
}
