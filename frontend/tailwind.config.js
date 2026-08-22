/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          900: '#0f1419',
          800: '#1a1f2e',
          700: '#2d3748',
        },
        accent: {
          purple: '#7c3aed',
          cyan: '#06b6d4',
          pink: '#ec4899',
        },
      },
      boxShadow: {
        'glow': '0 0 20px rgba(124, 58, 237, 0.15)',
        'glow-strong': '0 0 30px rgba(124, 58, 237, 0.25)',
      },
      animation: {
        'pulse-soft': 'pulse-soft 2s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite forwards',
        'slide-up': 'slide-up 300ms ease-out forwards',
        'waveform': 'waveform 0.6s ease-in-out infinite',
        'rotate-chevron': 'rotate-chevron 200ms ease forwards',
      },
      keyframes: {
        'pulse-soft': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.8' },
        },
        'glow': {
          '0%, 100%': { boxShadow: '0 0 20px rgba(124, 58, 237, 0.15)' },
          '50%': { boxShadow: '0 0 30px rgba(124, 58, 237, 0.25)' },
        },
        'slide-up': {
          'from': { transform: 'translateY(20px)', opacity: '0' },
          'to': { transform: 'translateY(0)', opacity: '1' },
        },
        'waveform': {
          '0%, 100%': { height: '4px' },
          '50%': { height: '16px' },
        },
        'rotate-chevron': {
          'from': { transform: 'rotate(0deg)' },
          'to': { transform: 'rotate(180deg)' },
        }
      }
    },
  },
  plugins: [],
}
