# Recipe Generator Platform - Design Guidelines

## Design Approach

**Hybrid System Approach**: Material Design foundation with inspiration from leading recipe platforms (Yummly, Mealime, HelloFresh) to balance data-heavy functionality with an appetizing, approachable aesthetic.

**Rationale**: This is a utility-focused application with significant data visualization needs, but must remain warm and inviting as a food-related platform. Material Design provides excellent form patterns and data display components, while recipe platform aesthetics ensure the interface feels friendly and food-focused.

---

## Color Palette

### Light Mode
- **Primary**: 16 85% 45% (vibrant green - represents freshness, health, sustainability)
- **Primary Variant**: 16 70% 35% (deeper green for hover states)
- **Secondary**: 25 90% 55% (warm orange - appetite stimulation, warmth)
- **Background**: 0 0% 98% (soft white)
- **Surface**: 0 0% 100% (pure white for cards)
- **Surface Variant**: 0 0% 95% (subtle gray for secondary surfaces)
- **Text Primary**: 0 0% 13% (near black)
- **Text Secondary**: 0 0% 40% (medium gray)
- **Success**: 142 76% 36% (green for low waste, healthy options)
- **Warning**: 38 92% 50% (amber for expiring items)
- **Error**: 0 84% 60% (red for allergen alerts)

### Dark Mode
- **Primary**: 16 75% 55% (brightened green)
- **Secondary**: 25 85% 60% (softened orange)
- **Background**: 0 0% 10% (dark charcoal)
- **Surface**: 0 0% 14% (elevated dark surface)
- **Surface Variant**: 0 0% 18% (lighter dark surface)
- **Text Primary**: 0 0% 95% (off-white)
- **Text Secondary**: 0 0% 65% (light gray)

---

## Typography

**Font Families** (via Google Fonts CDN):
- **Primary**: 'Inter' - clean, highly legible for data displays, forms, and UI elements
- **Headings**: 'Playfair Display' - elegant serif for page titles and recipe names, adds warmth
- **Data/Numbers**: 'JetBrains Mono' - monospaced for analytics, nutrition facts, measurements

**Scale**:
- Hero/H1: text-5xl font-display (Playfair)
- H2: text-3xl font-display
- H3: text-2xl font-semibold (Inter)
- H4: text-xl font-semibold
- Body: text-base (Inter)
- Small/Captions: text-sm
- Data Labels: text-xs font-mono uppercase tracking-wide

---

## Layout System

**Spacing Primitives**: Tailwind units of **2, 4, 6, 8, 12, 16, 20** (e.g., p-4, gap-8, my-12)

**Grid System**:
- Container: max-w-7xl mx-auto px-4 md:px-6 lg:px-8
- Dashboard widgets: grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6
- Recipe cards: grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4
- Forms: max-w-2xl single column with grouped sections

**Vertical Rhythm**:
- Section spacing: py-12 md:py-16
- Component spacing: space-y-6 for stacked elements
- Card padding: p-6

---

## Component Library

### Navigation
- **Navbar**: Fixed top, backdrop-blur-md with subtle shadow, height h-16
- Active link: Primary color underline with font-semibold
- Mobile: Hamburger menu transforms to slide-out drawer

### Forms & Inputs
- **Text Inputs**: Rounded-lg border-2 with focus ring, h-12 px-4
- **Labels**: text-sm font-medium mb-2 positioned above inputs
- **Checkboxes/Radio**: Custom styled with accent-color, larger touch targets (h-5 w-5)
- **Sliders**: Track height 2px, thumb size 16px, primary color fill
- **Dropdowns**: Chevron icon, rounded-lg, shadow-sm on open
- All form elements: Consistent 8px border-radius, clear focus states

### Cards
- **Recipe Cards**: Rounded-xl shadow-md hover:shadow-xl transition, aspect-ratio-square image top
- **Meal Plan Cards**: Rounded-lg border-2 p-6, colored left border accent (4px) indicating nutrition score
- **Pantry Items**: Table rows with zebra striping, expiry badges inline
- **Dashboard Widgets**: Rounded-xl bg-surface shadow-sm p-6

### Buttons
- **Primary**: bg-primary text-white rounded-lg px-6 py-3 font-semibold shadow-sm
- **Secondary**: border-2 border-primary text-primary rounded-lg px-6 py-3
- **Icon Buttons**: Circular p-2 with icon centered, subtle hover background
- **Sizes**: Small (px-4 py-2 text-sm), Default (px-6 py-3), Large (px-8 py-4 text-lg)

### Data Visualization
- **Charts**: Card container with p-6, title text-lg font-semibold mb-4
- **Color Scheme**: Use primary (green) for positive metrics, secondary (orange) for costs, warning for sustainability impacts
- **Tooltips**: Rounded shadow-lg bg-surface p-2 text-sm

### Badges & Tags
- **Status Badges**: Rounded-full px-3 py-1 text-xs font-medium (success/warning/error colors)
- **Diet Tags**: Rounded-md px-2 py-1 bg-surface-variant text-xs (vegan, gluten-free, etc.)
- **Expiry Alerts**: Inline warning/error badge with countdown text

### Tables
- **Headers**: bg-surface-variant text-left text-sm font-semibold py-3 px-4
- **Rows**: py-4 px-4 border-b hover:bg-surface-variant transition
- **Actions**: Icon buttons in last column, aligned right

---

## Page-Specific Guidelines

### Homepage/Onboarding
- **Hero Section**: Full viewport height with food photography background (fresh ingredients, colorful vegetables)
- Headline: "Your Personalized Meal Planning Assistant" (text-5xl Playfair)
- Onboarding form: Multi-step wizard with progress indicator, max-w-2xl centered
- Each step: Generous spacing (space-y-8), clear section headings, helpful descriptions

### Dashboard
- **Layout**: 3-column grid on desktop (active plan, pantry stats, quick actions)
- **Active Meal Plan**: Featured card with image, nutrition rings (Chart.js doughnut), cost summary
- **Pantry Stats**: Number highlights (items, expiring soon) with icon badges
- **Quick Actions**: Button grid for common tasks

### Pantry Manager
- **Add Form**: Sticky sidebar or modal overlay, auto-complete for ingredient names
- **Table View**: Sortable columns (name, quantity, expiry), color-coded expiry status
- **Expiry Alerts**: Warning badges for <3 days, error for expired

### Meal Planner
- **Generator Panel**: Prominent CTA button "Generate Meal Plans" with loading spinner state
- **Results Grid**: 2-3 columns of meal plan cards, each showing small food preview image
- **Metrics Display**: Icon + number pairs (nutrition score, cost, CO2 impact, waste reduction)
- **Comparison**: Side-by-side view option with toggle

### Recipe Library
- **Search Bar**: Sticky top with filters dropdown (diet, time, cuisine)
- **Card Grid**: Responsive 4-column, image-first design with overlay gradient for text
- **Hover Effect**: Lift animation (translateY -4px) with shadow increase

### Analytics
- **Chart Sections**: Full-width containers with title + description
- **Pareto Chart**: Bubble chart showing trade-offs, legend positioned right
- **Comparison Table**: Sticky header, highlight best value in each column
- **AI Explanation Panel**: Bordered card with icon, text-base line-height-relaxed

---

## Images

**Hero Image**: Full-width hero section on homepage featuring vibrant, professionally-shot food photography - overhead shot of fresh vegetables, grains, and ingredients arranged aesthetically. Should convey health, freshness, and variety.

**Recipe Cards**: Each card includes a 1:1 aspect ratio food photo at the top, rounded corners matching card radius.

**Meal Plan Previews**: Smaller thumbnail images (16:9) showing prepared meals.

**Dashboard**: Optional header image strip showing seasonal produce or meal prep scenes.

All images should use object-cover, lazy loading, and have subtle loading skeleton states.

---

## Accessibility & Interactions

- All interactive elements: min-height 44px (touch targets)
- Form labels: Explicitly associated with inputs via htmlFor
- Error states: Aria-live regions announce validation errors
- Keyboard navigation: Visible focus rings (ring-2 ring-primary ring-offset-2)
- Color contrast: Minimum 4.5:1 for text, 3:1 for UI elements
- Motion: Respect prefers-reduced-motion for transitions
- Animations: Use sparingly - subtle hover lifts, smooth page transitions only