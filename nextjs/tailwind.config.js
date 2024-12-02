/** @type {import('tailwindcss').Config} */

module.exports = {
  content: [
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/layouts/**/*.{js,ts,jsx,tsx,mdx}",
    "./node_modules/@tremor/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        gray: {
          DEFAULT: "#4B5563",
          light: "#F5F5F7",
        },
      },
      fontFamily: {
        body: [
          "-apple-system",
          "BlinkMacSystemFont",
          "Inter",
          "Segoe UI",
          "Roboto",
          "sans-serif",
        ],
        sans: [
          "-apple-system",
          "BlinkMacSystemFont",
          "Inter",
          "Segoe UI",
          "Roboto",
          "sans-serif",
        ],
      },
    },
  },
  daisyui: {
    themes: [
      {
        [process.env.NEXT_PUBLIC_SITE_NAME]: {
          // TODO colors
          primary: "#FFFFFF",
          secondary: "#FFFFFF",
          accent: "#FFFFFF",
          neutral: "#4B5563",
          "base-100": "#FFFFFF",
          success: "#22C55E",
          warning: "#EAB308",
          error: "#EF4444",
        },
      },
    ],
  },
  plugins: [
    require("daisyui"),
    require("@headlessui/tailwindcss"),
    require("@tailwindcss/forms"),
  ],
};
