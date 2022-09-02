import { api } from "@/api";
import { ActionContext } from "vuex";
import {
  IUserProfileCreate,
  IUserProfileUpdate,
  IWasteSampleImportExport,
} from "@/interfaces";
import { State } from "../state";
import { AdminState } from "./state";
import { getStoreAccessors } from "typesafe-vuex";
import {
  commitSetUsers,
  commitSetUser,
  commitSetWasteSamples,
} from "./mutations";
import { dispatchCheckApiError } from "../main/actions";
import {
  commitAddNotification,
  commitRemoveNotification,
} from "../main/mutations";
import { AxiosError } from "axios";

type MainContext = ActionContext<AdminState, State>;

export const actions = {
  async actionGetUsers(context: MainContext) {
    try {
      const response = await api.getUsers(context.rootState.main.token);
      if (response) {
        commitSetUsers(context, response.data);
      }
    } catch (error) {
      await dispatchCheckApiError(context, error as AxiosError);
    }
  },
  async actionExportAllUsers(context: MainContext) {
    try {
      const response = await api.getAllUsers(context.rootState.main.token);
      if (response) {
        const data = JSON.stringify(response.data);
        const blob = new Blob([data], { type: "text/json" });
        const objectUrl = URL.createObjectURL(blob);
        const a = document.createElement("a") as HTMLAnchorElement;

        a.href = objectUrl;
        a.download = "users.json";
        document.body.appendChild(a);
        a.click();

        document.body.removeChild(a);
        URL.revokeObjectURL(objectUrl);
      }
    } catch (error) {
      await dispatchCheckApiError(context, error as AxiosError);
    }
  },
  async actionUpdateUser(
    context: MainContext,
    payload: { id: number; user: IUserProfileUpdate }
  ) {
    try {
      const loadingNotification = { content: "saving", showProgress: true };
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.updateUser(
            context.rootState.main.token,
            payload.id,
            payload.user
          ),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          ),
        ])
      )[0];
      commitSetUser(context, response.data);
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: "User successfully updated",
        color: "success",
      });
    } catch (error) {
      await dispatchCheckApiError(context, error as AxiosError);
    }
  },
  async actionCreateUser(context: MainContext, payload: IUserProfileCreate) {
    try {
      const loadingNotification = { content: "saving", showProgress: true };
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.createUser(context.rootState.main.token, payload),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          ),
        ])
      )[0];
      commitSetUser(context, response.data);
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: "User successfully created",
        color: "success",
      });
    } catch (error) {
      const aError = error as AxiosError;
      if (aError.response!.status === 400) {
        return aError;
      }
      await dispatchCheckApiError(context, aError);
    }
  },
  async actionGetWasteSamples(context: MainContext) {
    try {
      const response = await api.getWasteSamples(context.rootState.main.token);
      if (response) {
        commitSetWasteSamples(context, response.data);
      }
    } catch (error) {
      await dispatchCheckApiError(context, error as AxiosError);
    }
  },
  async actionExportAllWasteSamples(context: MainContext) {
    try {
      const response = await api.getAllWasteSamples(
        context.rootState.main.token
      );
      if (response) {
        const data = JSON.stringify(response.data);
        const blob = new Blob([data], { type: "text/json" });
        const objectUrl = URL.createObjectURL(blob);
        const a = document.createElement("a") as HTMLAnchorElement;

        a.href = objectUrl;
        a.download = "wastesamples.json";
        document.body.appendChild(a);
        a.click();

        document.body.removeChild(a);
        URL.revokeObjectURL(objectUrl);
      }
    } catch (error) {
      await dispatchCheckApiError(context, error as AxiosError);
    }
  },
  async actionCreateWasteSamplesBulk(
    context: MainContext,
    payload: IWasteSampleImportExport[]
  ) {
    try {
      const loadingNotification = { content: "uploading", showProgress: true };
      commitAddNotification(context, loadingNotification);
      const response = await api.createWasteSamplesBulk(
        context.rootState.main.token,
        payload
      );
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: "Successfully imported",
        color: "success",
      });
    } catch (error) {
      await dispatchCheckApiError(context, error as AxiosError);
    }
  },
};

const { dispatch } = getStoreAccessors<AdminState, State>("");

export const dispatchCreateUser = dispatch(actions.actionCreateUser);
export const dispatchGetUsers = dispatch(actions.actionGetUsers);
export const dispatchExportAllUsers = dispatch(actions.actionExportAllUsers);
export const dispatchUpdateUser = dispatch(actions.actionUpdateUser);
export const dispatchGetWasteSamples = dispatch(actions.actionGetWasteSamples);
export const dispatchExportAllWasteSamples = dispatch(
  actions.actionExportAllWasteSamples
);
export const dispatchCreateWasteSamplesBulk = dispatch(
  actions.actionCreateWasteSamplesBulk
);
