import Vue from "vue";
import Router from "vue-router";

import RouterComponent from "../components/RouterComponent.vue";

Vue.use(Router);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/:view_center_zoom(@\\d+\\.\\d+,\\d+\\.\\d+,\\d+z)?",
      component: () =>
        import(/* webpackChunkName: "home" */ "../views/Home.vue"),
      name: "home",
      children: [
        {
          path: "login",
          component: () =>
            import(/* webpackChunkName: "login" */ "../views/Login.vue"),
        },
      ],
    },
    {
      path: "/profile",
      component: RouterComponent,
      redirect: "profile/view",
      children: [
        {
          path: "view",
          component: () =>
            import(
              /* webpackChunkName: "profile" */ "../views/ProfileIndex.vue"
            ),
        },
        {
          path: "edit",
          component: () =>
            import(
              /* webpackChunkName: "profile-edit" */ "../views/main/profile/UserProfileEdit.vue"
            ),
        },
        {
          path: "password",
          component: () =>
            import(
              /* webpackChunkName: "profile-password" */ "../views/main/profile/UserProfileEditPassword.vue"
            ),
        },
      ],
    },
    {
      path: "/signup",
      name: "signup",
      component: () =>
        import(/* webpackChunkName: "signup" */ "../views/Signup.vue"),
    },
    {
      path: "/recover-password",
      component: () =>
        import(
          /* webpackChunkName: "recover-password" */ "../views/PasswordRecovery.vue"
        ),
    },
    {
      path: "/reset-password",
      component: () =>
        import(
          /* webpackChunkName: "reset-password" */ "../views/ResetPassword.vue"
        ),
    },
    {
      path: "/verify-email",
      component: () =>
        import(
          /* webpackChunkName: "verify-email" */ "../views/VerifyEmail.vue"
        ),
    },
    {
      path: "/privacy",
      component: () =>
        import(/* webpackChunkName: "privacy" */ "../views/Privacy.vue"),
    },
    {
      path: "/imprint",
      component: () =>
        import(/* webpackChunkName: "imprint" */ "../views/Imprint.vue"),
    },
    {
      path: "/admin",
      name: "admin",
      component: () =>
        import(/* webpackChunkName: "admin" */ "../views/main/admin/Admin.vue"),
      redirect: "/admin/dashboard",
      children: [
        {
          path: "dashboard",
          component: () =>
            import(
              /* webpackChunkName: "main-dashboard" */ "../views/main/admin/Dashboard.vue"
            ),
        },
        {
          path: "profile",
          component: RouterComponent,
          redirect: "profile/view",
          children: [
            {
              path: "view",
              component: () =>
                import(
                  /* webpackChunkName: "main-profile" */ "../views/main/profile/UserProfile.vue"
                ),
            },
            {
              path: "edit",
              component: () =>
                import(
                  /* webpackChunkName: "main-profile-edit" */ "../views/main/profile/UserProfileEdit.vue"
                ),
            },
            {
              path: "password",
              component: () =>
                import(
                  // tslint:disable-next-line:max-line-length
                  /* webpackChunkName: "main-profile-password" */ "../views/main/profile/UserProfileEditPassword.vue"
                ),
            },
          ],
        },
        {
          path: "users",
          component: RouterComponent,
          redirect: "users/all",
          children: [
            {
              path: "all",
              component: () =>
                import(
                  /* webpackChunkName: "main-admin-users" */ "../views/main/admin/AdminUsers.vue"
                ),
            },
            {
              path: "edit/:id",
              name: "main-admin-users-edit",
              component: () =>
                import(
                  /* webpackChunkName: "main-admin-users-edit" */ "../views/main/admin/EditUser.vue"
                ),
            },
            {
              path: "create",
              name: "main-admin-users-create",
              component: () =>
                import(
                  /* webpackChunkName: "main-admin-users-create" */ "../views/main/admin/CreateUser.vue"
                ),
            },
          ],
        },
        {
          path: "waste-samples",
          component: RouterComponent,
          redirect: "waste-samples/all",
          children: [
            {
              path: "all",
              component: () =>
                import(
                  /* webpackChunkName: "main-admin-waste-samples" */ "../views/main/admin/AdminWasteSamples.vue"
                ),
            },
            {
              path: "create-bulk",
              component: () =>
                import(
                  /* webpackChunkName: "main-admin-waste-sampkes-create-bulk" */ "../views/main/admin/CreateWasteSamplesBulk.vue"
                ),
            },
          ],
        },
      ],
    },
    /*{
      path: '/*', redirect: '/',
    },*/
  ],
});
