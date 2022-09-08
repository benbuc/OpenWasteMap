import { IUserProfile, IWasteSample } from "@/interfaces";

export interface AdminState {
  users: IUserProfile[];
  waste_samples: IWasteSample[];
}
