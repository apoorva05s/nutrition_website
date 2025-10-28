# Person A - Frontend Developer: Detailed Component Breakdown

## Overview
**Total Stories: 35 component-level stories**
**Total Story Points: 215 points**
**Focus: React/Next.js components with specific API integrations**

---

## 1. FRONTEND SETUP & CORE COMPONENTS (20 points)

### FRONTEND-001: React Project Setup (5 points)
- **Component**: Project initialization
- **APIs**: None
- **Deliverables**: Next.js 14+ with TypeScript, Tailwind CSS, folder structure
- **Expectations**: Complete development environment ready for team

### FRONTEND-002: BaseButton Component (2 points)
- **Component**: `components/ui/BaseButton.tsx`
- **APIs**: None
- **Props**: `variant, size, loading, disabled, icon, onClick, children`
- **Expectations**: Reusable button with 4 variants, loading states, accessibility

### FRONTEND-003: BaseInput Component (3 points)
- **Component**: `components/ui/BaseInput.tsx`
- **APIs**: None
- **Props**: `type, label, placeholder, error, helperText, required, value, onChange`
- **Expectations**: Form-compatible input with validation styling

### FRONTEND-004: BaseModal Component (3 points)
- **Component**: `components/ui/BaseModal.tsx`
- **APIs**: None
- **Props**: `isOpen, onClose, title, children, size`
- **Expectations**: Portal-based modal with focus trap and animations

### COMMON-UI-001: LoadingSpinner (1 point)
- **Component**: `components/ui/LoadingSpinner.tsx`
- **APIs**: None
- **Props**: `size, text, overlay, color`
- **Expectations**: Customizable loading indicators

### COMMON-UI-002: ErrorBoundary (3 points)
- **Component**: `components/ErrorBoundary.tsx`
- **APIs**: None
- **Props**: `fallback, onError`
- **Expectations**: React error boundary with retry functionality

### COMMON-UI-003: FormErrorDisplay (2 points)
- **Component**: `components/ui/FormErrorDisplay.tsx`
- **APIs**: None
- **Props**: `errors, fieldName`
- **Expectations**: Accessible error message display

---

## 2. AUTHENTICATION COMPONENTS (16 points)

### AUTH-UI-001: RegistrationForm (8 points)
- **Component**: `components/auth/RegistrationForm.tsx`
- **APIs**: 
  - `POST /auth/register`
  - `GET /settings/dietary-options`
- **Props**: `onSubmit, loading`
- **State**: `currentStep, formData, dietaryOptions, errors, isSubmitting`
- **Expectations**: 
  - Multi-step form (Personal Info → Dietary Preferences → Verification)
  - Real-time validation and password strength
  - Progress indicator
  - Dietary preferences loaded from API

### AUTH-UI-002: EmailVerification (3 points)
- **Component**: `components/auth/EmailVerification.tsx`
- **APIs**: `POST /auth/verify-email`
- **Props**: `email, onVerificationSuccess`
- **State**: `verificationCode, countdown, isVerifying, error`
- **Expectations**: 
  - 6-digit code input with auto-focus
  - Resend functionality with countdown
  - Auto-submit when complete

### AUTH-UI-003: LoginForm (5 points)
- **Component**: `components/auth/LoginForm.tsx`
- **APIs**: 
  - `POST /auth/login`
  - `POST /auth/refresh`
- **Props**: `onLoginSuccess, redirectUrl`
- **State**: `formData, isLoading, error, rememberMe`
- **Expectations**: 
  - Email/password with validation
  - Remember me with localStorage
  - Forgot password link

---

## 3. NAVIGATION & LAYOUT (8 points)

### NAV-001: AppLayout (5 points)
- **Component**: `components/layout/AppLayout.tsx`
- **APIs**: None
- **Props**: `children, currentUser`
- **State**: `sidebarOpen, currentPath`
- **Expectations**: 
  - Responsive sidebar navigation
  - Header with user menu
  - Breadcrumb navigation
  - Mobile hamburger menu

### NAV-002: Header (3 points)
- **Component**: `components/layout/Header.tsx`
- **APIs**: `POST /auth/logout`
- **Props**: `user, notificationCount`
- **State**: `userMenuOpen, searchQuery`
- **Expectations**: 
  - Logo and user avatar
  - Global search bar
  - Quick access buttons
  - Logout functionality

---

## 4. USER PROFILE MANAGEMENT (10 points)

### AUTH-UI-004: UserProfile (10 points)
- **Component**: `components/profile/UserProfile.tsx`
- **APIs**: 
  - `GET /users/profile`
  - `PUT /users/profile`
  - `GET /users/dietary-preferences`
  - `POST /users/dietary-preferences`
  - `GET /users/allergens`
  - `POST /users/allergens`
- **Props**: `initialData`
- **State**: `profileData, dietaryPreferences, allergens, goals, avatar, isEditing, isSaving`
- **Expectations**: 
  - Complete profile management
  - Dietary preferences multi-select
  - Allergen management with severity
  - Goal setting interface
  - Profile picture upload

---

## 5. RECIPE MANAGEMENT COMPONENTS (26 points)

### RECIPE-UI-001: RecipeSearch (8 points)
- **Component**: `components/recipes/RecipeSearch.tsx`
- **APIs**: 
  - `GET /recipes`
  - `GET /recipes/search`
  - `GET /settings/dietary-options`
- **Props**: `onRecipeSelect`
- **State**: `searchQuery, filters, recipes, loading, hasMore, viewMode`
- **Expectations**: 
  - Search with autocomplete
  - Filter panel (cuisine, dietary, time)
  - Grid/list view toggle
  - Infinite scroll pagination

### RECIPE-UI-002: RecipeCard (3 points)
- **Component**: `components/recipes/RecipeCard.tsx`
- **APIs**: None
- **Props**: `recipe, onSelect, onAddToMealPlan`
- **State**: `imageLoaded, isHovered`
- **Expectations**: 
  - Recipe image with fallback
  - Rating and nutrition score
  - Quick add to meal plan

### RECIPE-UI-003: RecipeDetail (10 points)
- **Component**: `components/recipes/RecipeDetail.tsx`
- **APIs**: 
  - `GET /recipes/{id}`
  - `GET /pantry`
- **Props**: `recipeId`
- **State**: `recipe, pantryItems, checkedIngredients, loading, error`
- **Expectations**: 
  - Complete recipe display
  - Ingredient list with pantry indicators
  - Checkable ingredients for shopping
  - Nutrition charts visualization
  - Add to meal plan functionality

### RECIPE-UI-004: RecipeRecommendations (5 points)
- **Component**: `components/recipes/RecipeRecommendations.tsx`
- **APIs**: `GET /recipes/recommendations`
- **Props**: `userId`
- **State**: `recommendations, currentIndex, userFeedback, loading`
- **Expectations**: 
  - Swipeable recommendation cards
  - Recommendation reasons display
  - Like/dislike feedback
  - Filter options

---

## 6. PANTRY MANAGEMENT COMPONENTS (24 points)

### PANTRY-UI-001: PantryManager (13 points)
- **Component**: `components/pantry/PantryManager.tsx`
- **APIs**: 
  - `GET /pantry`
  - `POST /pantry`
  - `PUT /pantry/{id}`
  - `DELETE /pantry/{id}`
- **Props**: None
- **State**: `pantryItems, selectedItems, editingItem, showAddForm, filters, isLoading`
- **Expectations**: 
  - Item grid with category tabs
  - Add/edit item forms
  - Bulk actions
  - Search and filtering
  - CSV import/export

### PANTRY-UI-002: PantryItemCard (3 points)
- **Component**: `components/pantry/PantryItemCard.tsx`
- **APIs**: None
- **Props**: `item, onEdit, onDelete, onMarkUsed`
- **State**: `daysUntilExpiry, status`
- **Expectations**: 
  - Item image and details
  - Expiry status color coding
  - Quick action buttons

### PANTRY-UI-003: PantryAnalytics (8 points)
- **Component**: `components/pantry/PantryAnalytics.tsx`
- **APIs**: `GET /pantry/analytics`
- **Props**: `timeframe`
- **State**: `analytics, chartData, insights, selectedMetric`
- **Expectations**: 
  - Usage statistics charts
  - Waste reduction metrics
  - Expiry calendar view
  - Cost tracking graphs

---

## 7. MEAL PLANNING COMPONENTS (33 points)

### MEAL-UI-001: MealPlanGenerator (15 points)
- **Component**: `components/meal-planning/MealPlanGenerator.tsx`
- **APIs**: 
  - `POST /meal-plans/generate`
  - `GET /meal-plans/generation/{id}/status`
  - `GET /meal-plans/generation/{id}/results`
- **Props**: `userPreferences`
- **State**: `generationParams, generationId, paretoSolutions, selectedPlans, isGenerating, progress`
- **Expectations**: 
  - Parameter form for optimization
  - Real-time progress tracking
  - Pareto front visualization
  - Plan comparison interface
  - Selection workflow

### MEAL-UI-002: ParetoFrontChart (8 points)
- **Component**: `components/meal-planning/ParetoFrontChart.tsx`
- **APIs**: None
- **Props**: `solutions, onPlanSelect, selectedPlan`
- **State**: `hoveredPlan, zoomState`
- **Expectations**: 
  - Interactive D3.js scatter plot
  - Hover tooltips
  - Clickable points for selection
  - Zoom and pan functionality

### MEAL-UI-003: MealPlanDashboard (10 points)
- **Component**: `components/meal-planning/MealPlanDashboard.tsx`
- **APIs**: 
  - `GET /meal-plans`
  - `GET /meal-plans/{id}`
- **Props**: `currentWeek`
- **State**: `mealPlans, selectedPlan, viewMode, filters, loading`
- **Expectations**: 
  - Weekly calendar view
  - Plan cards with metrics
  - Filtering and search
  - Quick actions

---

## 8. SHOPPING LIST COMPONENTS (13 points)

### SHOP-UI-001: ShoppingList (8 points)
- **Component**: `components/shopping/ShoppingList.tsx`
- **APIs**: 
  - `GET /shopping-lists/{id}`
  - `PUT /shopping-lists/{id}/items/{item_id}/purchase`
  - `POST /shopping-lists/{id}/complete`
- **Props**: `listId`
- **State**: `shoppingList, checkedItems, totalCost, isCompleting`
- **Expectations**: 
  - Checkable item list
  - Category grouping
  - Cost tracking
  - Completion workflow

### SHOP-UI-002: ShoppingListGenerator (5 points)
- **Component**: `components/shopping/ShoppingListGenerator.tsx`
- **APIs**: 
  - `POST /shopping-lists/generate`
  - `GET /pantry`
- **Props**: `mealPlanId`
- **State**: `generationParams, isGenerating, generatedList, pantryItems`
- **Expectations**: 
  - Meal plan selection
  - Pantry exclusion options
  - Store preferences
  - Budget settings

---

## 9. ANALYTICS COMPONENTS (21 points)

### ANALYTICS-UI-001: AnalyticsDashboard (13 points)
- **Component**: `components/analytics/AnalyticsDashboard.tsx`
- **APIs**: 
  - `GET /analytics/dashboard`
  - `GET /analytics/insights`
  - `GET /analytics/performance`
- **Props**: `userId`
- **State**: `analytics, timeRange, chartData, insights, achievements`
- **Expectations**: 
  - Summary metrics cards
  - Interactive charts (spending, nutrition, sustainability)
  - Time range selector
  - Achievement display
  - Export functionality

### ANALYTICS-UI-002: MetricsCard (3 points)
- **Component**: `components/analytics/MetricsCard.tsx`
- **APIs**: None
- **Props**: `metric, value, trend, onClick`
- **State**: `isLoading`
- **Expectations**: 
  - Metric value with trend
  - Color-coded status
  - Click for drill-down

### ANALYTICS-UI-003: AchievementsList (5 points)
- **Component**: `components/analytics/AchievementsList.tsx`
- **APIs**: `GET /analytics/insights`
- **Props**: `achievements`
- **State**: `filter, selectedAchievement`
- **Expectations**: 
  - Achievement cards with progress
  - Social sharing
  - Category filtering

---

## 10. MAIN DASHBOARD (10 points)

### DASH-UI-001: MainDashboard (10 points)
- **Component**: `components/dashboard/MainDashboard.tsx`
- **APIs**: 
  - `GET /users/profile`
  - `GET /meal-plans`
  - `GET /pantry/expiring`
  - `GET /analytics/dashboard`
- **Props**: `currentUser`
- **State**: `dashboardData, isLoading, quickActions`
- **Expectations**: 
  - Personalized welcome section
  - Key metrics overview
  - Current meal plan display
  - Expiring items alerts
  - Quick action buttons

---

## INTEGRATION REQUIREMENTS FOR PERSON A:

### API Integration Patterns:
1. **Authentication APIs**: JWT token management, automatic refresh
2. **CRUD APIs**: Consistent error handling and loading states
3. **Real-time APIs**: WebSocket connections for live updates
4. **File Upload APIs**: Image upload with progress tracking

### State Management:
- **React Context** for global user state
- **React Hook Form** for all forms
- **React Query/SWR** for API data fetching and caching

### Component Architecture:
- **Atomic Design**: Atoms (BaseButton) → Molecules (FormField) → Organisms (LoginForm)
- **TypeScript**: Full type safety for props and state
- **Responsive Design**: Mobile-first with Tailwind CSS

### Testing Requirements:
- **Unit Tests**: All components with React Testing Library
- **Integration Tests**: API integration flows
- **E2E Tests**: Critical user journeys with Cypress

This breakdown gives Person A clear, actionable stories with specific APIs to integrate and detailed expectations for each component!