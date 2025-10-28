# AI Nutrition Optimizer - REST API Specification

## API Base URL
- Development: `http://localhost:8000/api/v1`
- Production: `https://api.nutrition-optimizer.com/v1`

## Authentication
- **Type**: JWT Bearer Token
- **Header**: `Authorization: Bearer <token>`

---

## 1. Authentication & User Management APIs

### 1.1 User Authentication
```
POST /auth/register
Content-Type: application/json

Request Body:
{
  "email": "user@example.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1990-01-01",
  "gender": "male",
  "height_cm": 175,
  "weight_kg": 70.5,
  "activity_level": "moderately_active"
}

Response (201):
{
  "user_id": "uuid",
  "email": "user@example.com",
  "message": "Registration successful. Please verify your email.",
  "verification_token": "token"
}
```

```
POST /auth/login
Content-Type: application/json

Request Body:
{
  "email": "user@example.com",
  "password": "password123"
}

Response (200):
{
  "access_token": "jwt_token",
  "refresh_token": "refresh_token",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

```
POST /auth/refresh
Content-Type: application/json

Request Body:
{
  "refresh_token": "refresh_token"
}

Response (200):
{
  "access_token": "new_jwt_token",
  "expires_in": 3600
}
```

```
POST /auth/logout
Authorization: Bearer <token>

Response (200):
{
  "message": "Successfully logged out"
}
```

```
POST /auth/verify-email
Content-Type: application/json

Request Body:
{
  "verification_token": "token"
}

Response (200):
{
  "message": "Email verified successfully"
}
```

### 1.2 User Profile Management
```
GET /users/profile
Authorization: Bearer <token>

Response (200):
{
  "id": "uuid",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1990-01-01",
  "gender": "male",
  "height_cm": 175,
  "weight_kg": 70.5,
  "activity_level": "moderately_active",
  "created_at": "2025-01-01T00:00:00Z",
  "dietary_preferences": ["vegetarian"],
  "allergens": ["nuts", "shellfish"],
  "goals": [
    {
      "goal_type": "budget",
      "target_value": 200.00,
      "current_value": 150.00,
      "unit": "USD"
    }
  ]
}
```

```
PUT /users/profile
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "first_name": "John",
  "last_name": "Doe",
  "height_cm": 175,
  "weight_kg": 70.5,
  "activity_level": "very_active"
}

Response (200):
{
  "message": "Profile updated successfully",
  "user": { /* updated user object */ }
}
```

### 1.3 Dietary Preferences & Allergens
```
POST /users/dietary-preferences
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "preferences": ["vegetarian", "gluten_free"]
}

Response (201):
{
  "message": "Dietary preferences updated",
  "preferences": ["vegetarian", "gluten_free"]
}
```

```
GET /users/dietary-preferences
Authorization: Bearer <token>

Response (200):
{
  "preferences": ["vegetarian", "gluten_free"]
}
```

```
POST /users/allergens
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "allergens": [
    {
      "allergen_name": "nuts",
      "severity": "severe"
    },
    {
      "allergen_name": "shellfish",
      "severity": "moderate"
    }
  ]
}

Response (201):
{
  "message": "Allergens updated",
  "allergens": [/* allergen objects */]
}
```

```
GET /users/allergens
Authorization: Bearer <token>

Response (200):
{
  "allergens": [
    {
      "allergen_name": "nuts",
      "severity": "severe"
    }
  ]
}
```

---

## 2. Ingredients & Nutrition APIs

### 2.1 Ingredients Management
```
GET /ingredients
Query Parameters:
- category: string (optional)
- search: string (optional)
- limit: integer (default: 50)
- offset: integer (default: 0)

Response (200):
{
  "ingredients": [
    {
      "id": "uuid",
      "name": "Organic Spinach",
      "category": "vegetables",
      "subcategory": "leafy_greens",
      "unit": "g",
      "nutrition": {
        "calories_per_100g": 23,
        "protein_g": 2.9,
        "carbs_g": 3.6,
        "fat_g": 0.4
      },
      "environmental_data": {
        "carbon_footprint_kg_co2": 0.2,
        "seasonality": ["spring", "fall"]
      },
      "avg_price_per_kg": 8.50
    }
  ],
  "total": 150,
  "limit": 50,
  "offset": 0
}
```

```
GET /ingredients/{ingredient_id}

Response (200):
{
  "id": "uuid",
  "name": "Organic Spinach",
  "category": "vegetables",
  "nutrition": {
    "serving_size": 100,
    "serving_unit": "g",
    "calories": 23,
    "protein_g": 2.9,
    "carbs_g": 3.6,
    "fat_g": 0.4,
    "fiber_g": 2.2,
    "sodium_mg": 79
  },
  "environmental_data": {
    "carbon_footprint_kg_co2": 0.2,
    "water_usage_liters": 1.8,
    "seasonality": ["spring", "fall"]
  },
  "pricing_history": [
    {
      "price_per_unit": 8.50,
      "unit": "kg",
      "store_name": "Whole Foods",
      "price_date": "2025-01-01"
    }
  ]
}
```

### 2.2 Nutrition Analysis
```
POST /nutrition/analyze
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "ingredients": [
    {
      "ingredient_id": "uuid",
      "quantity": 200,
      "unit": "g"
    }
  ]
}

Response (200):
{
  "total_nutrition": {
    "calories": 46,
    "protein_g": 5.8,
    "carbs_g": 7.2,
    "fat_g": 0.8,
    "fiber_g": 4.4
  },
  "nutrition_score": 85.5,
  "breakdown": [
    {
      "ingredient_id": "uuid",
      "ingredient_name": "Organic Spinach",
      "contribution": {
        "calories": 46,
        "protein_g": 5.8
      }
    }
  ]
}
```

---

## 3. Recipe Management APIs

### 3.1 Recipe CRUD Operations
```
GET /recipes
Query Parameters:
- search: string (optional)
- cuisine_type: string (optional)
- difficulty_level: string (optional)
- dietary_restrictions: array (optional)
- max_cook_time: integer (optional)
- min_rating: decimal (optional)
- limit: integer (default: 20)
- offset: integer (default: 0)
- sort_by: string (rating, cook_time, nutrition_score)

Response (200):
{
  "recipes": [
    {
      "id": "uuid",
      "name": "Mediterranean Quinoa Bowl",
      "cuisine_type": "mediterranean",
      "difficulty_level": "easy",
      "prep_time_minutes": 15,
      "cook_time_minutes": 20,
      "total_time_minutes": 35,
      "servings": 2,
      "rating_avg": 4.8,
      "rating_count": 124,
      "image_url": "https://...",
      "dietary_info": ["vegetarian", "gluten_free"],
      "nutrition_summary": {
        "calories_per_serving": 450,
        "protein_g_per_serving": 18,
        "nutrition_score": 88
      },
      "estimated_cost_per_serving": 4.25
    }
  ],
  "total": 500,
  "filters_applied": {
    "cuisine_type": "mediterranean",
    "difficulty_level": "easy"
  }
}
```

```
GET /recipes/{recipe_id}

Response (200):
{
  "id": "uuid",
  "name": "Mediterranean Quinoa Bowl",
  "description": "A healthy and delicious bowl...",
  "cuisine_type": "mediterranean",
  "difficulty_level": "easy",
  "prep_time_minutes": 15,
  "cook_time_minutes": 20,
  "total_time_minutes": 35,
  "servings": 2,
  "instructions": "Step 1: Rinse quinoa...",
  "image_url": "https://...",
  "ingredients": [
    {
      "ingredient_id": "uuid",
      "ingredient_name": "Quinoa",
      "quantity": 1,
      "unit": "cup",
      "is_optional": false,
      "preparation_note": "uncooked"
    }
  ],
  "nutrition_summary": {
    "calories_per_serving": 450,
    "protein_g_per_serving": 18,
    "carbs_g_per_serving": 52,
    "fat_g_per_serving": 20,
    "nutrition_score": 88
  },
  "environmental_impact": {
    "carbon_footprint_per_serving": 1.2,
    "water_usage_liters": 45
  },
  "cost_analysis": {
    "estimated_cost_per_serving": 4.25,
    "ingredient_costs": [
      {
        "ingredient_name": "Quinoa",
        "cost": 1.50
      }
    ]
  },
  "tags": ["healthy", "meal_prep", "high_protein"],
  "dietary_info": ["vegetarian", "gluten_free"],
  "rating_avg": 4.8,
  "rating_count": 124
}
```

```
POST /recipes
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "name": "My Custom Recipe",
  "description": "A delicious recipe",
  "cuisine_type": "american",
  "difficulty_level": "easy",
  "prep_time_minutes": 10,
  "cook_time_minutes": 15,
  "servings": 4,
  "instructions": "Step 1: ...",
  "ingredients": [
    {
      "ingredient_id": "uuid",
      "quantity": 2,
      "unit": "cups",
      "preparation_note": "chopped"
    }
  ],
  "tags": ["quick", "easy"]
}

Response (201):
{
  "id": "uuid",
  "message": "Recipe created successfully",
  "recipe": { /* full recipe object */ }
}
```

### 3.2 Recipe Recommendations
```
GET /recipes/recommendations
Authorization: Bearer <token>
Query Parameters:
- pantry_based: boolean (default: true)
- max_results: integer (default: 10)
- preference_weight: decimal (0.0-1.0)

Response (200):
{
  "recommendations": [
    {
      "recipe": { /* recipe object */ },
      "recommendation_score": 0.92,
      "reasons": [
        "Uses 3 ingredients from your pantry",
        "Matches your vegetarian preference",
        "High nutrition score (88/100)"
      ],
      "pantry_match_percentage": 75,
      "missing_ingredients": [
        {
          "ingredient_name": "Feta Cheese",
          "quantity": 0.5,
          "unit": "cup",
          "estimated_cost": 3.50
        }
      ]
    }
  ]
}
```

---

## 4. Pantry Management APIs

### 4.1 Pantry CRUD Operations
```
GET /pantry
Authorization: Bearer <token>
Query Parameters:
- category: string (optional)
- expiring_within_days: integer (optional)
- location: string (optional)

Response (200):
{
  "pantry_items": [
    {
      "id": "uuid",
      "ingredient": {
        "id": "uuid",
        "name": "Fresh Spinach",
        "category": "vegetables"
      },
      "quantity": 250,
      "unit": "g",
      "purchase_date": "2025-01-10",
      "expiry_date": "2025-01-20",
      "cost": 3.99,
      "location": "fridge",
      "days_until_expiry": 3,
      "status": "expiring_soon"
    }
  ],
  "summary": {
    "total_items": 24,
    "expiring_soon": 5,
    "total_value": 145.50,
    "categories": {
      "vegetables": 8,
      "fruits": 6,
      "grains": 5
    }
  }
}
```

```
POST /pantry
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "ingredient_id": "uuid",
  "quantity": 500,
  "unit": "g",
  "purchase_date": "2025-01-15",
  "expiry_date": "2025-02-15",
  "cost": 4.50,
  "location": "pantry"
}

Response (201):
{
  "id": "uuid",
  "message": "Pantry item added successfully",
  "item": { /* pantry item object */ }
}
```

```
PUT /pantry/{item_id}
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "quantity": 300,
  "expiry_date": "2025-02-20"
}

Response (200):
{
  "message": "Pantry item updated successfully",
  "item": { /* updated pantry item */ }
}
```

```
DELETE /pantry/{item_id}
Authorization: Bearer <token>

Response (204): No Content
```

### 4.2 Pantry Analytics
```
GET /pantry/analytics
Authorization: Bearer <token>
Query Parameters:
- period: string (week, month, quarter, year)

Response (200):
{
  "usage_statistics": {
    "total_items_used": 45,
    "total_items_wasted": 3,
    "waste_percentage": 6.67,
    "total_spending": 285.50,
    "average_item_cost": 6.35
  },
  "category_breakdown": {
    "vegetables": {
      "items_used": 20,
      "items_wasted": 2,
      "total_cost": 85.50
    }
  },
  "expiry_predictions": [
    {
      "ingredient_name": "Milk",
      "expiry_date": "2025-01-21",
      "days_remaining": 1,
      "suggested_recipes": ["Creamy Pasta", "Smoothie Bowl"]
    }
  ],
  "recommendations": [
    "Consider buying smaller quantities of leafy greens",
    "Your vegetable usage rate is 85% - excellent!"
  ]
}
```

### 4.3 Expiry Notifications
```
GET /pantry/expiring
Authorization: Bearer <token>
Query Parameters:
- days: integer (default: 3)

Response (200):
{
  "expiring_items": [
    {
      "id": "uuid",
      "ingredient_name": "Spinach",
      "quantity": 250,
      "unit": "g",
      "expiry_date": "2025-01-20",
      "days_remaining": 1,
      "suggested_recipes": [
        {
          "recipe_id": "uuid",
          "recipe_name": "Green Smoothie",
          "uses_quantity": 100
        }
      ]
    }
  ],
  "total_expiring": 5,
  "estimated_waste_value": 15.50
}
```

---

## 5. Meal Planning APIs

### 5.1 Meal Plan Generation
```
POST /meal-plans/generate
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "start_date": "2025-01-20",
  "end_date": "2025-01-26",
  "meal_types": ["breakfast", "lunch", "dinner"],
  "servings_per_meal": 2,
  "optimization_preferences": {
    "nutrition_weight": 0.3,
    "cost_weight": 0.3,
    "sustainability_weight": 0.2,
    "waste_reduction_weight": 0.2
  },
  "budget_limit": 150.00,
  "dietary_restrictions": ["vegetarian"],
  "excluded_ingredients": ["mushrooms"],
  "pantry_priority": true
}

Response (202):
{
  "generation_id": "uuid",
  "message": "Meal plan generation started",
  "estimated_completion_time": "2025-01-15T10:02:00Z",
  "status": "processing"
}
```

```
GET /meal-plans/generation/{generation_id}/status
Authorization: Bearer <token>

Response (200):
{
  "generation_id": "uuid",
  "status": "completed", // processing, completed, failed
  "progress_percentage": 100,
  "completion_time": "2025-01-15T10:01:45Z",
  "result": {
    "pareto_solutions_count": 8,
    "selected_plan_id": "uuid"
  }
}
```

```
GET /meal-plans/generation/{generation_id}/results
Authorization: Bearer <token>

Response (200):
{
  "generation_id": "uuid",
  "pareto_solutions": [
    {
      "plan_id": "uuid",
      "rank": 1,
      "name": "Balanced Nutrition Plan",
      "objectives": {
        "nutrition_score": 92.5,
        "total_cost": 128.50,
        "carbon_footprint": 8.2,
        "waste_reduction": 85
      },
      "meals_count": 21,
      "explanation": "This plan maximizes nutrition while staying within budget...",
      "is_recommended": true
    }
  ],
  "visualization_data": {
    "pareto_front_coordinates": [
      {
        "plan_id": "uuid",
        "x": 128.50, // cost
        "y": 92.5,   // nutrition
        "size": 85   // sustainability indicator
      }
    ]
  }
}
```

### 5.2 Meal Plan Management
```
GET /meal-plans
Authorization: Bearer <token>
Query Parameters:
- status: string (active, completed, archived)
- start_date: date (optional)
- end_date: date (optional)

Response (200):
{
  "meal_plans": [
    {
      "id": "uuid",
      "name": "Sustainable Week",
      "start_date": "2025-01-20",
      "end_date": "2025-01-26",
      "status": "active",
      "total_cost": 128.50,
      "avg_nutrition_score": 92.5,
      "total_carbon_footprint": 8.2,
      "waste_reduction_percentage": 85,
      "meals_count": 21,
      "created_at": "2025-01-15T10:00:00Z"
    }
  ]
}
```

```
GET /meal-plans/{plan_id}
Authorization: Bearer <token>

Response (200):
{
  "id": "uuid",
  "name": "Sustainable Week",
  "start_date": "2025-01-20",
  "end_date": "2025-01-26",
  "meals": [
    {
      "id": "uuid",
      "planned_date": "2025-01-20",
      "meal_type": "breakfast",
      "recipe": {
        "id": "uuid",
        "name": "Overnight Oats",
        "prep_time_minutes": 5,
        "nutrition_score": 85
      },
      "servings": 2,
      "cost_per_serving": 2.50,
      "pantry_ingredients_used": [
        "Oats", "Milk", "Honey"
      ]
    }
  ],
  "objectives": {
    "nutrition_score": 92.5,
    "total_cost": 128.50,
    "carbon_footprint": 8.2,
    "waste_reduction": 85
  },
  "explanation": {
    "key_factors": [
      "Uses 75% of pantry ingredients",
      "Prioritizes seasonal vegetables",
      "Balances protein across all meals"
    ],
    "trade_offs": "Higher cost for better nutrition",
    "confidence_score": 0.92
  }
}
```

```
PUT /meal-plans/{plan_id}/select
Authorization: Bearer <token>

Response (200):
{
  "message": "Meal plan selected successfully",
  "plan": { /* meal plan object */ },
  "shopping_list_generated": true,
  "shopping_list_id": "uuid"
}
```

---

## 6. Shopping List APIs

### 6.1 Shopping List Generation
```
POST /shopping-lists/generate
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "meal_plan_id": "uuid",
  "exclude_pantry_items": true,
  "preferred_stores": ["Whole Foods", "Trader Joes"],
  "budget_limit": 75.00
}

Response (201):
{
  "shopping_list_id": "uuid",
  "total_items": 15,
  "estimated_total_cost": 68.50,
  "message": "Shopping list generated successfully"
}
```

```
GET /shopping-lists/{list_id}
Authorization: Bearer <token>

Response (200):
{
  "id": "uuid",
  "name": "Week of Jan 20-26",
  "meal_plan_id": "uuid",
  "status": "active",
  "total_estimated_cost": 68.50,
  "items": [
    {
      "id": "uuid",
      "ingredient": {
        "id": "uuid",
        "name": "Cucumber",
        "category": "vegetables"
      },
      "quantity_needed": 2,
      "unit": "pieces",
      "estimated_cost": 1.50,
      "is_purchased": false,
      "stores": [
        {
          "store_name": "Whole Foods",
          "price": 1.50,
          "distance_km": 2.5
        }
      ]
    }
  ],
  "categories": {
    "vegetables": {
      "items_count": 6,
      "estimated_cost": 24.50
    },
    "proteins": {
      "items_count": 3,
      "estimated_cost": 18.00
    }
  }
}
```

### 6.2 Shopping List Management
```
PUT /shopping-lists/{list_id}/items/{item_id}/purchase
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "actual_cost": 1.75,
  "store_name": "Whole Foods",
  "purchase_date": "2025-01-18"
}

Response (200):
{
  "message": "Item marked as purchased",
  "remaining_items": 14,
  "remaining_cost": 66.75
}
```

```
POST /shopping-lists/{list_id}/complete
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "total_actual_cost": 72.30,
  "notes": "Found good deals on vegetables"
}

Response (200):
{
  "message": "Shopping list completed",
  "cost_variance": 3.80,
  "pantry_updated": true
}
```

---

## 7. Analytics & Insights APIs

### 7.1 User Analytics
```
GET /analytics/dashboard
Authorization: Bearer <token>
Query Parameters:
- period: string (week, month, quarter, year)
- start_date: date (optional)
- end_date: date (optional)

Response (200):
{
  "period": "month",
  "start_date": "2025-01-01",
  "end_date": "2025-01-31",
  "summary": {
    "total_spending": 520.00,
    "avg_nutrition_score": 91.2,
    "carbon_footprint_kg": 45.2,
    "waste_reduction_percentage": 88.5,
    "meals_planned": 84,
    "meals_completed": 76
  },
  "trends": {
    "spending": {
      "current_period": 520.00,
      "previous_period": 632.00,
      "change_percentage": -17.7,
      "trend": "decreasing"
    },
    "nutrition": {
      "current_avg": 91.2,
      "previous_avg": 83.5,
      "change_percentage": 9.2,
      "trend": "improving"
    }
  },
  "weekly_breakdown": [
    {
      "week": "2025-01-01",
      "spending": 65.00,
      "nutrition_score": 89.5,
      "carbon_footprint": 8.2
    }
  ]
}
```

### 7.2 Insights & Recommendations
```
GET /analytics/insights
Authorization: Bearer <token>

Response (200):
{
  "insights": [
    {
      "type": "spending_optimization",
      "title": "Cost Optimization Opportunity",
      "description": "Switching to seasonal vegetables could save you $15-20 per month",
      "impact": "medium",
      "actionable": true,
      "suggested_actions": [
        "Choose winter vegetables like carrots and cabbage",
        "Avoid out-of-season produce"
      ]
    },
    {
      "type": "nutrition_pattern",
      "title": "Your Best Day: Thursdays",
      "description": "You consistently make healthier choices on Thursdays with 94/100 nutrition score",
      "impact": "informational",
      "suggested_actions": [
        "Replicate Thursday's meal planning strategy"
      ]
    }
  ],
  "achievements": [
    {
      "id": "uuid",
      "type": "waste_warrior",
      "title": "Waste Warrior",
      "description": "Zero waste for 7 consecutive days",
      "earned_date": "2025-01-15",
      "points": 100
    }
  ]
}
```

### 7.3 Performance Metrics
```
GET /analytics/performance
Authorization: Bearer <token>
Query Parameters:
- metric: string (nutrition, cost, sustainability, waste)
- period: string (week, month, year)

Response (200):
{
  "metric": "nutrition",
  "period": "month",
  "current_score": 91.2,
  "target_score": 85.0,
  "performance": "exceeding",
  "history": [
    {
      "date": "2025-01-01",
      "value": 88.5
    },
    {
      "date": "2025-01-02",
      "value": 89.2
    }
  ],
  "percentile_ranking": 85, // compared to other users
  "recommendations": [
    "Continue focusing on protein variety",
    "Consider adding more omega-3 rich foods"
  ]
}
```

---

## 8. ML/AI Service APIs

### 8.1 Model Information
```
GET /ml/models
Authorization: Bearer <token>

Response (200):
{
  "models": [
    {
      "name": "nsga_ii_optimizer",
      "version": "1.2.0",
      "type": "optimization",
      "status": "active",
      "performance_metrics": {
        "convergence_rate": 0.95,
        "solution_quality": 0.92
      },
      "last_updated": "2025-01-10T00:00:00Z"
    },
    {
      "name": "recipe_recommender",
      "version": "2.1.0",
      "type": "recommendation",
      "status": "active",
      "performance_metrics": {
        "accuracy": 0.89,
        "precision": 0.91
      }
    }
  ]
}
```

### 8.2 Custom Optimization
```
POST /ml/optimize
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "objective_weights": {
    "nutrition": 0.4,
    "cost": 0.3,
    "sustainability": 0.2,
    "waste": 0.1
  },
  "constraints": {
    "max_cost": 200.00,
    "min_nutrition_score": 80,
    "required_nutrients": ["protein", "vitamin_c"]
  },
  "time_horizon_days": 7,
  "population_size": 100,
  "generations": 50
}

Response (202):
{
  "optimization_id": "uuid",
  "status": "processing",
  "estimated_completion": "2025-01-15T10:05:00Z"
}
```

---

## 9. System APIs

### 9.1 Health Check
```
GET /health

Response (200):
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected",
  "ml_services": "operational",
  "timestamp": "2025-01-15T10:00:00Z"
}
```

### 9.2 System Settings
```
GET /settings/dietary-options

Response (200):
{
  "dietary_preferences": [
    "vegan", "vegetarian", "pescatarian", "keto", "paleo", "mediterranean"
  ],
  "allergens": [
    "nuts", "shellfish", "dairy", "gluten", "eggs", "soy"
  ],
  "activity_levels": [
    "sedentary", "lightly_active", "moderately_active", "very_active"
  ]
}
```

## Error Responses

All APIs follow standard HTTP status codes:

```
400 Bad Request:
{
  "error": "validation_error",
  "message": "Invalid request data",
  "details": {
    "field": "email",
    "error": "Invalid email format"
  }
}

401 Unauthorized:
{
  "error": "authentication_required",
  "message": "Valid authentication token required"
}

403 Forbidden:
{
  "error": "access_denied",
  "message": "Insufficient permissions"
}

404 Not Found:
{
  "error": "resource_not_found",
  "message": "Requested resource not found"
}

429 Too Many Requests:
{
  "error": "rate_limit_exceeded",
  "message": "Rate limit exceeded. Try again in 60 seconds",
  "retry_after": 60
}

500 Internal Server Error:
{
  "error": "internal_server_error",
  "message": "An unexpected error occurred",
  "request_id": "uuid"
}
```

## Rate Limiting

- **Authentication endpoints**: 5 requests per minute per IP
- **Data modification endpoints**: 100 requests per hour per user
- **Read-only endpoints**: 1000 requests per hour per user
- **ML optimization endpoints**: 10 requests per hour per user