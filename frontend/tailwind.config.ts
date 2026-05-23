import type { Config } from 'tailwindcss'

export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: '#0B3D91', light: '#1a56c4', dark: '#082d6e' },
        accent: '#C0392B',
      },
      fontFamily: { sans: ['Inter', 'system-ui', 'sans-serif'] },
      keyframes: {
        fadeIn:      { from: { opacity: '0' }, to: { opacity: '1' } },
        slideUp:     { from: { opacity: '0', transform: 'translateY(24px)' }, to: { opacity: '1', transform: 'translateY(0)' } },
        slideIn:     { from: { opacity: '0', transform: 'translateX(-12px)' }, to: { opacity: '1', transform: 'translateX(0)' } },
        scaleIn:     { from: { opacity: '0', transform: 'scale(0.93)' }, to: { opacity: '1', transform: 'scale(1)' } },
        float:       { '0%,100%': { transform: 'translateY(0)' }, '50%': { transform: 'translateY(-8px)' } },
        scan:        { '0%': { top: '0%' }, '100%': { top: '95%' } },
        shimmer:     { '0%': { backgroundPosition: '-200% 0' }, '100%': { backgroundPosition: '200% 0' } },
        borderPulse: { '0%,100%': { borderColor: 'rgba(11,61,145,0.35)' }, '50%': { borderColor: 'rgba(11,61,145,0.9)' } },
        gradientX:   { '0%,100%': { backgroundPosition: '0% 50%' }, '50%': { backgroundPosition: '100% 50%' } },
      },
      animation: {
        fadeIn:        'fadeIn 0.4s ease-out both',
        slideUp:       'slideUp 0.5s ease-out both',
        'slideUp-200': 'slideUp 0.5s ease-out 0.15s both',
        'slideUp-400': 'slideUp 0.5s ease-out 0.30s both',
        'slideUp-600': 'slideUp 0.5s ease-out 0.45s both',
        slideIn:       'slideIn 0.4s ease-out both',
        scaleIn:       'scaleIn 0.35s ease-out both',
        float:         'float 3s ease-in-out infinite',
        scan:          'scan 1.6s ease-in-out infinite alternate',
        shimmer:       'shimmer 2s linear infinite',
        borderPulse:   'borderPulse 1.4s ease-in-out infinite',
        gradientX:     'gradientX 5s ease infinite',
      },
      backgroundSize: { '200%': '200% 200%' },
    },
  },
  plugins: [],
} satisfies Config
