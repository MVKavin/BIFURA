# BIFURA — AI-Agent Incident Intelligence & Debugging Platform

> **Tagline:** One mistake. Many consequences. One verified fix.

This repository contains the multi-page landing experience for **BIFURA**, engineered with a scroll-driven camera portal transition, clean editorial typography, and a custom Mint Green (`#98FF98`) color system.

---

## 🚀 Quickstart & Setup Instructions

### 1. Prerequisites
- **Node.js**: v18.0.0 or higher (v20+ recommended).
- **npm** (or `pnpm` / `yarn`).

### 2. Install Dependencies
```bash
npm install
```

### 3. Run Development Server
```bash
npm run dev
```
The local server will start at `http://localhost:5173`.

### 4. Build for Production
```bash
npm run build
```
Generates optimized production assets in the `dist/` directory.

### 5. Preview Production Build
```bash
npm run preview
```

---

## 📁 Key File Structure & Architecture

- **`src/components/ui/glyph-portal.tsx`**:
  The scroll-driven camera portal component. Utilizes dynamic Canvas 2D raster scanning to locate the thickest ink stem of the word `BIFURA` and performs hardware-accelerated SVG `clip-path` camera scale and roll transitions.

- **`src/components/ui/demo.tsx`**:
  The `BifuraPortal` wrapper. Renders the pure white opening canvas with deep green letters, the minimal top bar (`bifura.` | `AI incident intelligence`), and the `Step inside ↘` pill button.

- **`src/pages/OverviewPage.jsx`**:
  The main landing page. Begins inside the portal, smoothly transitions from the deep green letter stem into the **Mint Green (`#98FF98`)** background, and displays:
  1. Editorial hero tagline and mission statement with deep obsidian text.
  2. 3-beat minimal workflow:
     - `01 / Root-Cause Pinpointing` (Earliest Point of Divergence)
     - `02 / Safety Guardrails` (ALLOW · REVIEW · BLOCK)
     - `03 / Verified Resolution` (Deterministic CI/CD Replay)
  3. Audited enterprise metrics (`0`, `89%`, `100%`, `< 14ms`).
  4. Closing walkthrough call-to-action.

- **`src/components/AppleNav.jsx`**:
  Unified 60px frosted dark glass navigation bar (`bifura.` + page tabs + `Book Demo ↗` button). It smoothly hides on initial scroll=0 to keep the white opening frame immaculate, and glides into view as soon as the user enters the portal.

- **`src/pages/IntelligencePage.jsx`**:
  Incident intelligence deep dive, featuring the causal backtracking graph and blast radius DAG simulation.

- **`src/pages/SafetyPage.jsx`**:
  Real-time tool execution enforcement with interactive ALLOW / REVIEW / BLOCK tri-state gates.

- **`src/pages/ReplayPage.jsx`**:
  Deterministic CI/CD test harness, replay code fixtures, and automated patch synthesis verification.

- **`src/pages/EnterprisePage.jsx`**:
  Enterprise compliance certifications (SOC 2 Type II, ISO 27001, EU AI Act Art. 14, SLA 99.99%) and customer case studies.

- **`src/pages/BuySpecPage.jsx`**:
  Interactive fleet scale & sovereign deployment perimeter configurator.

- **`src/components/AppleFooter.jsx`**:
  Dark obsidian footer with multi-column site directory, compliance links, and legal disclosures.

---

## 🎨 Color Tokens & Theming
- **Opening Canvas**: `#FFFFFF` (Pure White)
- **Portal Letter Ink**: Forest Green radial gradient (`#0b3b2a` to `#14573f`)
- **Revealed Canvas**: Official Mint Green (`#98FF98`)
- **Primary Text on Mint**: Deep Obsidian Black (`#0c1c13` / `#000000`)
- **Secondary Text on Mint**: Dark Pine / Moss (`#1e442f` / `#255239`)
- **Accents**: Emerald (`#047857`), Amber (`#b45309`), Crimson Rose (`#f87171`)
