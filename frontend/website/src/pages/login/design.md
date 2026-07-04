# Login Page Design System

## Overview

Premium split-panel login page with abstract wave background.

## Layout

- **Desktop**: Split card (48% left / 52% right), centered on dark background
- **Mobile**: Single column, left panel hidden
- **Card**: max-width 1020px, rounded-2xl, heavy shadow

## Color Palette

| Token | Value | Usage |
|-------|-------|-------|
| `--color-bg` | `#0A0A0A` | Page background |
| `--color-surface` | `#FFFFFF` | Card, right panel |
| `--color-input` | `#F5F5F5` | Input backgrounds |
| `--color-text-primary` | `#111827` | Headings, body |
| `--color-text-secondary` | `#6B7280` | Subtitles, labels |
| `--color-text-muted` | `#9CA3AF` | Placeholders |
| `--color-border` | `#E5E7EB` | Input borders, dividers |
| `--color-button` | `#000000` | Primary button |
| `--color-button-hover` | `#1F2937` | Button hover |
| `--color-error` | `#EF4444` | Validation errors |
| `--color-success` | `#22C55E` | Success states |

## Typography

- **Font**: Plus Jakarta Sans
- **Brand**: 18px / 700
- **Heading**: 28px / 700
- **Subheading**: 14px / 400
- **Label**: 14px / 500
- **Input**: 14px / 400
- **Button**: 14px / 600
- **Small**: 13px / 400

## Animations

- `fadeInUp`: Card entrance (0.7s ease-out)
- `fadeIn`: Staggered element entrance
- `subtlePulse`: Background breathing (optional)

## Components

### Left Panel
- Abstract wave image (Unsplash)
- Bottom-up gradient overlay
- Quote text: "Get Everything You Want"

### Right Panel
- Brand logo + name
- "Welcome Back" heading
- Email/password form
- Social login (Google full-width + Apple/Facebook/X circles)
- Sign up link
