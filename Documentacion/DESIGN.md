---
name: Integral System
colors:
  surface: '#f7fafc'
  surface-dim: '#d7dadc'
  surface-bright: '#f7fafc'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f1f4f6'
  surface-container: '#ebeef0'
  surface-container-high: '#e5e9eb'
  surface-container-highest: '#e0e3e5'
  on-surface: '#181c1e'
  on-surface-variant: '#444650'
  inverse-surface: '#2d3133'
  inverse-on-surface: '#eef1f3'
  outline: '#757681'
  outline-variant: '#c5c6d1'
  surface-tint: '#465c9a'
  primary: '#000c2f'
  on-primary: '#ffffff'
  primary-container: '#001f5c'
  on-primary-container: '#7389cb'
  inverse-primary: '#b3c5ff'
  secondary: '#b02f00'
  on-secondary: '#ffffff'
  secondary-container: '#ff5722'
  on-secondary-container: '#541100'
  tertiary: '#001209'
  on-tertiary: '#ffffff'
  tertiary-container: '#002a1a'
  on-tertiary-container: '#68947d'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dbe1ff'
  primary-fixed-dim: '#b3c5ff'
  on-primary-fixed: '#00174a'
  on-primary-fixed-variant: '#2d4481'
  secondary-fixed: '#ffdbd1'
  secondary-fixed-dim: '#ffb5a0'
  on-secondary-fixed: '#3b0900'
  on-secondary-fixed-variant: '#862200'
  tertiary-fixed: '#bdedd2'
  tertiary-fixed-dim: '#a2d1b7'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#234f3b'
  background: '#f7fafc'
  on-background: '#181c1e'
  surface-variant: '#e0e3e5'
typography:
  display-lg:
    fontFamily: Segoe UI
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Segoe UI
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Segoe UI
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-sm:
    fontFamily: Segoe UI
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Segoe UI
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Segoe UI
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Segoe UI
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-lg:
    fontFamily: Segoe UI
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.02em
  label-md:
    fontFamily: Segoe UI
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.04em
  headline-lg-mobile:
    fontFamily: Segoe UI
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 8px
  xs: 4px
  sm: 12px
  md: 24px
  lg: 48px
  xl: 80px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 40px
---

## Brand & Style

The brand personality is authoritative yet efficient, designed specifically for the logistical rigor of corporate travel and expense management. It targets corporate employees and finance administrators who require a tool that feels secure, transparent, and high-velocity.

The design style is a **Minimalist-Corporate** hybrid. It utilizes heavy whitespace to reduce cognitive load during complex data entry. The aesthetic focuses on structural clarity and a "split-screen" architectural logic, where navigation or high-level summaries occupy a stable left or top quadrant, while task-specific actions inhabit a fluid, expansive work area. The emotional response should be one of "controlled precision"—every element serves a functional purpose without decorative excess.

## Colors

The palette is anchored by **Navy (#001F5C)**, representing institutional stability and the primary brand voice. **Orange (#FF5722)** is used sparingly as a high-visibility action color for primary calls-to-action and critical alerts.

**Dark Green (#013220)** is reserved for financial "Success" states and approved reimbursement indicators, providing a sophisticated alternative to standard bright greens. **Celeste (#00ADEF)** functions as a secondary utility color for info-states, active selection indicators, and interactive links. The **Background (#F4F7F9)** is a cool grey-blue that reduces screen glare during extended use, while **White (#FFFFFF)** is used exclusively for elevated cards and data-entry surfaces to create clear visual separation.

## Typography

This design system leverages **Segoe UI** to maintain a native, professional feel that integrates seamlessly with enterprise environments. The hierarchy is strictly enforced: Headlines use semi-bold weights with tighter tracking to command attention, while body text remains neutral and highly legible.

Labels and metadata use increased letter-spacing and uppercase styling where appropriate to differentiate technical data from narrative content. On mobile devices, headline sizes are scaled down to ensure that long-form financial titles do not break layouts or force excessive scrolling.

## Layout & Spacing

The layout utilizes a **12-column fluid grid** for desktop and a **4-column grid** for mobile. The hallmark of the system is the **Split-Screen Ratio**: on desktop, a fixed 280px sidebar manages navigation, while the content area is divided into a 60/40 split for data list and detail views.

Spacing follows a strict 8px linear scale. Large 48px to 80px "safety zones" are used between major content sections to prevent the UI from feeling cluttered. Gutters are fixed at 24px to ensure distinct separation between financial data columns.

## Elevation & Depth

To maintain a minimalist profile, the design system avoids heavy drop shadows. Instead, it employs **Tonal Layering** and **Low-Contrast Outlines**.

1.  **Level 0 (Base):** The Background color (#F4F7F9).
2.  **Level 1 (Cards):** White surfaces with a 1px solid border in a 10% opacity version of the Navy color. No shadow.
3.  **Level 2 (Interaction):** When a user interacts with a card or element, a soft, neutral ambient shadow is applied (0px 4px 12px, 5% Navy opacity) to suggest lift.
4.  **Level 3 (Modals):** Large modals use a 20% Navy backdrop tint to focus the user’s attention, with the surface itself maintaining a crisp, thin border.

## Shapes

The shape language is **Soft (0.25rem)**. This provides a subtle modern touch without sacrificing the professional, "square" rigor required by a banking institution.

- **Buttons & Inputs:** 4px (0.25rem) corner radius.
- **Cards & Modals:** 8px (0.5rem) corner radius.
- **Status Badges:** 12px (0.75rem) to create a distinct visual "pill" shape that contrasts against rectangular data fields.

## Components

### Buttons
- **Primary:** Solid Navy (#001F5C) with white text. High-emphasis actions.
- **Secondary:** Solid Orange (#FF5722) with white text. Reserved for "Submit" or "Approve."
- **Ghost:** Transparent background with Navy border and text. Used for "Cancel" or secondary navigation.

### Input Fields
Inputs use a white background with a 1px border. On focus, the border changes to Celeste (#00ADEF) with a 2px thickness. Labels are consistently placed above the input in `label-md` styling.

### Status Chips
Small, high-contrast badges used for expense status:
- **Pending:** Celeste background, Navy text.
- **Approved:** Dark Green background, White text.
- **Rejected:** Light Red (Utility), Dark Red text.

### Expense Cards
Cards are the primary container for viaticum entries. They feature a 1px Navy-tinted border, `body-md` for the amount (bolded), and `body-sm` for the date/category.

### Progress Trackers
A horizontal stepper component used for multi-stage reimbursement requests. Active steps are Navy; completed steps are Dark Green with a check icon; upcoming steps are light grey.