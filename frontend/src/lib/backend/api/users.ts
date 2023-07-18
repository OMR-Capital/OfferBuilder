import { BaseAPI } from '../base_api';
import type { User } from '../models/users';

export class UsersAPI extends BaseAPI {
	async getMyUser(): Promise<User> {
		const userResponse = await this.fetchApi('/users/me');
		return userResponse.user;
	}
}
