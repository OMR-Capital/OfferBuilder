import { BaseAPI } from "../base_api";
import type { User } from "../models/users";
import type { Result } from "../utils";

interface UserResponse {
	user: User;
}

interface UserUpdate {
	name?: string;
	login?: string;
}

export class UsersAPI extends BaseAPI {
	async getMyUser(): Promise<Result<User>> {
		const result = (await this.fetchApi('/users/me', 'GET')) as Result<UserResponse>;
		if (result.ok) {
			return { ok: true, value: result.value.user };
		}
		return result;
	}

	async updateMyUser(userData: UserUpdate): Promise<Result<User>> {
		const result = (await this.fetchApi('/users/me', 'PUT', userData)) as Result<UserResponse>;
		if (result.ok) {
			return { ok: true, value: result.value.user };
		}
		return result;
	}
}
