// filename: vue_js_project/tailwind.config.js
module.exports = {
  content: ["./index.html","./src/**/*.{vue,js,ts,jsx,tsx}"],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: '#2563eb',
        secondary: '#9333ea'
      }
    },
  },
  plugins: [],
}
