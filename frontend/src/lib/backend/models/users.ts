export enum UserRole {
    Admin = 'admin',
    Employee = 'employee',
}


export interface User {
    uid: string;
    name: string;
    login: string;
    role: UserRole;
}
