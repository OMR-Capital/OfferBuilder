import { fetchApi } from "./utils";

export class BaseAPI {
    private token: string;

    constructor(token: string) {
        this.token = token;
    }

    async fetchApi(
        path: string,
        options: {
            method?: string;
            body?: Record<string, any>;
            headers?: Record<string, string>;
            formData?: boolean;
        } = {}
    ): Promise<any> {
        return await fetchApi(path, this.token, options);
    }
}
