/** @type {import('next').NextConfig} */

if (process.env.NODE_ENV == "development") {
  require("dotenv").config({ path: "../.env" });
}
else if (process.env.NODE_ENV == "production") {
  require("dotenv").config({ path: "../.prod.env" });
}

const nextConfig = {

};

const withPWA = require("next-pwa")({
  dest: "public",
  disable: process.env.NODE_ENV == "development",
});

module.exports = withPWA(nextConfig);
