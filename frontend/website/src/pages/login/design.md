# Login Page Design System

## Color Palette

| Token | Value | Usage |
|-------|-------|-------|
| `primary` | `#1A7A6D` | Buttons, links, accents |
| `primary-dark` | `#0D3B35` | Hover states, right panel bg |
| `primary-light` | `#E8F5F3` | Tab active bg, subtle highlights |
| `background` | `#F0F4F8` | Page background |
| `surface` | `#FFFFFF` | Card, input backgrounds |
| `text-primary` | `#1A2B3C` | Headings, body text |
| `text-secondary` | `#6B7B8D` | Labels, placeholders |
| `text-muted` | `#9CA3AF` | Disabled text |
| `border` | `#E2E8F0` | Input borders, dividers |
| `border-focus` | `#1A7A6D` | Focused input border |
| `error` | `#DC3545` | Validation errors |
| `success` | `#28A745` | Success states |

## Typography

- **Font Family:** Inter (Google Fonts)
- **Weights:** 400 (regular), 500 (medium), 600 (semibold), 700 (bold)
- **Sizes:**
  - Page title: 28px / 700
  - Section heading: 20px / 600
  - Body: 15px / 400
  - Label: 14px / 500
  - Small: 13px / 400
  - Footer: 12px / 400

## Spacing

- Card padding: 48px (desktop), 32px (mobile)
- Input padding: 14px vertical, 16px horizontal
- Gap between form fields: 20px
- Gap between sections: 24px
- Social buttons gap: 12px

## Borders & Shadows

- Card border-radius: 16px
- Input border-radius: 10px
- Button border-radius: 10px
- Social icon border-radius: 50%
- Card shadow: `0 4px 24px rgba(0,0,0,0.08)`
- Input shadow (focus): `0 0 0 3px rgba(26,122,109,0.12)`

## Layout

- Split screen: 50% / 50% on desktop (>= 1024px)
- Mobile: single column, right panel hidden
- Left panel: white background, centered content
- Right panel: dark teal gradient with floating cards

## Components

### Sign In / Sign Up Tabs
- Container: rounded pill shape, light gray bg
- Active tab: white bg, subtle shadow, teal text
- Inactive tab: transparent, gray text

### Input Fields
- Label above input, 14px, weight 500, color text-secondary
- Icon inside input (left), 18px, color text-muted
- Placeholder: text-muted
- Border: 1px solid border
- Focus: border-color primary, ring effect

### Social Login Buttons
- Size: 48x48px circle
- Border: 1px solid border
- Background: white
- Hover: background #F8F9FA
- Icons: brand-colored SVGs

### Primary Button
- Full width
- Background: primary
- Text: white, 15px, weight 600
- Padding: 14px vertical
- Hover: primary-dark
- Border-radius: 10px

### Right Panel Cards
- Floating dashboard preview cards
- White cards with shadows, slight rotation
- Positioned absolutely with staggered offsets
