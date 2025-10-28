# RecipeGen - AI-Powered Meal Planning Platform

## Overview

RecipeGen is a comprehensive meal planning and recipe generation platform that helps users create personalized meal plans optimized for nutrition, budget, and sustainability. The application combines AI-powered recipe suggestions with practical pantry management and detailed analytics to provide a complete meal planning solution.

**Core Purpose**: Enable users to generate healthy, cost-effective, and environmentally conscious meal plans based on their dietary preferences, available ingredients, and personal goals.

**Key Features**:
- Personalized onboarding capturing dietary preferences, allergens, and nutrition goals
- AI-powered meal plan generation with multi-objective optimization
- Pantry management with expiry tracking and waste reduction
- Comprehensive recipe library with filtering and search
- Analytics and visualizations for nutritional insights and sustainability metrics
- Responsive design with light/dark mode support

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Framework**: React 18 with TypeScript using a Single Page Application (SPA) pattern via Wouter for client-side routing.

**Rationale**: React provides component reusability and efficient state management for the data-heavy interface. TypeScript adds type safety for better maintainability across the large component library.

**UI Component System**: Radix UI primitives with shadcn/ui styling system.

**Rationale**: Radix provides accessible, unstyled components that can be customized to match the hybrid Material Design + food platform aesthetic. The shadcn/ui approach allows for consistent styling while maintaining flexibility.

**Styling**: Tailwind CSS with custom design tokens and CSS variables for theming.

**Key Design Decisions**:
- Custom color palette with primary green (freshness/health) and secondary orange (appetite stimulation)
- Typography hierarchy using Inter (UI/data), Playfair Display (headings), and JetBrains Mono (numbers/analytics)
- Responsive grid layouts for recipe cards and dashboard components
- CSS variable-based theming for seamless light/dark mode switching

**State Management**: React Context API for global user state (preferences, pantry, active meal plan).

**Rationale**: Context API is sufficient for this application's state complexity without introducing additional dependencies. The UserContext centralizes user preferences, pantry items, and active meal plans for cross-component access.

**Data Visualization**: Chart.js for analytics dashboards and nutritional breakdowns.

**Alternatives Considered**: Recharts was considered but Chart.js provides simpler integration for the bubble charts (Pareto optimization visualization) and macro breakdowns required.

**Form Management**: React Hook Form with Zod validation via @hookform/resolvers.

**Rationale**: Provides performant form handling with built-in validation, reducing boilerplate for the multi-step onboarding and pantry management forms.

### Backend Architecture

**Server Framework**: Express.js with TypeScript running on Node.js.

**Rationale**: Express provides a minimal, flexible foundation for API routes. The application is structured to support future backend expansion while currently operating with mock data.

**Architecture Pattern**: API-first design with `/api` route prefix for clear separation of concerns.

**Current State**: The backend currently uses in-memory storage (MemStorage class) with placeholder routes. The storage interface (IStorage) is designed for easy migration to a database-backed implementation.

**Build System**: Vite for frontend bundling, esbuild for backend compilation.

**Rationale**: Vite provides fast HMR and optimized production builds. esbuild handles server-side TypeScript compilation with minimal configuration.

### Data Storage Solutions

**Current Implementation**: In-memory storage via MemStorage class implementing the IStorage interface.

**Database Schema**: PostgreSQL schema defined using Drizzle ORM with a users table (id, username, password).

**Migration Path**: The application is configured for PostgreSQL via Drizzle but not currently connected. The schema and configuration exist for future database integration:
- Drizzle Kit configuration points to PostgreSQL
- Environment variable `DATABASE_URL` expected but not required for current operation
- Schema uses UUID primary keys and unique constraints on usernames

**Rationale for Current Approach**: Enables rapid frontend development and prototyping without database dependency. The IStorage interface pattern allows seamless transition to persistent storage.

**Future Expansion Needs**:
- User authentication and session management (Connect-PG-Simple configured for PostgreSQL sessions)
- Persistent storage for pantry items, meal plans, and user preferences
- Recipe database with nutritional information
- Analytics data aggregation

### Component Architecture

**Reusable Components**: 
- Form primitives (FormInput, SelectDropdown, CheckboxGroup) for consistent input handling
- UI components from shadcn/ui (Button, Card, Badge, etc.) with custom styling
- Feature components (RecipeCard, VisualizationChart, PantryManager) for domain-specific functionality

**Page Structure**: Route-based page components (HomePage, DashboardPage, PantryPage, etc.) that compose feature components.

**Error Handling**: ErrorBoundary component catches React errors and provides user-friendly fallback UI.

**Accessibility**: ARIA labels, semantic HTML, keyboard navigation support through Radix UI primitives.

## External Dependencies

### UI Component Libraries
- **Radix UI**: Complete set of accessible UI primitives (@radix-ui/react-*)
- **shadcn/ui**: Component styling system built on Radix with Tailwind CSS
- **Lucide React**: Icon library for consistent iconography

### State & Data Management
- **@tanstack/react-query**: Server state management and caching (configured but not actively used with current mock data)
- **React Hook Form**: Form state management with validation
- **Zod**: Schema validation for forms and data
- **drizzle-zod**: Integration between Drizzle ORM and Zod validation

### Styling & Theming
- **Tailwind CSS**: Utility-first CSS framework with custom configuration
- **class-variance-authority**: Type-safe variant styling
- **tailwind-merge & clsx**: Utility class merging

### Data Visualization
- **Chart.js**: Canvas-based charting library
- **react-chartjs-2**: React wrapper for Chart.js

### Routing
- **wouter**: Lightweight client-side router (alternative to React Router)

### Database & ORM
- **Drizzle ORM**: TypeScript ORM for PostgreSQL
- **@neondatabase/serverless**: Serverless PostgreSQL driver (configured for future use)
- **drizzle-kit**: Schema management and migrations

### Session Management
- **connect-pg-simple**: PostgreSQL session store for Express (configured for future authentication)

### Development Tools
- **Vite**: Frontend build tool and dev server with HMR
- **@replit/vite-plugin-***: Replit-specific development enhancements (error overlay, cartographer, dev banner)
- **TypeScript**: Type safety across frontend and backend

### Utilities
- **date-fns**: Date manipulation and formatting
- **nanoid**: Unique ID generation

### Font Delivery
- **Google Fonts CDN**: Inter, Playfair Display, and JetBrains Mono via CDN link in index.html

**Key Integration Notes**:
- Mock data system (`utils/mockData.ts`) currently provides all recipe, meal plan, and pantry data
- TanStack Query configured but primarily for future API integration
- Database configured but not required for current operation
- All external API calls are simulated with timeouts for UX testing