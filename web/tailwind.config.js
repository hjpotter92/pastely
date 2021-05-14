module.exports = {
  /* mode: 'jit', */
  purge: ["./pages/**/*.{js,jsx}", "./components/**/*.{js,jsx}"],
  darkMode: "media",
  theme: {
    extend: {},
  },
  variants: {
    extend: {
      backgroundColor: ["checked"],
      borderColor: ["checked"],
      textColor: ["checked"],
    },
  },
  plugins: [require("@tailwindcss/forms")],
};
