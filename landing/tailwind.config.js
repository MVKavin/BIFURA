/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          red: '#FF3E24',
          redHover: '#E0341B',
          redBloom: 'rgba(255, 62, 36, 0.35)',
        },
        primary: {
          DEFAULT: '#0066cc', // Action Blue
          focus: '#0071e3',   // Focus Blue
          dark: '#2997ff',    // Sky Link Blue on dark tiles
        },
        ink: {
          DEFAULT: '#1d1d1f',
          muted80: '#333333',
          muted48: '#7a7a7a',
        },
        body: {
          DEFAULT: '#1d1d1f',
          dark: '#ffffff',
          muted: '#cccccc',
        },
        canvas: {
          DEFAULT: '#ffffff',
          parchment: '#f5f5f7',
        },
        surface: {
          pearl: '#fafafc',
          tile1: '#272729',
          tile2: '#2a2a2c',
          tile3: '#252527',
          black: '#000000',
          darkCanvas: '#0B0C10',
          darkPanel: '#111216',
          chip: 'rgba(210, 210, 215, 0.64)',
        },
        hairline: '#e0e0e0',
        dividerSoft: '#f0f0f0',
      },
      fontFamily: {
        display: ['"SF Pro Display"', '-apple-system', 'BlinkMacSystemFont', '"Inter"', 'system-ui', 'sans-serif'],
        text: ['"SF Pro Text"', '-apple-system', 'BlinkMacSystemFont', '"Inter"', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      transitionTimingFunction: {
        'apple-ease': 'cubic-bezier(0.16, 1, 0.3, 1)',
      },
      transitionDuration: {
        'micro': '200ms',
        'reveal': '600ms',
        'hero': '800ms',
      },
      boxShadow: {
        'apple-product': '3px 5px 30px 0 rgba(0, 0, 0, 0.22)',
        'apple-product-lg': '6px 14px 44px 0 rgba(0, 0, 0, 0.28)',
        'brand-bloom': '0 10px 25px -5px rgba(255, 62, 36, 0.35)',
        'brand-bloom-sm': '0 6px 18px -4px rgba(255, 62, 36, 0.28)',
      },
      borderRadius: {
        'apple-sm': '8px',
        'apple-md': '11px',
        'apple-lg': '18px',
        'apple-pill': '9999px',
      },
      animation: {
        'marquee': 'marquee 30s linear infinite',
      },
      keyframes: {
        marquee: {
          '0%': { transform: 'translateX(0%)' },
          '100%': { transform: 'translateX(-50%)' },
        },
      },
    },
  },
  plugins: [],
}
