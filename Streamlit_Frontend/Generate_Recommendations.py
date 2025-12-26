import requests
import json
import logging
import time
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
import pandas as pd
import numpy as np
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class RecipeRequest:
    """Data class for recipe request parameters"""
    nutrition_input: List[float]
    ingredients: List[str]
    params: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API request"""
        return {
            "nutrition_input": self.nutrition_input,
            "ingredients": self.ingredients,
            "params": self.params
        }

class RecipeAPI:
    """Handles communication with the recipe recommendation API with fallback"""
    
    def __init__(self, base_url: Optional[str] = None):
        # Use provided URL or try localhost, but always have fallback
        self.base_url = base_url or "http://127.0.0.1:8000"
        self.predict_url = f"{self.base_url}/predict"
        self.health_url = f"{self.base_url}/health"
        self.stats_url = f"{self.base_url}/stats"
        self.timeout = 10  # Reduced timeout for faster fallback
        self.use_api = False  # Will be set based on health check
        
    def check_health(self) -> bool:
        """Check if the API server is healthy - with timeout"""
        try:
            # Try localhost first, but fail fast
            response = requests.get(self.health_url, timeout=5)
            if response.status_code == 200:
                self.use_api = True
                return True
        except (requests.exceptions.ConnectionError, 
                requests.exceptions.Timeout,
                requests.exceptions.RequestException) as e:
            logger.info(f"API health check failed: {e}. Using fallback mode.")
            self.use_api = False
            return False
        return False
    
    def predict(self, request_data: RecipeRequest) -> Dict[str, Any]:
        """
        Make prediction request to API with automatic fallback
        Returns dict instead of Response object for consistency
        """
        if not self.use_api:
            # Already know API is not available
            raise ConnectionError("API server not available. Using fallback mode.")
        
        try:
            response = requests.post(
                url=self.predict_url,
                json=request_data.to_dict(),
                timeout=self.timeout,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise ConnectionError(f"API returned status {response.status_code}")
                
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.RequestException) as e:
            logger.warning(f"API request failed: {e}")
            self.use_api = False  # Disable API for future requests
            raise ConnectionError(f"API connection failed: {e}")

class Generator:
    """
    Main generator class for recipe recommendations
    Handles nutrition input, ingredients, with fallback when API is unavailable
    """
    
    # Default nutrition categories for reference
    NUTRITION_CATEGORIES = [
        "Calories",
        "FatContent",
        "SaturatedFatContent", 
        "CholesterolContent",
        "SodiumContent",
        "CarbohydrateContent",
        "FiberContent",
        "SugarContent",
        "ProteinContent",
    ]
    
    # Popular ingredient categories for suggestions
    INGREDIENT_CATEGORIES = {
        "Proteins": [
            "chicken", "beef", "fish", "shrimp", "egg", "tofu", 
            "lentils", "beans", "pork", "lamb", "turkey", "salmon",
            "tuna", "cod", "tilapia", "shrimp", "prawns", "crab",
            "lobster", "mussels", "clams", "scallops", "tempeh",
            "seitan", "edamame", "chickpeas", "black beans", "kidney beans",
            "pinto beans", "navy beans", "white beans", "ground beef",
            "chicken breast", "chicken thighs", "chicken wings", "duck",
            "goose", "venison", "bison", "rabbit", "quail", "quinoa",
            "soybeans", "peanuts", "almonds", "walnuts", "cashews",
            "pecans", "hazelnuts", "pistachios", "sunflower seeds",
            "pumpkin seeds", "chia seeds", "flax seeds", "hemp seeds"
        ],
        "Vegetables": [
            "broccoli", "spinach", "carrot", "potato", "tomato",
            "onion", "garlic", "bell pepper", "mushroom", "cabbage",
            "cauliflower", "zucchini", "eggplant", "cucumber", "lettuce",
            "kale", "celery", "asparagus", "green beans", "peas",
            "corn", "sweet potato", "pumpkin", "butternut squash",
            "acorn squash", "beets", "radish", "turnip", "parsnip",
            "rutabaga", "artichoke", "brussels sprouts", "bok choy",
            "swiss chard", "collard greens", "mustard greens", "arugula",
            "watercress", "endive", "escarole", "fennel", "leek",
            "shallot", "scallion", "chives", "ginger", "turmeric",
            "jalapeno", "habanero", "serrano", "poblano", "anaheim"
        ],
        "Fruits": [
            "apple", "banana", "orange", "lemon", "lime",
            "strawberry", "blueberry", "raspberry", "blackberry",
            "grape", "watermelon", "melon", "pineapple", "mango",
            "papaya", "kiwi", "peach", "plum", "pear", "cherry",
            "apricot", "fig", "date", "prune", "raisin", "cranberry",
            "pomegranate", "guava", "passion fruit", "dragon fruit",
            "star fruit", "persimmon", "lychee", "rambutan", "durian",
            "jackfruit", "breadfruit", "soursop", "acai", "goji berry"
        ],
        "Grains & Carbs": [
            "rice", "pasta", "bread", "flour", "quinoa", "oats",
            "corn", "barley", "couscous", "bulgur", "farro",
            "spelt", "rye", "millet", "sorghum", "buckwheat",
            "wheat", "semolina", "polenta", "grits", "tapioca",
            "arrowroot", "potato starch", "cornstarch", "breadcrumbs",
            "panko", "crackers", "cereal", "granola", "muesli",
            "popcorn", "tortilla", "wrap", "pita", "naan",
            "bagel", "croissant", "muffin", "pancake", "waffle"
        ],
        "Dairy & Alternatives": [
            "cheese", "milk", "butter", "yogurt", "cream",
            "sour cream", "cream cheese", "mozzarella", "cheddar",
            "parmesan", "ricotta", "feta", "gouda", "brie",
            "camembert", "blue cheese", "swiss cheese", "provolone",
            "monterey jack", "pepper jack", "colby", "havarti",
            "mascarpone", "cottage cheese", "heavy cream",
            "whipping cream", "half and half", "evaporated milk",
            "condensed milk", "buttermilk", "kefir", "greek yogurt",
            "skyrt", "coconut milk", "almond milk", "soy milk",
            "oat milk", "rice milk", "cashew milk", "hemp milk",
            "vegan cheese", "nutritional yeast", "vegan butter"
        ],
        "Seasonings & Oils": [
            "salt", "pepper", "sugar", "honey", "soy sauce",
            "vinegar", "olive oil", "vegetable oil", "canola oil",
            "coconut oil", "avocado oil", "sesame oil", "peanut oil",
            "sunflower oil", "grapeseed oil", "walnut oil",
            "almond oil", "flaxseed oil", "mustard oil",
            "spices", "herbs", "ginger", "garlic powder",
            "onion powder", "paprika", "cumin", "coriander",
            "turmeric", "cinnamon", "nutmeg", "cloves",
            "cardamom", "star anise", "fennel seeds",
            "mustard seeds", "sesame seeds", "poppy seeds",
            "caraway seeds", "celery seeds", "dill seeds",
            "basil", "oregano", "thyme", "rosemary", "sage",
            "parsley", "cilantro", "mint", "chives", "dill",
            "tarragon", "marjoram", "bay leaf", "lemongrass",
            "kaffir lime", "curry leaves", "vanilla", "cocoa",
            "chocolate", "coffee", "tea", "matcha"
        ]
    }
    
    # Default parameters for API requests
    DEFAULT_PARAMS = {
        "n_neighbors": 5,
        "return_distance": False,
        "random_state": 42,
        "algorithm": "auto"
    }
    
    def __init__(
        self,
        nutrition_input: Optional[List[float]] = None,
        ingredients: Optional[List[str]] = None,
        params: Optional[Dict[str, Any]] = None,
        api_url: Optional[str] = None
    ):
        """
        Initialize the Generator
        
        Args:
            nutrition_input: List of nutrition values
            ingredients: List of ingredient names
            params: Dictionary of parameters
            api_url: URL of the recommendation API (optional)
        """
        self.nutrition_input = nutrition_input or []
        self.ingredients = ingredients or []
        self.params = {**self.DEFAULT_PARAMS, **(params or {})}
        
        # Initialize API with automatic fallback detection
        self.api = RecipeAPI(api_url)
        
        # Try to connect to API, but don't fail if unavailable
        try:
            self.api_available = self.api.check_health()
            if self.api_available:
                logger.info("API server is available")
            else:
                logger.info("API server not available, using standalone mode")
        except Exception as e:
            logger.info(f"API check failed: {e}. Using standalone mode.")
            self.api_available = False
        
        self.last_response = None
        self.last_request_time = None
        
        # Initialize recipe database for standalone mode
        self._init_recipe_database()
    
    def _init_recipe_database(self):
        """Initialize recipe database for standalone mode"""
        self.recipe_database = [
            {
                "Name": "Grilled Chicken Bowl",
                "Calories": 450,
                "PrepTime": 15,
                "CookTime": 20,
                "ProteinContent": 35,
                "FatContent": 12,
                "CarbohydrateContent": 40,
                "FiberContent": 8,
                "SugarContent": 5,
                "SaturatedFatContent": 3,
                "CholesterolContent": 85,
                "SodiumContent": 350,
                "RecipeIngredientParts": ["chicken breast", "brown rice", "broccoli", "carrot", "soy sauce"],
                "RecipeInstructions": ["Grill chicken until cooked through", "Cook rice according to package", "Steam vegetables", "Combine all ingredients in bowl", "Add sauce and serve"]
            },
            {
                "Name": "Vegetable Omelette",
                "Calories": 320,
                "PrepTime": 10,
                "CookTime": 10,
                "ProteinContent": 22,
                "FatContent": 18,
                "CarbohydrateContent": 15,
                "FiberContent": 4,
                "SugarContent": 3,
                "SaturatedFatContent": 5,
                "CholesterolContent": 370,
                "SodiumContent": 420,
                "RecipeIngredientParts": ["eggs", "bell pepper", "onion", "spinach", "cheese", "olive oil"],
                "RecipeInstructions": ["Chop vegetables", "Beat eggs in bowl", "Sauté vegetables", "Pour eggs over vegetables", "Cook until set", "Add cheese and fold"]
            },
            {
                "Name": "Rice & Broccoli",
                "Calories": 380,
                "PrepTime": 5,
                "CookTime": 15,
                "ProteinContent": 12,
                "FatContent": 8,
                "CarbohydrateContent": 65,
                "FiberContent": 6,
                "SugarContent": 2,
                "SaturatedFatContent": 1,
                "CholesterolContent": 0,
                "SodiumContent": 280,
                "RecipeIngredientParts": ["rice", "broccoli", "garlic", "soy sauce", "sesame oil"],
                "RecipeInstructions": ["Cook rice", "Steam broccoli", "Sauté garlic", "Combine all ingredients", "Season with soy sauce and sesame oil"]
            },
            {
                "Name": "Salmon with Asparagus",
                "Calories": 420,
                "PrepTime": 10,
                "CookTime": 15,
                "ProteinContent": 38,
                "FatContent": 22,
                "CarbohydrateContent": 18,
                "FiberContent": 6,
                "SugarContent": 4,
                "SaturatedFatContent": 4,
                "CholesterolContent": 95,
                "SodiumContent": 320,
                "RecipeIngredientParts": ["salmon", "asparagus", "lemon", "garlic", "olive oil", "dill"],
                "RecipeInstructions": ["Season salmon", "Roast asparagus", "Pan-sear salmon", "Squeeze lemon", "Garnish with dill"]
            },
            {
                "Name": "Veggie Stir Fry",
                "Calories": 280,
                "PrepTime": 15,
                "CookTime": 10,
                "ProteinContent": 14,
                "FatContent": 10,
                "CarbohydrateContent": 35,
                "FiberContent": 9,
                "SugarContent": 8,
                "SaturatedFatContent": 1,
                "CholesterolContent": 0,
                "SodiumContent": 450,
                "RecipeIngredientParts": ["tofu", "broccoli", "carrot", "bell pepper", "soy sauce", "ginger"],
                "RecipeInstructions": ["Press tofu", "Chop vegetables", "Stir fry tofu", "Add vegetables", "Season with sauce"]
            },
            {
                "Name": "Greek Yogurt Parfait",
                "Calories": 250,
                "PrepTime": 5,
                "CookTime": 0,
                "ProteinContent": 20,
                "FatContent": 5,
                "CarbohydrateContent": 32,
                "FiberContent": 6,
                "SugarContent": 18,
                "SaturatedFatContent": 2,
                "CholesterolContent": 15,
                "SodiumContent": 120,
                "RecipeIngredientParts": ["greek yogurt", "granola", "mixed berries", "honey", "chia seeds"],
                "RecipeInstructions": ["Layer yogurt", "Add granola", "Top with berries", "Drizzle honey", "Sprinkle chia seeds"]
            },
            {
                "Name": "Quinoa Salad",
                "Calories": 320,
                "PrepTime": 20,
                "CookTime": 15,
                "ProteinContent": 18,
                "FatContent": 14,
                "CarbohydrateContent": 38,
                "FiberContent": 7,
                "SugarContent": 5,
                "SaturatedFatContent": 2,
                "CholesterolContent": 0,
                "SodiumContent": 280,
                "RecipeIngredientParts": ["quinoa", "cucumber", "tomato", "red onion", "feta cheese", "olive oil"],
                "RecipeInstructions": ["Cook quinoa", "Chop vegetables", "Mix ingredients", "Add dressing", "Chill before serving"]
            },
            {
                "Name": "Beef and Broccoli",
                "Calories": 380,
                "PrepTime": 15,
                "CookTime": 12,
                "ProteinContent": 42,
                "FatContent": 16,
                "CarbohydrateContent": 22,
                "FiberContent": 5,
                "SugarContent": 6,
                "SaturatedFatContent": 4,
                "CholesterolContent": 105,
                "SodiumContent": 520,
                "RecipeIngredientParts": ["beef strips", "broccoli", "garlic", "ginger", "soy sauce", "sesame oil"],
                "RecipeInstructions": ["Slice beef", "Blanch broccoli", "Stir fry beef", "Add broccoli", "Season with sauce"]
            },
            {
                "Name": "Avocado Toast",
                "Calories": 220,
                "PrepTime": 5,
                "CookTime": 3,
                "ProteinContent": 8,
                "FatContent": 12,
                "CarbohydrateContent": 22,
                "FiberContent": 7,
                "SugarContent": 2,
                "SaturatedFatContent": 2,
                "CholesterolContent": 0,
                "SodiumContent": 180,
                "RecipeIngredientParts": ["whole wheat bread", "avocado", "lemon juice", "salt", "pepper", "red pepper flakes"],
                "RecipeInstructions": ["Toast bread", "Mash avocado", "Add lemon juice", "Spread on toast", "Season to taste"]
            },
            {
                "Name": "Tomato Basil Pasta",
                "Calories": 420,
                "PrepTime": 10,
                "CookTime": 15,
                "ProteinContent": 15,
                "FatContent": 12,
                "CarbohydrateContent": 68,
                "FiberContent": 6,
                "SugarContent": 8,
                "SaturatedFatContent": 2,
                "CholesterolContent": 0,
                "SodiumContent": 320,
                "RecipeIngredientParts": ["pasta", "tomato", "basil", "garlic", "olive oil", "parmesan"],
                "RecipeInstructions": ["Cook pasta", "Chop tomatoes", "Sauté garlic", "Combine ingredients", "Garnish with basil"]
            }
        ]
    
    def set_request(self, 
                   nutrition_input: List[float], 
                   ingredients: List[str], 
                   params: Dict[str, Any]) -> None:
        """
        Set request parameters
        
        Args:
            nutrition_input: Nutrition values
            ingredients: List of ingredients
            params: Algorithm parameters
        """
        self.nutrition_input = nutrition_input
        self.ingredients = ingredients
        self.params = {**self.DEFAULT_PARAMS, **params}
        
    def validate_nutrition_input(self) -> bool:
        """
        Validate nutrition input format
        
        Returns:
            bool: True if valid, False otherwise
        """
        if not self.nutrition_input:
            logger.warning("Nutrition input is empty")
            return False
            
        if len(self.nutrition_input) != len(self.NUTRITION_CATEGORIES):
            logger.warning(f"Expected {len(self.NUTRITION_CATEGORIES)} nutrition values, "
                        f"got {len(self.nutrition_input)}. Using default values if needed.")
            # Pad or truncate to correct length
            if len(self.nutrition_input) < len(self.NUTRITION_CATEGORIES):
                self.nutrition_input = self.nutrition_input + [0] * (len(self.NUTRITION_CATEGORIES) - len(self.nutrition_input))
            else:
                self.nutrition_input = self.nutrition_input[:len(self.NUTRITION_CATEGORIES)]
            
        # Check for negative values (some might be acceptable, but warn)
        negatives = [val for val in self.nutrition_input if val < 0]
        if negatives:
            logger.warning(f"Found {len(negatives)} negative nutrition values. Setting to 0.")
            self.nutrition_input = [max(0, val) for val in self.nutrition_input]
            
        return True
    
    def normalize_ingredients(self, ingredients: List[str]) -> List[str]:
        """
        Normalize ingredient names (lowercase, strip whitespace)
        
        Args:
            ingredients: List of ingredient names
            
        Returns:
            List[str]: Normalized ingredient names
        """
        normalized = []
        for ingredient in ingredients:
            if ingredient and str(ingredient).strip():  # Skip empty strings
                normalized.append(str(ingredient).strip().lower())
        return list(set(normalized))  # Remove duplicates
    
    def get_ingredient_suggestions(self, category: Optional[str] = None) -> List[str]:
        """
        Get ingredient suggestions by category or all
        
        Args:
            category: Optional category name
            
        Returns:
            List[str]: List of ingredient suggestions
        """
        if category and category in self.INGREDIENT_CATEGORIES:
            return self.INGREDIENT_CATEGORIES[category]
        elif category:
            logger.warning(f"Category '{category}' not found")
            return []
        else:
            # Return all ingredients flattened
            all_ingredients = []
            for cat_ingredients in self.INGREDIENT_CATEGORIES.values():
                all_ingredients.extend(cat_ingredients)
            return all_ingredients
    
    def get_categorized_ingredients(self) -> Dict[str, List[str]]:
        """
        Get ingredients organized by category
        
        Returns:
            Dict[str, List[str]]: Categorized ingredients
        """
        return self.INGREDIENT_CATEGORIES.copy()
    
    def _generate_standalone_recommendations(self) -> List[Dict[str, Any]]:
        """
        Generate recommendations using standalone logic (no API)
        
        Returns:
            List[Dict[str, Any]]: Recipe recommendations
        """
        n_neighbors = self.params.get("n_neighbors", 5)
        
        # Filter recipes based on ingredients
        normalized_ingredients = self.normalize_ingredients(self.ingredients)
        
        if normalized_ingredients:
            # Score recipes based on ingredient matches
            scored_recipes = []
            for recipe in self.recipe_database:
                recipe_ingredients = [ing.lower() for ing in recipe["RecipeIngredientParts"]]
                
                # Calculate match score
                matches = sum(1 for ing in normalized_ingredients if any(ing in recipe_ing for recipe_ing in recipe_ingredients))
                score = matches / len(normalized_ingredients) if normalized_ingredients else 0
                
                # Add nutrition similarity score (simplified)
                if self.nutrition_input:
                    cal_diff = abs(recipe.get("Calories", 0) - self.nutrition_input[0]) / max(self.nutrition_input[0], 1)
                    nutrition_score = 1 / (1 + cal_diff)
                    score = (score + nutrition_score) / 2
                
                scored_recipes.append((score, recipe))
            
            # Sort by score and take top N
            scored_recipes.sort(key=lambda x: x[0], reverse=True)
            recommendations = [recipe for _, recipe in scored_recipes[:n_neighbors]]
            
            # Add similarity scores
            for i, recipe in enumerate(recommendations):
                recipe["similarity_score"] = round(0.8 - (i * 0.1), 2)  # Decreasing similarity
        
        else:
            # No ingredients specified, return random selection
            recommendations = random.sample(self.recipe_database, min(n_neighbors, len(self.recipe_database)))
            for i, recipe in enumerate(recommendations):
                recipe["similarity_score"] = round(random.uniform(0.6, 0.9), 2)
        
        return recommendations
    
    def generate(self) -> Dict[str, Any]:
        """
        Generate recipe recommendations with automatic fallback
        
        Returns:
            Dict[str, Any]: Recipe recommendations response
        """
        # Validate input
        if not self.validate_nutrition_input():
            # Use default nutrition values if invalid
            if not self.nutrition_input:
                self.nutrition_input = [500] * len(self.NUTRITION_CATEGORIES)
        
        # Normalize ingredients
        normalized_ingredients = self.normalize_ingredients(self.ingredients)
        
        # Prepare request data
        request_data = RecipeRequest(
            nutrition_input=self.nutrition_input,
            ingredients=normalized_ingredients,
            params=self.params
        )
        
        self.last_request_time = time.time()
        
        # Try API if available
        if self.api_available:
            try:
                logger.info("Attempting API request...")
                response = self.api.predict(request_data)
                self.last_response = response
                self.api_available = True  # API worked, keep it enabled
                
                return {
                    "success": True,
                    "output": response.get("output", []),
                    "metadata": {
                        "source": "api",
                        "api_available": True,
                        "ingredients_used": normalized_ingredients,
                        "nutrition_input": self.nutrition_input
                    }
                }
                
            except ConnectionError as e:
                logger.warning(f"API request failed: {e}")
                self.api_available = False  # Disable API for next time
                # Fall through to standalone mode
        
        # Use standalone mode (fallback)
        logger.info("Using standalone recommendation mode")
        recommendations = self._generate_standalone_recommendations()
        
        return {
            "success": True,
            "output": recommendations,
            "metadata": {
                "source": "standalone",
                "api_available": self.api_available,
                "ingredients_used": normalized_ingredients,
                "nutrition_input": self.nutrition_input,
                "message": "Generated using built-in recipe database"
            }
        }
    
    def get_response_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the last response
        
        Returns:
            Dict[str, Any]: Response statistics
        """
        stats = {
            "api_available": self.api_available,
            "last_request_time": self.last_request_time,
            "mode": "api" if self.api_available else "standalone"
        }
        
        return stats
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test connection to API server
        Returns:
            Dict[str, Any]: Connection test results
        """
        results = {
            "api_url": self.api.base_url,
            "api_available": self.api_available,
            "standalone_mode": not self.api_available,
            "timestamp": time.time(),
            "recipe_database_size": len(self.recipe_database)
        }
        
        return results


# ================= TEST & EXAMPLE USAGE =================
if __name__ == "__main__":
    # Test the generator
    print("=" * 50)
    print("Testing Recipe Generator")
    print("=" * 50)
    
    # Create generator instance
    generator = Generator(
        nutrition_input=[500, 25, 8, 100, 400, 100, 12, 15, 30],
        ingredients=["chicken", "rice", "broccoli"],
        params={"n_neighbors": 3}
    )
    
    # Test connection
    connection_test = generator.test_connection()
    print("Connection Test:", json.dumps(connection_test, indent=2))
    
    # Generate recommendations
    print("\nGenerating recommendations...")
    try:
        result = generator.generate()
        
        if result["success"]:
            print(f"\nSuccess! Generated {len(result['output'])} recipes")
            print(f"Source: {result['metadata']['source']}")
            
            for i, recipe in enumerate(result["output"], 1):
                print(f"\n{i}. {recipe.get('Name', 'Unknown')}")
                print(f"   Calories: {recipe.get('Calories', 0)}")
                print(f"   Protein: {recipe.get('ProteinContent', 0)}g")
                print(f"   Ingredients: {', '.join(recipe.get('RecipeIngredientParts', [])[:3])}...")
        else:
            print("Failed to generate recommendations")
            
    except Exception as e:
        print(f"Error during generation: {e}")
