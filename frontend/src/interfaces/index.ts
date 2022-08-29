export interface IUserProfile {
    email: string;
    nickname: string;
    is_active: boolean;
    is_superuser: boolean;
    full_name: string;
    id: number;
}

export interface IUserProfileUpdate {
    email?: string;
    nickname?: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface IUserProfileCreate {
    email: string;
    nickname: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface IWasteSample {
    waste_level: number;
    latitude: number;
    longitude: number;
    id: number;
    owner_id: number;
}

export interface IWasteSampleUpdate {
    waste_level?: number;
    latitude?: number;
    longitude?: number;
}

export interface IWasteSampleCreate {
    waste_level: number;
    latitude: number;
    longitude: number;
}

export interface IWasteSampleCreateBulk {
    waste_level: number;
    latitude: number;
    longitude: number;
    owner_nickname: string;
    sampling_date: string;
}