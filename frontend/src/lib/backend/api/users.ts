import { BaseAPI, type Result } from '../base_api';
import type { User } from '../models/users';
import { asUrlParams, defaultPaginationParams, type PaginationParams } from '../pagination';

interface UserResponse {
	user: User;
}

export interface UsersResponse {
	users: User[];
	last: string | null;
}

interface UserUpdate {
	name?: string;
	login?: string;
}

interface UserCreate {
	name: string;
	role: string;
}

interface UserWithPassword {
	user: User;
	password: string;
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

	async regenMyPassword(): Promise<Result<string>> {
		const result = (await this.fetchApi('/users/me/password', 'PATCH')) as Result<{
			password: string;
		}>;
		if (result.ok) {
			return { ok: true, value: result.value.password };
		}
		return result;
	}

	async getUsers(
		pagination: PaginationParams = defaultPaginationParams
	): Promise<Result<UsersResponse>> {
		const url = `/users?${asUrlParams(pagination)}`;
		return (await this.fetchApi(url, 'GET')) as Result<UsersResponse>;
	}

	async deleteUser(uid: string): Promise<Result<User>> {
		const result = (await this.fetchApi(`/users/${uid}`, 'DELETE')) as Result<UserResponse>;
		if (result.ok) {
			return { ok: true, value: result.value.user };
		}
		return result;
	}

	async createUser(userData: UserCreate): Promise<Result<UserWithPassword>> {
		const result = (await this.fetchApi('/users', 'POST', userData)) as Result<UserWithPassword>;
		if (result.ok) {
			return { ok: true, value: result.value };
		}
		return result;
	}
}
