# Data Analysis Project - Integration Guide

This project is ready to be copied into another React + Tailwind project.

## Files to Copy

### Required Files:
1. `/components/DataSection.tsx` - The main section component
2. `/App.tsx` - Example implementation (or copy the content into your existing page)

### Dependencies Required:
- `motion/react` (Framer Motion) - for animations
- `./components/ui/badge` - ShadCN badge component

## Integration Steps

### Option 1: Use as a separate page
1. Copy `/components/DataSection.tsx` to your project's components directory
2. Copy the content from `/App.tsx` into a new page component
3. Update import paths to match your project structure
4. Ensure you have the ShadCN Badge component installed

### Option 2: Integrate into existing page
1. Copy `/components/DataSection.tsx` to your components directory
2. Import and use `DataSection` components in your existing page:

```tsx
import { DataSection } from './components/DataSection';
import { motion } from 'motion/react';

export function YourPage() {
  return (
    <div>
      {/* Your existing content */}
      
      <DataSection
        sectionNumber={1}
        title="Your Analysis Title"
        conclusion="Your analysis conclusion text here..."
        graphPlaceholder="unique-id"
        delay={0.2}
      />
      
      <DataSection
        sectionNumber={2}
        title="Another Section"
        conclusion="More analysis..."
        graphPlaceholder="unique-id-2"
        delay={0.3}
        reversed
      />
    </div>
  );
}
```

## Theme Support

This component works with both light and dark themes automatically using Tailwind's dark mode classes:
- `bg-background`, `text-foreground`, `bg-card`, `border-border`, etc.

To enable dark mode in your project, add the `dark` class to the html or body element:
```tsx
document.documentElement.classList.add('dark');
```

Or use Tailwind's dark mode configuration in your project.

## Customization

### DataSection Props:
- `sectionNumber`: number - Section number badge
- `title`: string - Section title
- `conclusion`: string - Analysis text
- `graphPlaceholder`: string - Unique ID for the graph (used for SVG pattern IDs)
- `delay?`: number - Animation delay in seconds (optional, default: 0)
- `reversed?`: boolean - Flip layout (text on right, graph on left) (optional, default: false)

### Replace Graph Placeholders:
To add real graphs, replace the placeholder div in `DataSection.tsx` with your actual chart component (e.g., using recharts, chart.js, etc.)

## Styling Notes

- Uses Tailwind v4 CSS variables
- Responsive: stacks on mobile, side-by-side on desktop (md breakpoint)
- Smooth scroll animations trigger when sections come into view
- All spacing and colors use CSS custom properties for easy theming
