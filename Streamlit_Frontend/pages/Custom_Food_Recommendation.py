import streamlit as st
import pandas as pd
import numpy as np
import time
from Generate_Recommendations import Generator
from ImageFinder.ImageFinder import get_images_links as find_image
from streamlit_echarts import st_echarts

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="Custom Food Recommendation",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ CUSTOM CSS & ANIMATIONS ------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-title {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        font-weight: 700 !important;
        margin-bottom: 2rem !important;
        animation: fadeInDown 1s ease;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    .animate-fadeIn { animation: fadeIn 1s ease; }
    .animate-fadeInUp { animation: fadeInUp 0.8s ease; }
    .animate-fadeInDown { animation: fadeInDown 0.8s ease; }
    .animate-slideInLeft { animation: slideInLeft 0.8s ease; }
    
    .recipe-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border-left: 5px solid #667eea;
    }
    
    .recipe-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .nutrition-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        margin: 2px;
        animation: fadeIn 0.5s ease;
    }
    
    .ingredient-pill {
        display: inline-block;
        background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
        color: #2d5016;
        padding: 6px 15px;
        border-radius: 25px;
        margin: 5px;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease;
    }
    
    .ingredient-pill:hover {
        transform: scale(1.1);
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    .ingredient-pill.selected {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transform: scale(1.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 50px;
        font-weight: 600;
        transition: all 0.3s ease;
        animation: pulse 2s infinite;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
    }
    
    .section-header {
        color: #667eea;
        font-weight: 600;
        margin-top: 30px;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 3px solid #667eea;
    }
    
    .shimmer {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 1000px 100%;
        animation: shimmer 2s infinite;
    }
    
    .success-toast {
        background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
        color: #2d5016;
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        animation: fadeInUp 0.8s ease;
    }
    
    .ingredient-btn {
        width: 100%;
        margin: 5px 0;
    }
    
    .recipe-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 10px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

nutrition_values = [
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

# Common ingredients for quick selection
COMMON_INGREDIENTS = [
    "chicken", "beef", "fish", "shrimp", "egg", 
    "rice", "pasta", "potato", "bread", "flour",
    "tomato", "onion", "garlic", "spinach", "broccoli",
    "carrot", "bell pepper", "mushroom", "cheese", "milk",
    "butter", "oil", "salt", "pepper", "sugar",
    "lemon", "lime", "honey", "soy sauce", "vinegar"
]

# ------------------ SESSION STATE ------------------
if "generated" not in st.session_state:
    st.session_state.generated = False
    st.session_state.recommendations = None
if "selected_ingredients" not in st.session_state:
    st.session_state.selected_ingredients = []

# ------------------ RECOMMENDATION LOGIC ------------------
class Recommendation:
    def __init__(self, nutrition_list, nb_recommendations, ingredients_list):
        self.nutrition_list = nutrition_list
        self.nb_recommendations = nb_recommendations
        self.ingredients_list = ingredients_list

    def generate(self):
        params = {
            "n_neighbors": self.nb_recommendations,
            "return_distance": False,
        }

        generator = Generator(self.nutrition_list, self.ingredients_list, params)
        response = generator.generate()

        if response.status_code != 200:
            return None

        recipes = response.json().get("output", [])

        # Add images with loading animation
        for recipe in recipes:
            recipe["image_link"] = find_image(recipe.get("Name", ""))
            # Simulate some processing delay for animation
            time.sleep(0.01)

        return recipes

# ------------------ DISPLAY LOGIC ------------------
class Display:
    def display_recommendation(self, recommendations):
        st.markdown('<div class="animate-fadeIn">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header animate-slideInLeft">🍽️ Recommended Recipes</h2>', unsafe_allow_html=True)
        
        if not recommendations:
            st.markdown('<div class="animate-fadeInUp">', unsafe_allow_html=True)
            st.error("No recipes found matching your criteria. Try adjusting your nutritional targets or ingredients!")
            st.markdown('</div>', unsafe_allow_html=True)
            return

        # Success message
        st.markdown(f"""
        <div class="success-toast">
            <h3>✨ {len(recommendations)} Recipes Found!</h3>
            <p>Based on your nutritional targets and selected ingredients</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display recipes in a grid
        cols = st.columns(3)
        for idx, recipe in enumerate(recommendations):
            with cols[idx % 3]:
                self._display_recipe_card(recipe, idx)
        
        st.markdown('</div>', unsafe_allow_html=True)

    def _display_recipe_card(self, recipe, index):
        name = recipe.get("Name", "Unknown Recipe")
        
        with st.container():
            st.markdown(f'<div class="recipe-card animate-fadeIn" style="animation-delay: {index*0.1}s">', unsafe_allow_html=True)
            
            # Recipe header with badges
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### {name}")
            with col2:
                st.markdown(f'<span class="nutrition-badge">{recipe.get("Calories", 0)} cal</span>', unsafe_allow_html=True)
            
            # Image - FIXED: Replaced use_column_width with use_container_width
            img = recipe.get("image_link")
            if img:
                st.image(img, use_container_width=True)
            
            # Quick stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Prep Time", f"{recipe.get('PrepTime', 0)} min")
            with col2:
                st.metric("Cook Time", f"{recipe.get('CookTime', 0)} min")
            with col3:
                st.metric("Protein", f"{recipe.get('ProteinContent', 0)}g")
            
            # Expand for details
            with st.expander("View Details"):
                # Nutrition table
                nutrition_df = pd.DataFrame({
                    key: [recipe.get(key, 0)]
                    for key in nutrition_values
                })
                st.markdown("#### 🍎 Nutritional Values")
                st.dataframe(nutrition_df, use_container_width=True)
                
                # Ingredients with pills
                st.markdown("#### 🛒 Ingredients")
                ingredients = recipe.get("RecipeIngredientParts", [])
                if ingredients:
                    cols = st.columns(4)
                    for i, ing in enumerate(ingredients[:12]):  # Limit display
                        with cols[i % 4]:
                            st.markdown(f'<div class="ingredient-pill">{ing}</div>', unsafe_allow_html=True)
                
                # Instructions
                st.markdown("#### 👨‍🍳 Instructions")
                instructions = recipe.get("RecipeInstructions", [])
                for i, step in enumerate(instructions, 1):
                    st.markdown(f"**{i}.** {step}")
            
            st.markdown('</div>', unsafe_allow_html=True)

    def display_overview(self, recommendations):
        if not recommendations:
            return
        
        st.markdown('<div class="animate-fadeIn">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header animate-slideInLeft">📊 Nutrition Overview</h2>', unsafe_allow_html=True)
        
        recipe_names = [r.get("Name", "Unknown") for r in recommendations]
        
        selected_name = st.selectbox(
            "Select a recipe for detailed analysis",
            recipe_names,
            key="overview_recipe_selectbox"
        )
        
        selected_recipe = next(
            r for r in recommendations if r.get("Name") == selected_name
        )
        
        # Create two columns for charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie Chart with colors - FIXED
            pie_data = [
                {"value": selected_recipe.get('ProteinContent', 0), "name": "Protein", "color": "#4ECDC4"},
                {"value": selected_recipe.get('CarbohydrateContent', 0), "name": "Carbs", "color": "#FFD166"},
                {"value": selected_recipe.get('FatContent', 0), "name": "Fat", "color": "#EF476F"},
                {"value": selected_recipe.get('FiberContent', 0), "name": "Fiber", "color": "#06D6A0"},
                {"value": selected_recipe.get('SugarContent', 0), "name": "Sugar", "color": "#118AB2"}
            ]
            
            options_pie = {
                "title": {
                    "text": "Macronutrient Distribution",
                    "subtext": selected_name,
                    "left": "center",
                    "textStyle": {"color": "#333", "fontSize": 16}
                },
                "tooltip": {"trigger": "item", "formatter": "{b}: {c}g ({d}%)"},
                "legend": {
                    "orient": "vertical", 
                    "left": "left",
                    "top": "center",
                    "textStyle": {"color": "#333", "fontSize": 12}
                },
                "series": [
                    {
                        "type": "pie",
                        "radius": ["40%", "70%"],
                        "center": ["50%", "50%"],
                        "data": pie_data,
                        "emphasis": {
                            "itemStyle": {
                                "shadowBlur": 10,
                                "shadowOffsetX": 0,
                                "shadowColor": "rgba(0, 0, 0, 0.5)",
                            }
                        },
                        "itemStyle": {
                            "borderRadius": 8,
                            "borderColor": "#fff",
                            "borderWidth": 2
                        },
                        "label": {
                            "show": True,
                            "formatter": "{b}: {d}%",
                            "color": "#333",
                            "fontSize": 12
                        }
                    }
                ],
            }
            st_echarts(options=options_pie, height="450px")
        
        with col2:
            # Bar Chart for all nutrition values with colors
            bar_data = nutrition_values
            bar_values = [selected_recipe.get(key, 0) for key in bar_data]
            
            # Color mapping for different nutrition categories
            bar_colors = []
            for nutrient in bar_data:
                if "Calories" in nutrient:
                    bar_colors.append("#FF6B6B")
                elif "Protein" in nutrient:
                    bar_colors.append("#4ECDC4")
                elif "Carbohydrate" in nutrient or "Sugar" in nutrient or "Fiber" in nutrient:
                    bar_colors.append("#FFD166")
                elif "Fat" in nutrient:
                    bar_colors.append("#EF476F")
                elif "Cholesterol" in nutrient or "Sodium" in nutrient:
                    bar_colors.append("#06D6A0")
                else:
                    bar_colors.append("#118AB2")
            
            options_bar = {
                "title": {
                    "text": "Detailed Nutrition Profile",
                    "left": "center",
                    "textStyle": {"color": "#333", "fontSize": 16}
                },
                "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
                "xAxis": {
                    "type": "category", 
                    "data": bar_data,
                    "axisLabel": {
                        "rotate": 45,
                        "interval": 0,
                        "fontSize": 10,
                        "color": "#333"
                    }
                },
                "yAxis": {
                    "type": "value",
                    "axisLabel": {"color": "#333"}
                },
                "series": [
                    {
                        "type": "bar",
                        "data": [
                            {"value": val, "itemStyle": {"color": color}}
                            for val, color in zip(bar_values, bar_colors)
                        ],
                        "itemStyle": {
                            "borderRadius": [5, 5, 0, 0],
                            "shadowColor": "rgba(0, 0, 0, 0.1)",
                            "shadowBlur": 5
                        },
                        "barWidth": "60%"
                    }
                ],
            }
            st_echarts(options=options_bar, height="450px")
        
        # Nutrition metrics in a grid with color coding
        st.markdown("#### 📋 Quick Nutrition Facts")
        cols = st.columns(4)
        
        # Define metrics with their colors
        metrics = [
            ("🔥 Calories", selected_recipe.get('Calories', 0), "cal", "#FF6B6B"),
            ("🥩 Protein", selected_recipe.get('ProteinContent', 0), "g", "#4ECDC4"),
            ("🌾 Carbs", selected_recipe.get('CarbohydrateContent', 0), "g", "#FFD166"),
            ("🥑 Fat", selected_recipe.get('FatContent', 0), "g", "#EF476F"),
            ("🍬 Sugar", selected_recipe.get('SugarContent', 0), "g", "#118AB2"),
            ("🌿 Fiber", selected_recipe.get('FiberContent', 0), "g", "#06D6A0"),
            ("🧂 Sodium", selected_recipe.get('SodiumContent', 0), "mg", "#73C6B6"),
            ("❤️ Cholesterol", selected_recipe.get('CholesterolContent', 0), "mg", "#F78FB3"),
        ]
        
        for idx, (label, value, unit, color) in enumerate(metrics):
            with cols[idx % 4]:
                st.markdown(f"""
                <div class="metric-card" style="border-top: 4px solid {color};">
                    <h4 style="color: #333; margin-bottom: 8px;">{label}</h4>
                    <h3 style="color: {color}; margin: 0; font-size: 24px; font-weight: 700;">
                        {value} <span style="font-size: 14px; color: #666;">{unit}</span>
                    </h3>
                </div>
                """, unsafe_allow_html=True)
        
        # Additional nutrition info
        st.markdown("#### 📈 Nutrition Score")
        
        # Calculate a simple health score
        calories = selected_recipe.get('Calories', 0)
        protein = selected_recipe.get('ProteinContent', 0)
        fiber = selected_recipe.get('FiberContent', 0)
        sugar = selected_recipe.get('SugarContent', 0)
        sat_fat = selected_recipe.get('SaturatedFatContent', 0)
        
        # Simple scoring system
        score = 100
        if calories > 800: score -= 20
        elif calories > 500: score -= 10
        
        if protein < 20: score -= 10
        elif protein > 30: score += 10
        
        if fiber < 5: score -= 10
        elif fiber > 10: score += 10
        
        if sugar > 20: score -= 15
        elif sugar > 10: score -= 5
        
        if sat_fat > 10: score -= 10
        
        score = max(0, min(100, score))
        
        # Determine color based on score
        if score >= 80:
            score_color = "#06D6A0"
            score_text = "Excellent"
        elif score >= 60:
            score_color = "#FFD166"
            score_text = "Good"
        else:
            score_color = "#EF476F"
            score_text = "Needs Improvement"
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-card" style="text-align: center; border-top: 4px solid {score_color};">
                <h4 style="color: #333; margin-bottom: 8px;">Health Score</h4>
                <h3 style="color: {score_color}; margin: 0; font-size: 32px; font-weight: 700;">{score}/100</h3>
                <p style="color: {score_color}; margin: 5px 0 0 0; font-weight: 600;">{score_text}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Protein quality indicator
            protein_ratio = protein / max(1, calories/20)  # Simplified protein density
            if protein_ratio > 1.5:
                protein_color = "#06D6A0"
                protein_text = "High"
            elif protein_ratio > 1.0:
                protein_color = "#FFD166"
                protein_text = "Moderate"
            else:
                protein_color = "#EF476F"
                protein_text = "Low"
            
            st.markdown(f"""
            <div class="metric-card" style="text-align: center; border-top: 4px solid {protein_color};">
                <h4 style="color: #333; margin-bottom: 8px;">Protein Density</h4>
                <h3 style="color: {protein_color}; margin: 0; font-size: 28px; font-weight: 700;">{protein_text}</h3>
                <p style="color: #666; margin: 5px 0 0 0; font-size: 12px;">{protein_ratio:.1f}g per 100 cal</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            # Fiber indicator
            fiber_per_cal = (fiber * 100) / max(1, calories)
            if fiber_per_cal > 2:
                fiber_color = "#06D6A0"
                fiber_text = "High"
            elif fiber_per_cal > 1:
                fiber_color = "#FFD166"
                fiber_text = "Moderate"
            else:
                fiber_color = "#EF476F"
                fiber_text = "Low"
            
            st.markdown(f"""
            <div class="metric-card" style="text-align: center; border-top: 4px solid {fiber_color};">
                <h4 style="color: #333; margin-bottom: 8px;">Fiber Content</h4>
                <h3 style="color: {fiber_color}; margin: 0; font-size: 28px; font-weight: 700;">{fiber_text}</h3>
                <p style="color: #666; margin: 5px 0 0 0; font-size: 12px;">{fiber}g total</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------ INGREDIENTS SELECTOR COMPONENT ------------------
def ingredients_selector():
    """Ingredients selector component - must be outside form"""
    st.markdown('<div class="animate-fadeIn">', unsafe_allow_html=True)
    st.markdown("#### 🛒 Select Ingredients")
    
    # Common ingredients grid
    st.markdown("**Common Ingredients:**")
    cols = st.columns(5)
    for idx, ingredient in enumerate(COMMON_INGREDIENTS):
        with cols[idx % 5]:
            if st.button(f"➕ {ingredient}", key=f"ing_{ingredient}", help=f"Add {ingredient}"):
                if ingredient not in st.session_state.selected_ingredients:
                    st.session_state.selected_ingredients.append(ingredient)
                    st.rerun()
    
    # Custom ingredient input
    st.markdown("**Add Custom Ingredient:**")
    col1, col2 = st.columns([3, 1])
    with col1:
        custom_ing = st.text_input(
            "Enter custom ingredient",
            placeholder="e.g., avocado, quinoa, tofu...",
            key="custom_ing_input",
            label_visibility="collapsed"
        )
    with col2:
        if st.button("Add", key="add_custom", help="Add custom ingredient"):
            if custom_ing and custom_ing.strip().lower() not in st.session_state.selected_ingredients:
                st.session_state.selected_ingredients.append(custom_ing.strip().lower())
                st.rerun()
    
    # Selected ingredients display
    if st.session_state.selected_ingredients:
        st.markdown("**Selected Ingredients:**")
        selected_cols = st.columns(4)
        for idx, ing in enumerate(st.session_state.selected_ingredients):
            with selected_cols[idx % 4]:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f'<div class="ingredient-pill selected">{ing}</div>', unsafe_allow_html=True)
                with col2:
                    if st.button("❌", key=f"remove_{ing}", help=f"Remove {ing}"):
                        st.session_state.selected_ingredients.remove(ing)
                        st.rerun()
    
    # Clear all button
    if st.session_state.selected_ingredients:
        if st.button("🗑️ Clear All Ingredients", key="clear_all"):
            st.session_state.selected_ingredients = []
            st.rerun()
    
    # Display selected ingredients as semicolon-separated string
    ingredients_string = ";".join(st.session_state.selected_ingredients)
    
    # Show selected ingredients count
    st.markdown(f"**Selected:** {len(st.session_state.selected_ingredients)} ingredients")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return ingredients_string

# ------------------ UI ------------------
st.markdown('<h1 class="main-title">🍎 Custom Food Recommender</h1>', unsafe_allow_html=True)

display = Display()

# Sidebar for ingredients selection
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    
    # Ingredients selector in sidebar
    st.markdown("### 🛒 Ingredients Selection")
    ingredient_txt = ingredients_selector()
    
    st.markdown("---")
    
    # Recipe options in sidebar
    st.markdown("### ⚙️ Recipe Options")
    nb_recommendations = st.slider(
        "Number of recommendations",
        5, 20, 10, step=1,
        help="Choose how many recipes you want to see",
        key="nb_rec_slider"
    )
    
    add_randomness = st.checkbox(
        "Add randomness to results",
        value=True,
        help="Adds slight variation to get more diverse recipes",
        key="randomness_checkbox"
    )
    
    st.markdown("---")
    
    # Quick tips
    st.markdown("### 💡 Tips")
    st.info("""
    1. Select 2-5 ingredients for best results
    2. Adjust sliders based on your diet goals
    3. Try different combinations
    4. Check the nutrition charts
    """)

# Main content area
tab1, tab2 = st.tabs(["📊 Nutrition Targets", "ℹ️ How It Works"])

with tab1:
    with st.form("recommendation_form"):
        st.markdown('<div class="animate-fadeIn">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header animate-slideInLeft">🎯 Set Your Nutritional Targets</h2>', unsafe_allow_html=True)
        
        # Nutrition sliders in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 🔥 Energy & Fats")
            Calories = st.slider("Calories (kcal)", 0, 2000, 500, key="calories")
            FatContent = st.slider("Total Fat (g)", 0, 100, 50, key="fat")
            SaturatedFatContent = st.slider("Saturated Fat (g)", 0, 50, 10, key="sat_fat")
        
        with col2:
            st.markdown("#### 🩸 Cholesterol & Sodium")
            CholesterolContent = st.slider("Cholesterol (mg)", 0, 300, 50, key="chol")
            SodiumContent = st.slider("Sodium (mg)", 0, 2300, 400, key="sodium")
        
        with col3:
            st.markdown("#### 🌾 Carbs & Protein")
            CarbohydrateContent = st.slider("Carbohydrates (g)", 0, 325, 100, key="carbs")
            FiberContent = st.slider("Fiber (g)", 0, 50, 10, key="fiber")
            SugarContent = st.slider("Sugar (g)", 0, 40, 10, key="sugar")
            ProteinContent = st.slider("Protein (g)", 0, 100, 30, key="protein")
        
        nutrition_list = [
            Calories,
            FatContent,
            SaturatedFatContent,
            CholesterolContent,
            SodiumContent,
            CarbohydrateContent,
            FiberContent,
            SugarContent,
            ProteinContent,
        ]
        
        # Generate button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            generate = st.form_submit_button(
                "🚀 Generate Recommendations",
                use_container_width=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown("""
    ## How It Works
    
    ### 🎯 **Set Nutritional Goals**
    - Adjust sliders to match your dietary requirements
    - Target specific macronutrient ratios
    - Control sodium, cholesterol, and sugar intake
    
    ### 🛒 **Select Ingredients**
    - Choose from common ingredients in the sidebar
    - Add custom ingredients
    - Recipes will include your selected ingredients
    
    ### 🔍 **Get Recommendations**
    - Our AI analyzes thousands of recipes
    - Matches your nutritional targets
    - Filters by your preferred ingredients
    
    ### 📊 **Analyze Results**
    - View detailed nutrition breakdowns
    - Compare recipes side by side
    - Get cooking instructions and ingredient lists
    
    ---
    
    **💡 Tips for Best Results:**
    1. Start with broad targets, then refine
    2. Select 2-5 ingredients for best matches
    3. Use the charts to visualize nutrition
    4. Save your favorite recipes for later
    """)

# ------------------ RUN ------------------
if generate:
    with st.spinner("🧠 Finding perfect recipes for you..."):
        # Show loading animation
        st.markdown('<div class="shimmer" style="height: 100px; border-radius: 10px; margin: 20px 0;"></div>', unsafe_allow_html=True)
        
        # Add small delay for animation
        time.sleep(0.5)
        
        recommender = Recommendation(
            nutrition_list,
            nb_recommendations,
            st.session_state.selected_ingredients,
        )
        st.session_state.recommendations = recommender.generate()
        st.session_state.generated = True
        
        # Show success animation
        st.balloons()
        
        # Rerun to show results
        st.rerun()

if st.session_state.generated:
    display.display_recommendation(st.session_state.recommendations)
    display.display_overview(st.session_state.recommendations)
    
    # Reset button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Generate New Recommendations", use_container_width=True, key="reset_btn"):
            st.session_state.generated = False
            st.session_state.recommendations = None
            st.rerun()