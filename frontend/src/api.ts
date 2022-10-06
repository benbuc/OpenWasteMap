import axios from "axios";
import { apiUrl } from "@/env";
import {
  IUserProfile,
  IUserProfileUpdate,
  IUserProfileCreate,
  IWasteSample,
  IWasteSampleCreate,
  IWasteSampleImportExport,
} from "./interfaces";

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

export const api = {
  async logInGetToken(username: string, password: string) {
    const params = new URLSearchParams();
    params.append("username", username);
    params.append("password", password);

    return axios.post(`${apiUrl}/api/v1/login/access-token`, params);
  },
  async getMe(token: string) {
    return axios.get<IUserProfile>(
      `${apiUrl}/api/v1/users/me`,
      authHeaders(token)
    );
  },
  async updateMe(token: string, data: IUserProfileUpdate) {
    return axios.put<IUserProfile>(
      `${apiUrl}/api/v1/users/me`,
      data,
      authHeaders(token)
    );
  },
  async getUsers(token: string) {
    return axios.get<IUserProfile[]>(
      `${apiUrl}/api/v1/users`,
      authHeaders(token)
    );
  },
  async getAllUsers(token: string) {
    return axios.get<IUserProfile[]>(`${apiUrl}/api/v1/users`, {
      headers: authHeaders(token).headers,
      params: {
        limit: 0,
      },
    });
  },
  async updateUser(token: string, userId: number, data: IUserProfileUpdate) {
    return axios.put(
      `${apiUrl}/api/v1/users/${userId}`,
      data,
      authHeaders(token)
    );
  },
  async createUser(token: string, data: IUserProfileCreate) {
    return axios.post(`${apiUrl}/api/v1/users`, data, authHeaders(token));
  },
  async passwordRecovery(email: string) {
    return axios.post(`${apiUrl}/api/v1/password-recovery/${email}`);
  },
  async resetPassword(password: string, token: string) {
    return axios.post(`${apiUrl}/api/v1/reset-password`, {
      new_password: password,
      token,
    });
  },
  async verifyEmail(token: string) {
    return axios.post(`${apiUrl}/api/v1/verify-email`, {
      token,
    });
  },
  async resendVerification(token: string) {
    return axios.post(
      `${apiUrl}/api/v1/resend-verification`,
      null,
      authHeaders(token)
    );
  },
  getTilesEndpoint() {
    return `${apiUrl}/api/v1/tiles/{z}/{x}/{y}.png`;
  },
  async getWasteSamples(token: string) {
    return axios.get<IWasteSample[]>(
      `${apiUrl}/api/v1/waste-samples`,
      authHeaders(token)
    );
  },
  async getAllWasteSamples(token: string) {
    return axios.get<IWasteSample[]>(
      `${apiUrl}/api/v1/waste-samples/all`,
      authHeaders(token)
    );
  },
  async createWasteSample(token: string, data: IWasteSampleCreate) {
    return axios.post(
      `${apiUrl}/api/v1/waste-samples`,
      data,
      authHeaders(token)
    );
  },
  async createWasteSamplesBulk(
    token: string,
    data: IWasteSampleImportExport[]
  ) {
    return axios.post(
      `${apiUrl}/api/v1/waste-samples/bulk`,
      data,
      authHeaders(token)
    );
  },
};
