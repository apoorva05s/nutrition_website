# Feature Development Template: Step-by-Step Guide

This template shows exactly what each person does for every feature, in what order, and how they integrate.

---

## 📋 Template: How to Build Any Feature

### **Feature**: [Feature Name]
**Example**: Meal Plan Generation with NSGA-II Optimization

---

## 🔄 Development Sequence

### **STEP 1: Person D (Backend Dev 2) - Data Foundation**

#### **Your Responsibility:**
Set up the database tables and data structure needed for this feature.

#### **What You Do:**
1. **Create Database Tables**
```sql
-- Example for Meal Plan Generation
CREATE TABLE meal_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    name VARCHAR(200),
    start_date DATE,
    end_date DATE,
    optimization_results JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE meal_plan_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meal_plan_id UUID REFERENCES meal_plans(id),
    recipe_id UUID REFERENCES recipes(id),
    planned_date DATE,
    meal_type VARCHAR(20) -- breakfast, lunch, dinner
);
```

2. **Create Sample Data**
```sql
-- Insert test data for development
INSERT INTO meal_plans (user_id, name, start_date, end_date) VALUES
('user-123', 'Test Plan', '2025-01-20', '2025-01-26');
```

3. **Test Database Access**
```python
# test_database.py
import psycopg2

def test_meal_plan_creation():
    conn = psycopg2.connect("postgresql://localhost/nutrition_app")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM meal_plans WHERE name = 'Test Plan'")
    result = cursor.fetchone()
    
    assert result is not None
    print("✅ Database test passed")
```

#### **What You Deliver:**
```yaml
# handoff_to_person_c.yaml
database_setup:
  tables_created:
    - meal_plans
    - meal_plan_items
  connection_string: "postgresql://localhost:5432/nutrition_app"
  test_data: "Sample meal plans inserted"
  verification_queries:
    - "SELECT COUNT(*) FROM meal_plans"
    - "SELECT * FROM meal_plans WHERE user_id = 'user-123'"
```

#### **Person C's Next Steps:**
Person C can now create APIs that read/write to these tables.

---

### **STEP 2: Person B (ML Engineer) - Model Development**

#### **Your Responsibility:**
Build the AI/ML functionality that powers this feature.

#### **What You Do:**

1. **Implement the Algorithm**
```python
# nsga_ii_optimizer.py
from deap import base, creator, tools, algorithms
import numpy as np

class MealPlanOptimizer:
    def __init__(self):
        self.recipes = []
        self.user_preferences = {}
        
    def load_data(self, recipes, user_prefs):
        """Load recipe data and user preferences"""
        self.recipes = recipes
        self.user_preferences = user_prefs
        print(f"✅ Loaded {len(recipes)} recipes")
    
    def evaluate_nutrition(self, meal_plan):
        """Calculate nutrition score for a meal plan"""
        total_score = 0
        for recipe_id in meal_plan:
            recipe = self.get_recipe(recipe_id)
            # Calculate nutrition based on macros
            score = (recipe['protein'] * 0.3 + 
                    recipe['fiber'] * 0.3 + 
                    recipe['vitamins'] * 0.4)
            total_score += score
        return total_score / len(meal_plan)
    
    def evaluate_cost(self, meal_plan):
        """Calculate total cost for a meal plan"""
        total_cost = sum(self.get_recipe(rid)['cost'] for rid in meal_plan)
        return total_cost
    
    def evaluate_sustainability(self, meal_plan):
        """Calculate environmental impact score"""
        total_co2 = sum(self.get_recipe(rid)['carbon_footprint'] for rid in meal_plan)
        return 100 - total_co2  # Lower CO2 = higher score
    
    def evaluate_waste(self, meal_plan):
        """Calculate waste reduction score"""
        pantry_usage = 0
        for recipe_id in meal_plan:
            recipe = self.get_recipe(recipe_id)
            for ingredient in recipe['ingredients']:
                if ingredient in self.user_preferences['pantry_items']:
                    pantry_usage += 1
        return pantry_usage / len(meal_plan)
    
    def optimize_meal_plan(self, days=7, population_size=100, generations=50):
        """Run NSGA-II optimization"""
        print("🚀 Starting NSGA-II optimization...")
        
        # NSGA-II setup
        creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0, 1.0, 1.0))
        creator.create("Individual", list, fitness=creator.FitnessMulti)
        
        toolbox = base.Toolbox()
        toolbox.register("recipe", random.choice, range(len(self.recipes)))
        toolbox.register("individual", tools.initRepeat, creator.Individual, 
                        toolbox.recipe, days)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        
        # Evaluation function
        def evaluate(individual):
            nutrition = self.evaluate_nutrition(individual)
            cost = self.evaluate_cost(individual)
            sustainability = self.evaluate_sustainability(individual)
            waste = self.evaluate_waste(individual)
            return nutrition, cost, sustainability, waste
        
        toolbox.register("evaluate", evaluate)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutUniformInt, low=0, up=len(self.recipes)-1, indpb=0.1)
        toolbox.register("select", tools.selNSGA2)
        
        # Run optimization
        population = toolbox.population(n=population_size)
        
        for gen in range(generations):
            offspring = algorithms.varAnd(population, toolbox, cxpb=0.8, mutpb=0.2)
            fits = toolbox.map(toolbox.evaluate, offspring)
            for fit, ind in zip(fits, offspring):
                ind.fitness.values = fit
            population = toolbox.select(offspring, population_size)
            
            if gen % 10 == 0:
                print(f"⏳ Generation {gen}/{generations}")
        
        # Return Pareto front
        pareto_front = tools.sortNondominated(population, population_size, first_front_only=True)[0]
        
        results = []
        for individual in pareto_front:
            results.append({
                "meal_plan": individual,
                "nutrition_score": individual.fitness.values[0],
                "cost": individual.fitness.values[1],
                "sustainability_score": individual.fitness.values[2],
                "waste_score": individual.fitness.values[3]
            })
        
        print(f"✅ Optimization complete! Found {len(results)} optimal solutions")
        return results
```

2. **Create ML API**
```python
# ml_api.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class OptimizationRequest(BaseModel):
    user_id: str
    dietary_preferences: list[str]
    pantry_items: list[str]
    budget_limit: float
    days: int = 7

@router.post("/ml/optimize-meal-plan")
async def optimize_meal_plan(request: OptimizationRequest):
    try:
        # 1. Initialize optimizer
        optimizer = MealPlanOptimizer()
        
        # 2. Load recipes and user data
        recipes = await load_recipes_from_database()
        user_prefs = {
            "dietary_preferences": request.dietary_preferences,
            "pantry_items": request.pantry_items,
            "budget_limit": request.budget_limit
        }
        optimizer.load_data(recipes, user_prefs)
        
        # 3. Run optimization
        results = optimizer.optimize_meal_plan(days=request.days)
        
        # 4. Return results
        return {
            "optimization_id": generate_uuid(),
            "pareto_solutions": results,
            "total_solutions": len(results),
            "status": "completed"
        }
        
    except Exception as e:
        raise HTTPException(500, f"Optimization failed: {str(e)}")
```

3. **Test the Model**
```python
# test_optimization.py
def test_meal_plan_optimization():
    # Sample data
    recipes = [
        {"id": 1, "protein": 20, "cost": 5.0, "carbon_footprint": 2.0},
        {"id": 2, "protein": 15, "cost": 3.0, "carbon_footprint": 1.5},
        # ... more recipes
    ]
    
    user_prefs = {
        "dietary_preferences": ["vegetarian"],
        "pantry_items": ["quinoa", "tomatoes"],
        "budget_limit": 50.0
    }
    
    optimizer = MealPlanOptimizer()
    optimizer.load_data(recipes, user_prefs)
    
    results = optimizer.optimize_meal_plan(days=7)
    
    assert len(results) > 0
    assert all(r["cost"] <= 50.0 for r in results)
    print("✅ ML optimization test passed")
```

#### **What You Deliver:**
```yaml
# handoff_to_person_c.yaml
ml_services:
  endpoint: "POST /ml/optimize-meal-plan"
  input_format:
    user_id: "string"
    dietary_preferences: ["vegetarian", "gluten_free"]
    pantry_items: ["quinoa", "tomatoes"]
    budget_limit: 50.0
    days: 7
  output_format:
    optimization_id: "uuid"
    pareto_solutions: 
      - meal_plan: [1, 2, 3, 4, 5, 6, 7]
        nutrition_score: 85.5
        cost: 45.0
        sustainability_score: 78.2
        waste_score: 82.0
  performance:
    execution_time: "< 30 seconds"
    accuracy: "87% user satisfaction"
```

#### **Person C's Next Steps:**
Person C integrates this ML endpoint into user-facing APIs.

---

### **STEP 3: Person C (Backend Dev 1) - API Integration**

#### **Your Responsibility:**
Create user-facing APIs that combine database operations with ML functionality.

#### **What You Receive:**
- Database tables from Person D
- ML optimization endpoint from Person B

#### **What You Do:**

1. **Create User-Facing API**
```python
# meal_plan_api.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
import uuid

router = APIRouter()

class MealPlanGenerationRequest(BaseModel):
    start_date: str
    end_date: str
    optimization_preferences: dict
    budget_limit: float

@router.post("/meal-plans/generate")
async def generate_meal_plan(
    request: MealPlanGenerationRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    try:
        # 1. Get user preferences from database
        user_prefs = await get_user_dietary_preferences(current_user.id)
        pantry = await get_user_pantry_items(current_user.id)
        
        # 2. Create generation record
        generation_id = str(uuid.uuid4())
        await create_generation_record(generation_id, current_user.id, "processing")
        
        # 3. Start background optimization
        background_tasks.add_task(
            run_optimization_background,
            generation_id,
            current_user.id,
            user_prefs,
            pantry,
            request
        )
        
        # 4. Return generation ID for status tracking
        return {
            "generation_id": generation_id,
            "status": "processing",
            "estimated_completion": "30 seconds"
        }
        
    except Exception as e:
        raise HTTPException(500, f"Failed to start generation: {str(e)}")

async def run_optimization_background(generation_id, user_id, prefs, pantry, request):
    """Background task that calls ML service and saves results"""
    try:
        # 1. Call ML optimization service
        ml_request = {
            "user_id": user_id,
            "dietary_preferences": prefs,
            "pantry_items": [item.name for item in pantry],
            "budget_limit": request.budget_limit,
            "days": calculate_days(request.start_date, request.end_date)
        }
        
        ml_response = await call_ml_service("/ml/optimize-meal-plan", ml_request)
        
        # 2. Save results to database
        for solution in ml_response["pareto_solutions"]:
            meal_plan = await create_meal_plan(
                user_id=user_id,
                name=f"Optimized Plan {solution['nutrition_score']:.1f}★",
                start_date=request.start_date,
                end_date=request.end_date,
                optimization_results=solution
            )
            
            # Save individual meals
            for day, recipe_id in enumerate(solution["meal_plan"]):
                await create_meal_plan_item(
                    meal_plan_id=meal_plan.id,
                    recipe_id=recipe_id,
                    planned_date=add_days(request.start_date, day),
                    meal_type="dinner"  # Could be more sophisticated
                )
        
        # 3. Update generation status
        await update_generation_status(generation_id, "completed")
        
    except Exception as e:
        await update_generation_status(generation_id, "failed", str(e))

@router.get("/meal-plans/generation/{generation_id}/status")
async def get_generation_status(generation_id: str):
    """Check the status of meal plan generation"""
    status = await get_generation_record(generation_id)
    
    if not status:
        raise HTTPException(404, "Generation not found")
    
    return {
        "generation_id": generation_id,
        "status": status.status,
        "progress_percentage": calculate_progress(status),
        "completion_time": status.completed_at,
        "error_message": status.error_message
    }

@router.get("/meal-plans/generation/{generation_id}/results")
async def get_generation_results(generation_id: str):
    """Get the results of completed meal plan generation"""
    status = await get_generation_record(generation_id)
    
    if status.status != "completed":
        raise HTTPException(400, "Generation not completed")
    
    # Get all meal plans created for this generation
    meal_plans = await get_meal_plans_by_generation(generation_id)
    
    results = []
    for plan in meal_plans:
        results.append({
            "plan_id": plan.id,
            "name": plan.name,
            "objectives": plan.optimization_results,
            "meals": await get_meal_plan_items(plan.id),
            "explanation": generate_explanation(plan.optimization_results)
        })
    
    return {
        "generation_id": generation_id,
        "pareto_solutions": results,
        "visualization_data": create_pareto_chart_data(results)
    }
```

2. **Test API Integration**
```python
# test_meal_plan_api.py
import pytest
from fastapi.testclient import TestClient

def test_meal_plan_generation():
    client = TestClient(app)
    
    # 1. Start generation
    response = client.post("/meal-plans/generate", 
        json={
            "start_date": "2025-01-20",
            "end_date": "2025-01-26", 
            "budget_limit": 50.0,
            "optimization_preferences": {}
        },
        headers={"Authorization": "Bearer test_token"}
    )
    
    assert response.status_code == 200
    generation_id = response.json()["generation_id"]
    
    # 2. Check status
    status_response = client.get(f"/meal-plans/generation/{generation_id}/status")
    assert status_response.json()["status"] in ["processing", "completed"]
    
    # 3. Wait for completion and get results
    import time
    time.sleep(5)  # Wait for background task
    
    results_response = client.get(f"/meal-plans/generation/{generation_id}/results")
    assert results_response.status_code == 200
    assert len(results_response.json()["pareto_solutions"]) > 0
    
    print("✅ API integration test passed")
```

#### **What You Deliver:**
```yaml
# handoff_to_person_a.yaml
api_endpoints:
  generate:
    url: "POST /meal-plans/generate"
    request_body:
      start_date: "2025-01-20"
      end_date: "2025-01-26"
      budget_limit: 50.0
      optimization_preferences: {}
    response:
      generation_id: "uuid"
      status: "processing"
      estimated_completion: "30 seconds"
  
  status:
    url: "GET /meal-plans/generation/{id}/status"
    response:
      generation_id: "uuid"
      status: "completed"
      progress_percentage: 100
  
  results:
    url: "GET /meal-plans/generation/{id}/results"
    response:
      pareto_solutions:
        - plan_id: "uuid"
          name: "Optimized Plan 85.5★"
          objectives:
            nutrition_score: 85.5
            cost: 45.0
            sustainability_score: 78.2
          meals: [...]
```

#### **Person A's Next Steps:**
Person A builds the UI that calls these APIs and displays results.

---

### **STEP 4: Person A (Frontend) - UI Implementation**

#### **Your Responsibility:**
Create the user interface that lets users interact with this feature.

#### **What You Receive:**
- API endpoints from Person C
- Design mockups for the meal plan generator

#### **What You Do:**

1. **Create Meal Plan Generator Component**
```tsx
// components/meal-planning/MealPlanGenerator.tsx
import React, { useState } from 'react';
import { ParetoFrontChart } from './ParetoFrontChart';

interface GenerationParams {
  start_date: string;
  end_date: string;
  budget_limit: number;
  optimization_preferences: {
    nutrition_weight: number;
    cost_weight: number;
    sustainability_weight: number;
    waste_weight: number;
  };
}

export const MealPlanGenerator = () => {
  const [params, setParams] = useState<GenerationParams>({
    start_date: '',
    end_date: '',
    budget_limit: 50,
    optimization_preferences: {
      nutrition_weight: 0.25,
      cost_weight: 0.25,
      sustainability_weight: 0.25,
      waste_weight: 0.25
    }
  });
  
  const [generationId, setGenerationId] = useState<string>('');
  const [status, setStatus] = useState<string>('');
  const [progress, setProgress] = useState<number>(0);
  const [results, setResults] = useState<any[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);

  const startGeneration = async () => {
    setIsGenerating(true);
    
    try {
      // 1. Start meal plan generation
      const response = await fetch('/api/meal-plans/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
        },
        body: JSON.stringify(params)
      });
      
      const data = await response.json();
      setGenerationId(data.generation_id);
      
      // 2. Poll for status updates
      pollGenerationStatus(data.generation_id);
      
    } catch (error) {
      console.error('Generation failed:', error);
      setIsGenerating(false);
    }
  };

  const pollGenerationStatus = async (genId: string) => {
    const checkStatus = async () => {
      try {
        const response = await fetch(`/api/meal-plans/generation/${genId}/status`);
        const statusData = await response.json();
        
        setStatus(statusData.status);
        setProgress(statusData.progress_percentage);
        
        if (statusData.status === 'completed') {
          // Get results
          await loadResults(genId);
          setIsGenerating(false);
        } else if (statusData.status === 'failed') {
          alert('Generation failed: ' + statusData.error_message);
          setIsGenerating(false);
        } else {
          // Continue polling
          setTimeout(checkStatus, 2000);
        }
      } catch (error) {
        console.error('Status check failed:', error);
        setIsGenerating(false);
      }
    };
    
    checkStatus();
  };

  const loadResults = async (genId: string) => {
    try {
      const response = await fetch(`/api/meal-plans/generation/${genId}/results`);
      const resultsData = await response.json();
      setResults(resultsData.pareto_solutions);
    } catch (error) {
      console.error('Failed to load results:', error);
    }
  };

  const selectMealPlan = async (planId: string) => {
    try {
      await fetch(`/api/meal-plans/${planId}/select`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
        }
      });
      
      alert('Meal plan selected successfully!');
      // Redirect to meal plan dashboard
      window.location.href = '/meal-plans';
      
    } catch (error) {
      console.error('Failed to select meal plan:', error);
    }
  };

  return (
    <div className="meal-plan-generator">
      <h1>🎯 Generate Optimal Meal Plan</h1>
      
      {/* Generation Parameters Form */}
      <div className="generation-form">
        <div className="form-row">
          <label>Start Date:</label>
          <input 
            type="date" 
            value={params.start_date}
            onChange={(e) => setParams({...params, start_date: e.target.value})}
          />
          
          <label>End Date:</label>
          <input 
            type="date" 
            value={params.end_date}
            onChange={(e) => setParams({...params, end_date: e.target.value})}
          />
        </div>
        
        <div className="form-row">
          <label>Budget Limit: ${params.budget_limit}</label>
          <input 
            type="range" 
            min="20" 
            max="200" 
            value={params.budget_limit}
            onChange={(e) => setParams({...params, budget_limit: Number(e.target.value)})}
          />
        </div>
        
        {/* Optimization Preferences */}
        <div className="optimization-weights">
          <h3>Optimization Priorities:</h3>
          
          <div className="weight-slider">
            <label>Nutrition Priority: {params.optimization_preferences.nutrition_weight}</label>
            <input 
              type="range" 
              min="0" 
              max="1" 
              step="0.05"
              value={params.optimization_preferences.nutrition_weight}
              onChange={(e) => setParams({
                ...params, 
                optimization_preferences: {
                  ...params.optimization_preferences,
                  nutrition_weight: Number(e.target.value)
                }
              })}
            />
          </div>
          
          {/* Similar sliders for cost, sustainability, waste */}
        </div>
        
        <button 
          onClick={startGeneration} 
          disabled={isGenerating || !params.start_date || !params.end_date}
          className="generate-button"
        >
          {isGenerating ? `Generating... ${progress}%` : 'Generate Meal Plans'}
        </button>
      </div>
      
      {/* Generation Progress */}
      {isGenerating && (
        <div className="generation-progress">
          <div className="progress-bar">
            <div className="progress-fill" style={{width: `${progress}%`}}></div>
          </div>
          <p>Status: {status}</p>
          <p>🧠 AI is optimizing your meal plan using NSGA-II algorithm...</p>
        </div>
      )}
      
      {/* Results Display */}
      {results.length > 0 && (
        <div className="results-section">
          <h2>🎉 Optimization Complete! Found {results.length} optimal solutions</h2>
          
          {/* Pareto Front Visualization */}
          <div className="chart-section">
            <h3>Pareto Front Analysis</h3>
            <ParetoFrontChart 
              solutions={results}
              onPlanSelect={(plan) => console.log('Plan selected:', plan)}
            />
          </div>
          
          {/* Plan Cards */}
          <div className="plan-cards">
            {results.map((plan, index) => (
              <div key={plan.plan_id} className="plan-card">
                <h3>{plan.name}</h3>
                
                <div className="metrics-grid">
                  <div className="metric">
                    <span className="metric-label">Nutrition Score:</span>
                    <span className="metric-value">{plan.objectives.nutrition_score.toFixed(1)}/100</span>
                  </div>
                  
                  <div className="metric">
                    <span className="metric-label">Total Cost:</span>
                    <span className="metric-value">${plan.objectives.cost.toFixed(2)}</span>
                  </div>
                  
                  <div className="metric">
                    <span className="metric-label">Sustainability:</span>
                    <span className="metric-value">{plan.objectives.sustainability_score.toFixed(1)}/100</span>
                  </div>
                  
                  <div className="metric">
                    <span className="metric-label">Waste Reduction:</span>
                    <span className="metric-value">{plan.objectives.waste_score.toFixed(1)}%</span>
                  </div>
                </div>
                
                {/* XAI Explanation */}
                <div className="explanation-box">
                  <strong>🤖 Why this plan?</strong>
                  <p>{plan.explanation}</p>
                </div>
                
                <button 
                  onClick={() => selectMealPlan(plan.plan_id)}
                  className="select-plan-button"
                >
                  Select This Plan
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
```

2. **Create Pareto Front Visualization**
```tsx
// components/meal-planning/ParetoFrontChart.tsx
import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

interface ParetoFrontChartProps {
  solutions: Array<{
    plan_id: string;
    objectives: {
      nutrition_score: number;
      cost: number;
      sustainability_score: number;
    };
  }>;
  onPlanSelect: (plan: any) => void;
}

export const ParetoFrontChart: React.FC<ParetoFrontChartProps> = ({ 
  solutions, 
  onPlanSelect 
}) => {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!solutions.length) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove(); // Clear previous chart

    const width = 500;
    const height = 400;
    const margin = { top: 20, right: 20, bottom: 40, left: 50 };

    // Set up scales
    const xScale = d3.scaleLinear()
      .domain(d3.extent(solutions, d => d.objectives.cost) as [number, number])
      .range([margin.left, width - margin.right]);

    const yScale = d3.scaleLinear()
      .domain(d3.extent(solutions, d => d.objectives.nutrition_score) as [number, number])
      .range([height - margin.bottom, margin.top]);

    const sizeScale = d3.scaleLinear()
      .domain(d3.extent(solutions, d => d.objectives.sustainability_score) as [number, number])
      .range([5, 20]);

    // Draw axes
    svg.append("g")
      .attr("transform", `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(xScale));

    svg.append("g")
      .attr("transform", `translate(${margin.left},0)`)
      .call(d3.axisLeft(yScale));

    // Add axis labels
    svg.append("text")
      .attr("x", width / 2)
      .attr("y", height - 5)
      .attr("text-anchor", "middle")
      .text("Cost ($)");

    svg.append("text")
      .attr("transform", "rotate(-90)")
      .attr("x", -height / 2)
      .attr("y", 15)
      .attr("text-anchor", "middle")
      .text("Nutrition Score");

    // Draw data points
    svg.selectAll("circle")
      .data(solutions)
      .enter()
      .append("circle")
      .attr("cx", d => xScale(d.objectives.cost))
      .attr("cy", d => yScale(d.objectives.nutrition_score))
      .attr("r", d => sizeScale(d.objectives.sustainability_score))
      .attr("fill", "#667eea")
      .attr("opacity", 0.7)
      .style("cursor", "pointer")
      .on("mouseover", function(event, d) {
        // Show tooltip
        const tooltip = d3.select("body").append("div")
          .attr("class", "tooltip")
          .style("position", "absolute")
          .style("background", "black")
          .style("color", "white")
          .style("padding", "10px")
          .style("border-radius", "5px")
          .style("pointer-events", "none");

        tooltip.html(`
          <strong>Meal Plan</strong><br/>
          Nutrition: ${d.objectives.nutrition_score.toFixed(1)}<br/>
          Cost: $${d.objectives.cost.toFixed(2)}<br/>
          Sustainability: ${d.objectives.sustainability_score.toFixed(1)}
        `)
        .style("left", (event.pageX + 10) + "px")
        .style("top", (event.pageY - 10) + "px");
      })
      .on("mouseout", function() {
        d3.selectAll(".tooltip").remove();
      })
      .on("click", function(event, d) {
        onPlanSelect(d);
        
        // Highlight selected point
        svg.selectAll("circle").attr("stroke", "none");
        d3.select(this).attr("stroke", "#ff6b6b").attr("stroke-width", 3);
      });

  }, [solutions, onPlanSelect]);

  return (
    <div className="pareto-chart">
      <svg ref={svgRef} width={500} height={400}></svg>
      <p className="chart-caption">
        💡 Each bubble represents an optimal meal plan. 
        Bubble size indicates sustainability score. 
        Click to select a plan!
      </p>
    </div>
  );
};
```

3. **Test the Complete Feature**
```tsx
// test/MealPlanGenerator.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MealPlanGenerator } from '../components/meal-planning/MealPlanGenerator';

// Mock API responses
global.fetch = jest.fn();

describe('MealPlanGenerator', () => {
  beforeEach(() => {
    (fetch as jest.Mock).mockClear();
  });

  test('generates meal plan successfully', async () => {
    // Mock API responses
    (fetch as jest.Mock)
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({
          generation_id: 'test-gen-123',
          status: 'processing'
        })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({
          status: 'completed',
          progress_percentage: 100
        })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({
          pareto_solutions: [
            {
              plan_id: 'plan-1',
              name: 'Balanced Plan',
              objectives: {
                nutrition_score: 85.5,
                cost: 45.0,
                sustainability_score: 78.2
              }
            }
          ]
        })
      });

    render(<MealPlanGenerator />);

    // Fill in the form
    fireEvent.change(screen.getByLabelText(/start date/i), {
      target: { value: '2025-01-20' }
    });
    fireEvent.change(screen.getByLabelText(/end date/i), {
      target: { value: '2025-01-26' }
    });

    // Start generation
    fireEvent.click(screen.getByText('Generate Meal Plans'));

    // Wait for results
    await waitFor(() => {
      expect(screen.getByText(/Optimization Complete/)).toBeInTheDocument();
    });

    // Verify plan is displayed
    expect(screen.getByText('Balanced Plan')).toBeInTheDocument();
    expect(screen.getByText('85.5/100')).toBeInTheDocument();

    console.log('✅ Full feature test passed');
  });
});
```

#### **What You Deliver:**
- ✅ Working meal plan generator interface
- ✅ Real-time progress tracking during optimization
- ✅ Interactive Pareto front visualization
- ✅ Plan selection and comparison functionality
- ✅ Integration with all backend APIs
- ✅ User-friendly error handling and feedback

---

## 🔗 Integration Verification Checklist

After all 4 people complete their parts, run this verification:

### **End-to-End Test:**
```bash
# 1. Database check (Person D)
psql -d nutrition_app -c "SELECT COUNT(*) FROM meal_plans;"

# 2. ML service check (Person B)
curl -X POST http://localhost:8001/ml/optimize-meal-plan \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "dietary_preferences": ["vegetarian"], "pantry_items": ["quinoa"], "budget_limit": 50, "days": 7}'

# 3. Backend API check (Person C)
curl -X POST http://localhost:8000/api/meal-plans/generate \
  -H "Authorization: Bearer test_token" \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2025-01-20", "end_date": "2025-01-26", "budget_limit": 50}'

# 4. Frontend check (Person A)
npm test -- MealPlanGenerator.test.tsx
```

### **Success Criteria:**
- [ ] User can generate meal plans through the UI
- [ ] Plans are optimized using NSGA-II algorithm
- [ ] Results are saved to database
- [ ] Pareto front visualization works
- [ ] Plan selection updates user's active meal plan

This template ensures everyone knows exactly what to build and how to integrate with the team!