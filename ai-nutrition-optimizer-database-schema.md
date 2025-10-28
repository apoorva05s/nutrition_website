# AI Nutrition Optimizer - Database Schema Design

## Database Schema Overview

### 1. Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    gender VARCHAR(20),
    height_cm INTEGER,
    weight_kg DECIMAL(5,2),
    activity_level VARCHAR(50), -- sedentary, lightly_active, moderately_active, very_active
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(255),
    reset_token VARCHAR(255),
    reset_token_expires TIMESTAMP
);
```

### 2. User Dietary Preferences
```sql
CREATE TABLE user_dietary_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    preference_type VARCHAR(50) NOT NULL, -- vegan, vegetarian, keto, paleo, etc.
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE user_allergens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    allergen_name VARCHAR(100) NOT NULL,
    severity VARCHAR(20), -- mild, moderate, severe
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE user_goals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    goal_type VARCHAR(50) NOT NULL, -- budget, nutrition, sustainability, weight_loss
    target_value DECIMAL(10,2),
    current_value DECIMAL(10,2),
    unit VARCHAR(20),
    target_date DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 3. Ingredients and Nutrition Data
```sql
CREATE TABLE ingredients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    category VARCHAR(100), -- vegetables, fruits, proteins, grains, dairy, etc.
    subcategory VARCHAR(100),
    unit VARCHAR(20) DEFAULT 'g', -- g, ml, pieces, cups, etc.
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE ingredient_nutrition (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ingredient_id UUID REFERENCES ingredients(id) ON DELETE CASCADE,
    serving_size DECIMAL(8,2) NOT NULL,
    serving_unit VARCHAR(20) NOT NULL,
    calories DECIMAL(8,2),
    protein_g DECIMAL(8,2),
    carbs_g DECIMAL(8,2),
    fat_g DECIMAL(8,2),
    fiber_g DECIMAL(8,2),
    sugar_g DECIMAL(8,2),
    sodium_mg DECIMAL(8,2),
    potassium_mg DECIMAL(8,2),
    vitamin_c_mg DECIMAL(8,2),
    iron_mg DECIMAL(8,2),
    calcium_mg DECIMAL(8,2),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE ingredient_environmental_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ingredient_id UUID REFERENCES ingredients(id) ON DELETE CASCADE,
    carbon_footprint_kg_co2 DECIMAL(8,4), -- per kg
    water_usage_liters DECIMAL(10,2), -- per kg
    land_usage_m2 DECIMAL(10,4), -- per kg
    seasonality JSON, -- {"seasons": ["spring", "summer"], "peak_months": [3,4,5,6]}
    origin_country VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE ingredient_pricing (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ingredient_id UUID REFERENCES ingredients(id) ON DELETE CASCADE,
    price_per_unit DECIMAL(8,2),
    unit VARCHAR(20),
    store_name VARCHAR(100),
    location VARCHAR(200),
    price_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 4. Recipes
```sql
CREATE TABLE recipes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(300) NOT NULL,
    description TEXT,
    cuisine_type VARCHAR(100),
    difficulty_level VARCHAR(20), -- easy, medium, hard
    prep_time_minutes INTEGER,
    cook_time_minutes INTEGER,
    total_time_minutes INTEGER,
    servings INTEGER DEFAULT 1,
    instructions TEXT,
    image_url VARCHAR(500),
    created_by UUID REFERENCES users(id),
    is_public BOOLEAN DEFAULT TRUE,
    rating_avg DECIMAL(3,2) DEFAULT 0,
    rating_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE recipe_ingredients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipe_id UUID REFERENCES recipes(id) ON DELETE CASCADE,
    ingredient_id UUID REFERENCES ingredients(id),
    quantity DECIMAL(8,2) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    is_optional BOOLEAN DEFAULT FALSE,
    preparation_note VARCHAR(200), -- "diced", "chopped", "minced"
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE recipe_tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipe_id UUID REFERENCES recipes(id) ON DELETE CASCADE,
    tag_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE recipe_dietary_info (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipe_id UUID REFERENCES recipes(id) ON DELETE CASCADE,
    dietary_type VARCHAR(50), -- vegan, vegetarian, gluten_free, keto, etc.
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE recipe_nutrition_summary (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipe_id UUID REFERENCES recipes(id) ON DELETE CASCADE,
    calories_per_serving DECIMAL(8,2),
    protein_g_per_serving DECIMAL(8,2),
    carbs_g_per_serving DECIMAL(8,2),
    fat_g_per_serving DECIMAL(8,2),
    fiber_g_per_serving DECIMAL(8,2),
    nutrition_score DECIMAL(5,2), -- 0-100 calculated score
    calculated_at TIMESTAMP DEFAULT NOW()
);
```

### 5. User Pantry Management
```sql
CREATE TABLE user_pantry (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    ingredient_id UUID REFERENCES ingredients(id),
    quantity DECIMAL(8,2) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    purchase_date DATE,
    expiry_date DATE,
    cost DECIMAL(8,2),
    location VARCHAR(100), -- fridge, pantry, freezer
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE pantry_usage_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    ingredient_id UUID REFERENCES ingredients(id),
    quantity_used DECIMAL(8,2),
    unit VARCHAR(20),
    used_in_recipe_id UUID REFERENCES recipes(id),
    usage_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 6. Meal Planning
```sql
CREATE TABLE meal_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(200),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    plan_type VARCHAR(50), -- weekly, monthly, custom
    optimization_preferences JSON, -- {"priority": ["nutrition", "cost", "sustainability", "waste"]}
    total_cost DECIMAL(10,2),
    avg_nutrition_score DECIMAL(5,2),
    total_carbon_footprint DECIMAL(8,2),
    waste_reduction_percentage DECIMAL(5,2),
    generation_algorithm VARCHAR(50) DEFAULT 'NSGA-II',
    pareto_rank INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE meal_plan_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meal_plan_id UUID REFERENCES meal_plans(id) ON DELETE CASCADE,
    recipe_id UUID REFERENCES recipes(id),
    planned_date DATE NOT NULL,
    meal_type VARCHAR(20), -- breakfast, lunch, dinner, snack
    servings INTEGER DEFAULT 1,
    cost_per_serving DECIMAL(8,2),
    nutrition_score DECIMAL(5,2),
    carbon_footprint DECIMAL(8,4),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE meal_plan_generation_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    generation_parameters JSON,
    algorithm_used VARCHAR(50),
    execution_time_seconds DECIMAL(8,2),
    pareto_solutions_count INTEGER,
    selected_plan_id UUID REFERENCES meal_plans(id),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 7. Shopping Lists
```sql
CREATE TABLE shopping_lists (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    meal_plan_id UUID REFERENCES meal_plans(id),
    name VARCHAR(200),
    total_estimated_cost DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'active', -- active, completed, cancelled
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE shopping_list_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    shopping_list_id UUID REFERENCES shopping_lists(id) ON DELETE CASCADE,
    ingredient_id UUID REFERENCES ingredients(id),
    quantity_needed DECIMAL(8,2),
    unit VARCHAR(20),
    estimated_cost DECIMAL(8,2),
    is_purchased BOOLEAN DEFAULT FALSE,
    actual_cost DECIMAL(8,2),
    store_name VARCHAR(100),
    purchase_date DATE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 8. Analytics and Tracking
```sql
CREATE TABLE user_analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    total_spending DECIMAL(10,2) DEFAULT 0,
    avg_nutrition_score DECIMAL(5,2) DEFAULT 0,
    total_carbon_footprint DECIMAL(8,2) DEFAULT 0,
    food_waste_percentage DECIMAL(5,2) DEFAULT 0,
    meals_planned INTEGER DEFAULT 0,
    meals_completed INTEGER DEFAULT 0,
    pantry_utilization_percentage DECIMAL(5,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE user_achievements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    achievement_type VARCHAR(100), -- first_week, waste_warrior, budget_master
    achievement_name VARCHAR(200),
    description TEXT,
    earned_date DATE DEFAULT CURRENT_DATE,
    points INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE user_activity_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    activity_type VARCHAR(100), -- login, meal_plan_generated, recipe_viewed
    activity_data JSON,
    timestamp TIMESTAMP DEFAULT NOW()
);
```

### 9. ML Model Data
```sql
CREATE TABLE ml_model_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_name VARCHAR(100) NOT NULL,
    version VARCHAR(20) NOT NULL,
    model_type VARCHAR(50), -- nsga_ii, recommendation, nutrition_scoring
    model_path VARCHAR(500),
    parameters JSON,
    training_data_hash VARCHAR(255),
    performance_metrics JSON,
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE optimization_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    generation_id UUID,
    solution_rank INTEGER,
    nutrition_score DECIMAL(8,4),
    cost_score DECIMAL(8,4),
    sustainability_score DECIMAL(8,4),
    waste_score DECIMAL(8,4),
    dominated_solutions INTEGER,
    crowding_distance DECIMAL(12,6),
    meal_plan_data JSON,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE user_feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    meal_plan_id UUID REFERENCES meal_plans(id),
    recipe_id UUID REFERENCES recipes(id),
    feedback_type VARCHAR(50), -- rating, preference, complaint
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    feedback_text TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 10. System Configuration
```sql
CREATE TABLE system_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    description TEXT,
    setting_type VARCHAR(50), -- string, integer, decimal, boolean, json
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE api_rate_limits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    endpoint VARCHAR(200),
    requests_count INTEGER DEFAULT 0,
    window_start TIMESTAMP DEFAULT NOW(),
    window_duration_minutes INTEGER DEFAULT 60
);
```

## Indexes for Performance

```sql
-- User-related indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_active ON users(is_active);

-- Ingredient and recipe indexes
CREATE INDEX idx_ingredients_category ON ingredients(category);
CREATE INDEX idx_ingredients_name ON ingredients(name);
CREATE INDEX idx_recipes_cuisine ON recipes(cuisine_type);
CREATE INDEX idx_recipes_difficulty ON recipes(difficulty_level);
CREATE INDEX idx_recipes_rating ON recipes(rating_avg);
CREATE INDEX idx_recipe_ingredients_recipe ON recipe_ingredients(recipe_id);
CREATE INDEX idx_recipe_ingredients_ingredient ON recipe_ingredients(ingredient_id);

-- Pantry indexes
CREATE INDEX idx_user_pantry_user ON user_pantry(user_id);
CREATE INDEX idx_user_pantry_expiry ON user_pantry(expiry_date);
CREATE INDEX idx_user_pantry_ingredient ON user_pantry(ingredient_id);

-- Meal planning indexes
CREATE INDEX idx_meal_plans_user ON meal_plans(user_id);
CREATE INDEX idx_meal_plans_dates ON meal_plans(start_date, end_date);
CREATE INDEX idx_meal_plan_items_plan ON meal_plan_items(meal_plan_id);
CREATE INDEX idx_meal_plan_items_date ON meal_plan_items(planned_date);

-- Analytics indexes
CREATE INDEX idx_user_analytics_user_date ON user_analytics(user_id, date);
CREATE INDEX idx_user_activity_user_time ON user_activity_log(user_id, timestamp);

-- ML indexes
CREATE INDEX idx_optimization_results_user ON optimization_results(user_id);
CREATE INDEX idx_optimization_results_generation ON optimization_results(generation_id);
```

## Database Relationships Summary

1. **Users** → One-to-Many with dietary preferences, allergens, goals, pantry, meal plans
2. **Ingredients** → One-to-Many with nutrition data, environmental data, pricing
3. **Recipes** → Many-to-Many with ingredients through recipe_ingredients
4. **Meal Plans** → One-to-Many with meal plan items
5. **Shopping Lists** → Generated from meal plans, linked to ingredients
6. **Analytics** → Time-series data aggregated from user activities
7. **ML Models** → Version control and optimization results tracking

## Data Volume Estimates

- **Users**: 10,000 - 100,000 users
- **Ingredients**: ~2,000 ingredients
- **Recipes**: ~5,000 recipes
- **User Pantry**: ~50 items per user
- **Meal Plans**: ~50 plans per user per year
- **Analytics**: Daily records per user
- **Optimization Results**: ~10 solutions per generation, ~100 generations per user per year