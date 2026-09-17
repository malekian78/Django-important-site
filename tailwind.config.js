/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      './templates/**/*.html',
      './**/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        'custom-blue': '#1e3a8a',
      },
      fontFamily: {
        'vazir': ['Vazirmatn', 'sans-serif'],
      }
    },
  },
  plugins: [],
}

