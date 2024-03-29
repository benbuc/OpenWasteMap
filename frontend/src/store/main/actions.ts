import { api } from "@/api";
import { IWasteSampleCreate } from "@/interfaces";
import router from "@/router/routes";
import { getLocalToken, removeLocalToken, saveLocalToken } from "@/utils";
import { AxiosError } from "axios";
import { getStoreAccessors } from "typesafe-vuex";
import { ActionContext } from "vuex";
import { State } from "../state";
import {
  commitAddNotification,
  commitRemoveNotification,
  commitSetLoggedIn,
  commitSetLogInError,
  commitSetToken,
  commitSetUserProfile,
} from "./mutations";
import { AppNotification, MainState } from "./state";

type MainContext = ActionContext<MainState, State>;

export const actions = {
  async actionLogIn(
    context: MainContext,
    payload: { username: string; password: string }
  ) {
    try {
      const response = await api.logInGetToken(
        payload.username,
        payload.password
      );
      const token = response.data.access_token;
      if (token) {
        saveLocalToken(token);
        commitSetToken(context, token);
        commitSetLoggedIn(context, true);
        commitSetLogInError(context, false);
        await dispatchGetUserProfile(context);
        await dispatchRouteLoggedIn(context);
        commitAddNotification(context, {
          content: "Logged in",
          color: "success",
        });
      } else {
        await dispatchLogOut(context);
      }
    } catch (err) {
      commitSetLogInError(context, true);
      await dispatchLogOut(context);
    }
  },
  async actionGetUserProfile(context: MainContext) {
    try {
      const response = await api.getMe(context.state.token);
      if (response.data) {
        commitSetUserProfile(context, response.data);
      }
    } catch (error) {
      await dispatchCheckApiError(context, error as AxiosError);
    }
  },
  async actionUpdateUserProfile(context: MainContext, payload) {
    const loadingNotification = { content: "saving", showProgress: true };
    try {
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.updateMe(context.state.token, payload),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          ),
        ])
      )[0];
      commitSetUserProfile(context, response.data);
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: "Profile successfully updated",
        color: "success",
      });
    } catch (error) {
      const e = error as AxiosError;
      if (e.response && e.response.data.detail) {
        commitRemoveNotification(context, loadingNotification);
        commitAddNotification(context, {
          content: e.response.data.detail,
          color: "error",
        });
      } else {
        await dispatchCheckApiError(context, error as AxiosError);
      }
    }
  },
  async actionCheckLoggedIn(context: MainContext) {
    if (!context.state.isLoggedIn) {
      let token = context.state.token;
      if (!token) {
        const localToken = getLocalToken();
        if (localToken) {
          commitSetToken(context, localToken);
          token = localToken;
        }
      }
      if (token) {
        try {
          const response = await api.getMe(token);
          commitSetLoggedIn(context, true);
          commitSetUserProfile(context, response.data);
        } catch (error) {
          await dispatchRemoveLogIn(context);
        }
      } else {
        await dispatchRemoveLogIn(context);
      }
    }
  },
  async actionRemoveLogIn(context: MainContext) {
    removeLocalToken();
    commitSetToken(context, "");
    commitSetLoggedIn(context, false);
    commitSetUserProfile(context, null);
  },
  async actionLogOut(context: MainContext) {
    await dispatchRemoveLogIn(context);
  },
  async actionUserLogOut(context: MainContext) {
    await dispatchLogOut(context);
    commitAddNotification(context, { content: "Logged out", color: "success" });
  },
  async actionCheckApiError(context: MainContext, payload: AxiosError) {
    if (payload.response && payload.response!.status === 401) {
      await dispatchLogOut(context);
    } else {
      commitAddNotification(context, {
        content: payload.message,
        color: "error",
      });
    }
  },
  actionRouteLoggedIn(context: MainContext) {
    if (
      router.currentRoute.path === "/login" ||
      router.currentRoute.path === "/"
    ) {
      router.push("/");
    }
  },
  async removeNotification(
    context: MainContext,
    payload: { notification: AppNotification; timeout: number }
  ) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        commitRemoveNotification(context, payload.notification);
        resolve(true);
      }, payload.timeout);
    });
  },
  async passwordRecovery(context: MainContext, payload: { email: string }) {
    const loadingNotification = {
      content: "Sending password recovery email",
      showProgress: true,
    };
    try {
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.passwordRecovery(payload.email),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          ),
        ])
      )[0];
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: "Password recovery email sent",
        color: "success",
      });
      await dispatchLogOut(context);
    } catch (error) {
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        color: "error",
        content: "Incorrect username",
      });
    }
  },
  async resetPassword(
    context: MainContext,
    payload: { password: string; token: string }
  ) {
    const loadingNotification = {
      content: "Resetting password",
      showProgress: true,
    };
    try {
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.resetPassword(payload.password, payload.token),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          ),
        ])
      )[0];
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: "Password successfully reset",
        color: "success",
      });
      await dispatchLogOut(context);
    } catch (error) {
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        color: "error",
        content: "Error resetting password",
      });
    }
  },
  async verifyEmail(context: MainContext, payload: { token: string }) {
    const loadingNotification = {
      content: "Verifying e-mail",
      showProgress: true,
    };
    try {
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.verifyEmail(payload.token),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          ),
        ])
      )[0];
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: "E-mail successfuly verified",
        color: "success",
      });
    } catch (error) {
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: "Error verifying e-mail",
        color: "error",
      });
    }
  },
  async actionCreateWasteSample(
    context: MainContext,
    payload: IWasteSampleCreate
  ) {
    const loadingNotification = { content: "saving", showProgress: true };
    try {
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.createWasteSample(context.rootState.main.token, payload),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          ),
        ])
      )[0];
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: "Sample successfully created",
        color: "success",
      });
    } catch (error) {
      commitRemoveNotification(context, loadingNotification);
      await dispatchCheckApiError(context, error as AxiosError);
    }
  },
  async resendEmailVerification(context: MainContext) {
    const loadingNotification = {
      content: "Requesting new verification",
      showProgress: true,
    };
    try {
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.resendVerification(context.state.token),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          ),
        ])
      )[0];
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: "Please check your mailbox",
        color: "success",
      });
    } catch (error) {
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: "An error occured. Please try again",
        color: "error",
      });
    }
  },
};

const { dispatch } = getStoreAccessors<MainState | any, State>("");

export const dispatchCheckApiError = dispatch(actions.actionCheckApiError);
export const dispatchCheckLoggedIn = dispatch(actions.actionCheckLoggedIn);
export const dispatchGetUserProfile = dispatch(actions.actionGetUserProfile);
export const dispatchLogIn = dispatch(actions.actionLogIn);
export const dispatchLogOut = dispatch(actions.actionLogOut);
export const dispatchUserLogOut = dispatch(actions.actionUserLogOut);
export const dispatchRemoveLogIn = dispatch(actions.actionRemoveLogIn);
export const dispatchRouteLoggedIn = dispatch(actions.actionRouteLoggedIn);
export const dispatchUpdateUserProfile = dispatch(
  actions.actionUpdateUserProfile
);
export const dispatchCreateWasteSample = dispatch(
  actions.actionCreateWasteSample
);
export const dispatchRemoveNotification = dispatch(actions.removeNotification);
export const dispatchPasswordRecovery = dispatch(actions.passwordRecovery);
export const dispatchResetPassword = dispatch(actions.resetPassword);
export const dispatchVerifyEmail = dispatch(actions.verifyEmail);
export const dispatchResendEmailVerification = dispatch(
  actions.resendEmailVerification
);
