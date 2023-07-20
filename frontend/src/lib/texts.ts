import { UserRole } from '$lib/backend/models/users';

export function userRoleName(role: UserRole): string {
	switch (role) {
		case UserRole.Admin:
			return 'Администратор';
		case UserRole.Employee:
			return 'Сотрудник';
        default:
            return 'Неизвестно';
	}
}
