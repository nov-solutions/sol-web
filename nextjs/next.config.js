/** @type {import('next').NextConfig} */

const nextConfig = {
  webpackDevMiddleware: (config) => {
    console.log("Webpack Watch Options:", config.watchOptions);
    config.watchOptions = {
      poll: 1000, // Check for changes every second
      aggregateTimeout: 300, // Delay before rebuilding
    };
    return config;
  },
};

const withPWA = require("next-pwa")({
  dest: "public",
  disable: process.env.NODE_ENV == "development",
});

module.exports = withPWA(nextConfig);
