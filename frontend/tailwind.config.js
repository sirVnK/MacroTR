/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#202124",
        panel: "#ffffff",
        line: "#d9dde4",
        mist: "#f4f6f8",
        teal: "#138a8a",
        amber: "#b26b00",
        berry: "#b4234c",
        indigo: "#4f5bd5"
      },
      boxShadow: {
        panel: "0 12px 30px rgba(32, 33, 36, 0.08)"
      }
    }
  },
  plugins: []
};

