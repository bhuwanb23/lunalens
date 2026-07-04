# Login Page Design System

## Overview

Premium split-panel login page inspired by the Dribbble Cogie login design — dark canvas, ribbon art, serif headings.

## Layout

- **Desktop**: Split card (50% left / 50% right), centered on `#0A0A0A` background
- **Mobile**: Single column, left panel hidden
- **Card**: max-width 1020px, border-radius 28px, heavy shadow
- **Corner glow**: Ribbon asset bleeds outside card at top-left and bottom-right

## Color Palette

| Token | Value | Usage |
|-------|-------|-------|
| `--color-bg` | `#0A0A0A` | Page background |
| `--color-surface` | `#FFFFFF` | Card, right panel |
| `--color-input` | `#F5F5F5` | Input backgrounds |
| `--color-text-primary` | `#111827` | Headings, body |
| `--color-text-secondary` | `#6B7280` | Subtitles, labels |
| `--color-text-muted` | `#9CA3AF` | Placeholders |
| `--color-border` | `#E5E7EB` | Input borders |
| `--color-button` | `#000000` | Primary button |
| `--color-button-hover` | `#1F2937` | Button hover |
| `--color-error` | `#EF4444` | Validation errors |
| `--color-success` | `#22C55E` | Success states |

## Typography

- **Serif headings**: Playfair Display (`--font-serif`)
- **Sans body**: Plus Jakarta Sans (`--font-sans`)
- **Brand**: 18px / 700
- **Welcome heading**: 32px serif / 600
- **Left quote**: 42px serif / 600
- **Subheading**: 14px / 400
- **Label**: 14px / 600
- **Input**: 14px / 500
- **Button**: 14px / 600

## Assets

- `/images/login-ribbon-bg.webp` — left panel + corner glow background

## Components

### Left Panel (`LeftPanel.jsx`)
- Black base + ribbon image
- "A WISE QUOTE" label with underline
- Serif headline: "Get Everything You Want"

### Right Panel (`LoginCard.jsx`)
- Wave-circle logo + LunaLens name
- Serif "Welcome Back" heading
- Email/password form with eye toggle
- Black Sign In button
- Google sign-in (UI only, coming soon)
- Sign up link

## Auth

- Frontend sends `{ email, password }` to `POST /login`
- Demo: `test001@lunalens.app` / `test001@2024`
