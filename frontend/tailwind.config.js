/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'qh-primary': '#0F3830',
        'qh-accent': '#D4AF37',
        'qh-bg': '#F8F8F8',
        'qh-text': '#1F2937',
      },
      fontFamily: {
        'ui': ['Comic Neue', 'cursive'],
        'arabic': ['Amiri', 'serif'],
      },
    },
  },
  darkMode: 'class',
  plugins: [],
}
