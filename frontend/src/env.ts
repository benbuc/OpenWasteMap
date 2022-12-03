const env = process.env.VUE_APP_ENV;

let envApiUrl = "";

if (env === "production") {
  envApiUrl = `https://${process.env.VUE_APP_DOMAIN_PROD}`;
} else if (env === "staging") {
  envApiUrl = `https://${process.env.VUE_APP_DOMAIN_STAG}`;
} else if (env === "development") {
  envApiUrl = `https://${process.env.VUE_APP_DOMAIN_DEV}`;
} else {
  envApiUrl = `http://${process.env.VUE_APP_DOMAIN_LOCAL}`;
}

let envTilesUrl = "";
if (env === "production") {
  envTilesUrl = `https://${process.env.VUE_APP_TILES_DOMAIN_PROD}`;
} else if (env === "staging") {
  envTilesUrl = `https://${process.env.VUE_APP_TILES_DOMAIN_STAG}`;
} else if (env === "development") {
  envTilesUrl = `https://${process.env.VUE_APP_TILES_DOMAIN_DEV}`;
} else {
  envTilesUrl = `http://${process.env.VUE_APP_TILES_DOMAIN_LOCAL}`;
}

export const apiUrl = envApiUrl;
export const tilesUrl = envTilesUrl;
export const appName = process.env.VUE_APP_NAME;
export const appVersion = process.env.VUE_APP_VERSION || "no version";
