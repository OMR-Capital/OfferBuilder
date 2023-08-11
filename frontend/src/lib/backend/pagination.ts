export interface PaginationParams {
    limit: number;
    last: string | null;
}

export function asUrlParams(pagination: PaginationParams): string {
    if (pagination.last === null) {
        return `limit=${pagination.limit}`;
    }
    return `limit=${pagination.limit}&last=${pagination.last}`;
}

export const defaultPaginationParams = {
    limit: 1000,
    last: null,
}
