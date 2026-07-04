# Login Page Design System (Redesign)

## Color Palette

| Token | Value | Usage |
|-------|-------|-------|
| `background` | `#000000` | Page background (dark) |
| `surface` | `#FFFFFF` | Card right panel background |
| `card-left-bg` | Image (abstract waves) | Left panel background |
| `text-primary` | `#1A2B3C` | Headings, body text on white |
| `text-secondary` | `#6B7B8D` | Labels, placeholders |
| `text-muted` | `#9CA3AF` | Disabled text |
| `input-bg` | `#F5F5F5` | Input field background |
| `button-primary` | `#000000` | Sign In button background |
| `button-primary-text` | `#FFFFFF` | Sign In button text |
| `border` | `#E2E8F0` | Social button borders |
| `error` | `#DC3545` | Validation errors |
| `success` | `#28A745` | Success states |

## Typography

- **Font Family:** Plus Jakarta Sans (Google Fonts)
- **Weights:** 400 (regular), 500 (medium), 600 (semibold), 700 (bold)
- **Sizes:**
  - Page title (brand): 24px / 700
  - Heading: 28px / 700
  - Subheading: 14px / 400
  - Body: 14px / 400
  - Label: 13px / 500
  - Small: 12px / 400
  - Button: 14px / 600

## Spacing

- Card padding: 48px (desktop), 32px (mobile)
- Input padding: 12px vertical, 16px horizontal
- Gap between form fields: 16px
- Gap between sections: 20px
- Social buttons gap: 12px

## Borders & Shadows

- Card border-radius: 24px
- Input border-radius: 8px
- Button border-radius: 8px
- Social icon border-radius: 50%
- Card shadow: `0 8px 32px rgba(0,0,0,0.12)`

## Layout

- Split screen: 50% / 50% on desktop (>= 1024px)
- Mobile: single column, left panel hidden or shown above form
- Left panel: abstract wave image with overlaid text
- Right panel: white background, centered form

## Components

### Brand Logo
- Name: LunaLens
- Font: Plus Jakarta Sans, 24px, bold
- Color: text-primary

### Input Fields
- Label above input, 13px, weight 500, color text-secondary
- No icons inside inputs (as per design)
- Placeholder: text-muted
- Background: input-bg
- Border: none
- Border-radius: 8px
- Focus: subtle ring effect

### Primary Button (Sign In)
- Full width
- Background: button-primary (black)
- Text: button-primary-text (white), 14px, weight 600
- Padding: 12px vertical
- Hover: opacity 0.9
- Border-radius: 8px

### Google Button
- Full width
- Background: white
- Border: 1px solid border
- Text: 14px, weight 500
- Padding: 12px vertical
- Border-radius: 8px
- Includes Google icon

### Social Icons (secondary)
- Size: 44x44px circle
- Border: 1px solid border
- Background: white
- Hover: background #F8F9FA
- Icons: brand-colored SVGs

### Left Panel
- Background image: abstract colorful waves
- Overlay: dark gradient (for text readability)
- Text:
  - Small label: "A WISE QUOTE"
  - Large heading: "Get Everything You Want"
  - Subtitle: motivational quote