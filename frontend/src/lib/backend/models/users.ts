export enum UserRole {
    Admin = 'admin',
    Employee = 'employee',
    Superuser = 'superuser',
}


export interface User {
    uid: string;
    name: string;
    login: string;
    role: UserRole;
}
