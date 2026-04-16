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
        background: "#ffffff",
        foreground: "#18181b", // zinc-900
        surface: "#fafafa",    // zinc-50
        surfaceElevated: "#f4f4f5", // zinc-100
        border: "rgba(228, 228, 231, 0.8)", // zinc-200
        accent: {
          DEFAULT: "#f59e0b", // amber-500
          hover: "#d97706",   // amber-600
        },
        success: "#10b981", // emerald-500
        danger: "#ef4444",
        warning: "#f59e0b",
        muted: {
          DEFAULT: "#f4f4f5",
          foreground: "#71717a", // zinc-500
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
