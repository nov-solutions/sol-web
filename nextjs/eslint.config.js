const eslint = require("@eslint/js");
const tseslint = require("typescript-eslint");

module.exports = tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.recommended,
  {
    ignores: [
      "web/**",
      "nextjs/.next/**",
      "package.json",
      "**/*.config.js",
      "**/.cache/**",
    ],
    rules: {
      "@typescript-eslint/no-explicit-any": "off",
    },
  },
);
