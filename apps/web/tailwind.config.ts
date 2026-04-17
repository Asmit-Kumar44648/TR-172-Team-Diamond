import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        background: "#000000",
        foreground: "#ffffff",
        surface: "#09090b",    // zinc-950
        surfaceElevated: "#18181b", // zinc-900
        border: "rgba(255, 255, 255, 0.1)",
        accent: {
          DEFAULT: "#ffffff",
          hover: "#e4e4e7",   // zinc-200
        },
        success: "#ffffff", // Pure white for success in noir
        danger: "#ff0000",  // Keep red for high-contrast danger
        warning: "#ffffff", // Use white for warning too
        muted: {
          DEFAULT: "#18181b",
          foreground: "#52525b", // zinc-400
        },
      },
      borderRadius: {
        lg: "4px",
        md: "2px",
        sm: "1px",
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
