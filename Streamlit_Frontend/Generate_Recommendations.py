import requests
import json
import logging
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
import time

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
    """Handles communication with the recipe recommendation API"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.predict_url = f"{base_url}/predict"
        self.health_url = f"{base_url}/health"
        self.stats_url = f"{base_url}/stats"
        self.timeout = 30
        
    def check_health(self) -> bool:
        """Check if the API server is healthy"""
        try:
            response = requests.get(self.health_url, timeout=10)
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get API statistics"""
        try:
            response = requests.get(self.stats_url, timeout=10)
            if response.status_code == 200:
                return response.json()
            return {}
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get stats: {e}")
            return {}
    
    def predict(self, request_data: RecipeRequest) -> requests.Response:
        """Make prediction request to API"""
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
            return response
        except requests.exceptions.Timeout:
            logger.error("Request timeout")
            raise
        except requests.exceptions.ConnectionError:
            logger.error("Connection error - check if API server is running")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise

class Generator:
    """
    Main generator class for recipe recommendations
    Handles nutrition input, ingredients, and API communication
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
        api_url: str = "http://127.0.0.1:8000"
    ):
        """
        Initialize the Generator
        
        Args:
            nutrition_input: List of nutrition values in order:
                [Calories, FatContent, SaturatedFatContent, CholesterolContent,
                 SodiumContent, CarbohydrateContent, FiberContent, SugarContent,
                 ProteinContent]
            ingredients: List of ingredient names
            params: Dictionary of parameters for the recommendation algorithm
            api_url: URL of the recommendation API
        """
        self.nutrition_input = nutrition_input or []
        self.ingredients = ingredients or []
        self.params = {**self.DEFAULT_PARAMS, **(params or {})}
        self.api = RecipeAPI(api_url)
        self.last_response = None
        self.last_request_time = None
        
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
            logger.error(f"Expected {len(self.NUTRITION_CATEGORIES)} nutrition values, "
                        f"got {len(self.nutrition_input)}")
            return False
            
        # Check for negative values (some might be acceptable, but warn)
        negatives = [val for val in self.nutrition_input if val < 0]
        if negatives:
            logger.warning(f"Found {len(negatives)} negative nutrition values")
            
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
            if ingredient:  # Skip empty strings
                normalized.append(ingredient.strip().lower())
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
    
    def generate(self, max_retries: int = 3) -> requests.Response:
        """
        Generate recipe recommendations
        
        Args:
            max_retries: Maximum number of retry attempts
            
        Returns:
            requests.Response: API response object
        """
        # Validate input
        if not self.validate_nutrition_input():
            raise ValueError("Invalid nutrition input format")
        
        # Normalize ingredients
        normalized_ingredients = self.normalize_ingredients(self.ingredients)
        
        # Prepare request
        request_data = RecipeRequest(
            nutrition_input=self.nutrition_input,
            ingredients=normalized_ingredients,
            params=self.params
        )
        
        # Try with retries
        for attempt in range(max_retries):
            try:
                logger.info(f"Attempt {attempt + 1}/{max_retries}: "
                          f"Requesting {self.params['n_neighbors']} recommendations")
                
                response = self.api.predict(request_data)
                self.last_response = response
                self.last_request_time = time.time()
                
                if response.status_code == 200:
                    logger.info(f"Successfully received {len(response.json().get('output', []))} recommendations")
                    return response
                else:
                    logger.warning(f"API returned status code {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed on attempt {attempt + 1}: {e}")
                
                # Wait before retry (exponential backoff)
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.info(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    raise
        
        raise Exception(f"Failed to get response after {max_retries} attempts")
    
    def generate_with_fallback(self) -> List[Dict[str, Any]]:
        """
        Generate recommendations with fallback to mock data if API fails
        
        Returns:
            List[Dict[str, Any]]: Recipe recommendations
        """
        try:
            response = self.generate()
            if response.status_code == 200:
                data = response.json()
                return data.get("output", [])
            else:
                logger.warning(f"API returned error, using fallback data")
                return self._get_fallback_recipes()
                
        except Exception as e:
            logger.error(f"Generation failed: {e}, using fallback data")
            return self._get_fallback_recipes()
    
    def _get_fallback_recipes(self) -> List[Dict[str, Any]]:
        """
        Get fallback recipes when API is unavailable
        
        Returns:
            List[Dict[str, Any]]: Fallback recipe data
        """
        # Simple fallback recipes based on common inputs
        fallback_recipes = [
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
            }
        ]
        
        # Filter by ingredients if provided
        if self.ingredients:
            normalized_ingredients = self.normalize_ingredients(self.ingredients)
            filtered_recipes = []
            for recipe in fallback_recipes:
                recipe_ingredients = [ing.lower() for ing in recipe["RecipeIngredientParts"]]
                # Check if any selected ingredient is in recipe
                if any(ing in recipe_ingredients for ing in normalized_ingredients):
                    filtered_recipes.append(recipe)
            
            if filtered_recipes:
                return filtered_recipes[:self.params["n_neighbors"]]
        
        return fallback_recipes[:self.params["n_neighbors"]]
    
    def get_response_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the last response
        
        Returns:
            Dict[str, Any]: Response statistics
        """
        if not self.last_response:
            return {"status": "no_response", "message": "No response generated yet"}
        
        stats = {
            "status_code": self.last_response.status_code,
            "response_time": self.last_request_time,
            "url": self.last_response.url,
            "headers": dict(self.last_response.headers),
        }
        
        if self.last_response.status_code == 200:
            try:
                data = self.last_response.json()
                stats.update({
                    "recipe_count": len(data.get("output", [])),
                    "has_output": "output" in data,
                    "has_errors": "errors" in data,
                    "has_warnings": "warnings" in data,
                })
            except:
                stats["parse_error"] = "Failed to parse JSON response"
        
        return stats
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test connection to API server
        Returns:
            Dict[str, Any]: Connection test results
        """
        results = {
            "api_url": self.api.base_url,
            "health_check": False,
            "api_stats": {},
            "timestamp": time.time(),
        }
        
        try:
            results["health_check"] = self.api.check_health()
            results["api_stats"] = self.api.get_stats()
            results["status"] = "connected" if results["health_check"] else "unhealthy"
        except Exception as e:
            results["status"] = "error"
            results["error"] = str(e)
        
        return results


# ================= TEST & EXAMPLE USAGE =================
if __name__ == "__main__":
    # Example 1: Basic usage
    print("=" * 50)
    print("Example 1: Basic Recipe Generation")
    print("=" * 50)
    
    generator = Generator(
        nutrition_input=[500, 25, 8, 100, 400, 100, 12, 15, 30],
        ingredients=["chicken", "rice", "broccoli"],
        params={"n_neighbors": 3}
    )
    
    # Test connection first
    connection_test = generator.test_connection()
    print("Connection Test:", json.dumps(connection_test, indent=2))
    
    if connection_test.get("health_check"):
        try:
            response = generator.generate()
            print(f"\nStatus Code: {response.status_code}")
            if response.status_code == 200:
                recipes = response.json().get("output", [])
                print(f"Found {len(recipes)} recipes:")
                for i, recipe in enumerate(recipes, 1):
                    print(f"  {i}. {recipe.get('Name', 'Unknown')} - {recipe.get('Calories', 0)} cal")
        except Exception as e:
            print(f"Error: {e}")
            print("Using fallback recipes:")
            fallback = generator.generate_with_fallback()
            for i, recipe in enumerate(fallback, 1):
                print(f"  {i}. {recipe.get('Name', 'Unknown')} - {recipe.get('Calories', 0)} cal")
    else:
        print("API server not available, showing fallback:")
        fallback = generator.generate_with_fallback()
        for i, recipe in enumerate(fallback, 1):
            print(f"  {i}. {recipe.get('Name', 'Unknown')} - {recipe.get('Calories', 0)} cal")
    
    # Example 2: Get ingredient suggestions
    print("\n" + "=" * 50)
    print("Example 2: Ingredient Suggestions")
    print("=" * 50)
    
    print("Vegetable suggestions:", generator.get_ingredient_suggestions("Vegetables")[:5])
    print("Protein suggestions:", generator.get_ingredient_suggestions("Proteins")[:5])
    
    # Example 3: Response statistics
    print("\n" + "=" * 50)
    print("Example 3: Response Statistics")
    print("=" * 50)
    
    stats = generator.get_response_stats()
    print("Response Stats:", json.dumps(stats, indent=2))
    
    # Example 4: Categorized ingredients
    print("\n" + "=" * 50)
    print("Example 4: Ingredient Categories")
    print("=" * 50)
    
    categories = generator.get_categorized_ingredients()
    for category, items in categories.items():
        print(f"{category}: {len(items)} items")
    
    print("\n" + "=" * 50)
    print("Generator initialized successfully!")
    print("=" * 50)