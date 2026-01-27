# AURA+ Frontend Architecture Documentation

## Overview
The AURA+ frontend has been modernized with a modular, component-based architecture featuring glassmorphism effects, smooth animations, and a consistent design system.

## Directory Structure

```
src/app/
├── app.py                 # Main application entry point
├── components/            # Reusable UI components
│   ├── __init__.py       # Component exports
│   ├── navbar.py         # Top navigation bar
│   ├── sidebar.py        # Sidebar with navigation
│   ├── cards.py          # Card components (info, result cards)
│   ├── forms.py          # Form input components
│   └── status.py         # Progress indicators & status badges
├── static/
│   └── css/              # Modular stylesheets
│       ├── base.css      # Base styles, typography, utilities
│       ├── dark.css      # Dark theme variables
│       ├── light.css     # Light theme variables
│       ├── components.css # Component-specific styles
│       └── animations.css # Animations & micro-interactions
└── utils/                # Utility functions
    ├── constants.py      # Application constants
    ├── model.py          # Model loading & prediction
    └── styles.py         # CSS loading & style utilities
```

## Component Library

### Navbar Component (`components/navbar.py`)
- Fixed top navigation bar with glassmorphism
- Branding with animated logo
- Theme indicator
- Smooth slide-in animation

### Sidebar Component (`components/sidebar.py`)
- Enhanced sidebar with navigation menu
- Theme toggle functionality
- Information cards
- Quick info section

### Card Components (`components/cards.py`)
- `render_info_card()`: Information cards with glassmorphism
  - Supports multiple card types: info, warning, success, error
  - Animated icons and hover effects
- `render_header()`: Page headers with gradient text
- `render_result_card()`: Result display cards

### Form Components (`components/forms.py`)
- `render_question_section()`: Section-based question rendering
- `render_all_questions()`: Complete questionnaire rendering
- Modern slider styling with enhanced interactions

### Status Components (`components/status.py`)
- `render_progress_bar()`: Animated progress indicators
- `render_status_indicator()`: Status badges (success, warning, error, info)
- `render_loading_spinner()`: Loading states
- `render_step_indicator()`: Multi-step process indicators

## CSS Architecture

### Base Styles (`base.css`)
- CSS custom properties (variables)
- Typography scale
- Global resets
- Utility classes (gradient-text, glass)
- Base animations

### Theme Styles (`dark.css` / `light.css`)
- Color palette definitions
- Background colors
- Text colors
- Border colors
- Shadow & glow effects
- Gradient overlays

### Component Styles (`components.css`)
- Button styling with shimmer effects
- Enhanced sliders with modern design
- Expander/accordion styling
- Card components
- Input field styling
- Selectbox styling
- Toggle switches

### Animation Styles (`animations.css`)
- Keyframe animations (fadeIn, slideIn, pulse, glow, etc.)
- Animation utility classes
- Staggered animations
- Hover effects
- Loading states
- Progress indicators
- Status indicators
- Glassmorphism enhancements
- Micro-interactions

## Design System

### Color Palette
- **Primary**: #FF4B4B (Red)
- **Primary Light**: #FF6B6B
- **Primary Dark**: #FF2B2B / #E03B3B

### Typography
- **Font Family**: Inter (Google Fonts)
- **Scale**: 0.85rem - 3.5rem
- **Weights**: 300, 400, 500, 600, 700, 800

### Spacing
- **XS**: 0.5rem
- **SM**: 0.75rem
- **MD**: 1rem
- **LG**: 1.5rem
- **XL**: 2rem
- **2XL**: 3rem

### Border Radius
- **SM**: 8px
- **MD**: 12px
- **LG**: 16px
- **XL**: 20px

### Shadows & Glow
- Multiple shadow levels (sm, md, lg, xl)
- Glow effects for primary color
- Theme-specific shadow variations

## Key Features

### Glassmorphism
- Backdrop blur effects (20px)
- Semi-transparent backgrounds
- Layered depth with shadows
- Applied to: navbar, cards, modals

### Animations
- **Entrance**: fadeIn, slideIn, scaleIn
- **Interactive**: hover-lift, hover-glow, hover-scale
- **Status**: pulse, glow-pulse, float
- **Staggered**: Sequential element animations

### Modern Sliders
- Enhanced track with gradients
- Glowing active portion
- Modern thumb with multiple shadows
- Value display badges
- Smooth transitions and hover effects

### Responsive Design
- Mobile-friendly layouts
- Flexible grid system
- Adaptive spacing
- Reduced motion support

## Usage Examples

### Loading CSS
```python
from utils.styles import load_css

load_css(theme="dark")  # or "light"
```

### Using Components
```python
from components.cards import render_info_card, render_header
from components.status import render_progress_bar, render_status_indicator

# Render header
render_header("Page Title", "Subtitle", theme="dark")

# Render info card
render_info_card(
    "Title",
    "Content",
    emoji="ℹ️",
    theme="dark",
    card_type="info"  # or "warning", "success", "error"
)

# Render progress bar
render_progress_bar(0.75, "Progress", theme="dark")

# Render status indicator
render_status_indicator("success", "Operation completed", theme="dark")
```

## Theme System

The application supports dynamic theme switching:
- Dark mode (default)
- Light mode
- Theme persistence in session state
- Automatic CSS variable updates
- Smooth theme transitions

## Best Practices

1. **Component Reusability**: Use existing components instead of inline HTML
2. **Theme Awareness**: Always pass theme parameter to components
3. **Animation Classes**: Use utility classes for consistent animations
4. **CSS Variables**: Leverage CSS custom properties for theming
5. **Modular CSS**: Keep styles organized in appropriate files
6. **Accessibility**: Support reduced motion preferences

## Future Enhancements

- [ ] Add more animation variants
- [ ] Implement dark/light mode transition animations
- [ ] Add more status component variants
- [ ] Create toast notification component
- [ ] Add modal/dialog component
- [ ] Implement responsive breakpoints
- [ ] Add loading skeleton components
- [ ] Create chart visualization components

## Testing Checklist

- [x] Dark mode functionality
- [x] Light mode functionality
- [x] Theme switching
- [x] Component rendering
- [x] Animation performance
- [x] Responsive behavior
- [ ] Cross-browser compatibility
- [ ] Accessibility compliance

## Notes

- All animations respect `prefers-reduced-motion`
- CSS is loaded dynamically based on theme
- Components are designed to be theme-agnostic
- Glassmorphism effects use backdrop-filter (modern browsers)
