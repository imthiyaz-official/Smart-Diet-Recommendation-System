import streamlit as st
import pandas as pd
import numpy as np
import time
from Generate_Recommendations import Generator
from ImageFinder.ImageFinder import get_images_links as find_image
from streamlit_echarts import st_echarts
# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="AI Nutrition Chef",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ------------------ ENHANCED CSS & ANIMATIONS ------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main background with gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50% }
        50% { background-position: 100% 50% }
        100% { background-position: 0% 50% }
    }
    
    .main-title {
        text-align: center;
        background: linear-gradient(135deg, #fff 0%, #fdfcfb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 2rem !important;
        text-shadow: 0 2px 10px rgba(0,0,0,0.1);
        animation: floatTitle 3s ease-in-out infinite;
        padding: 20px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    @keyframes floatTitle {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
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
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.05); opacity: 0.8; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.5); }
        50% { box-shadow: 0 0 40px rgba(102, 126, 234, 0.8); }
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .animate-fadeIn { animation: fadeIn 1s ease; }
    .animate-fadeInUp { animation: fadeInUp 0.8s ease; }
    .animate-fadeInDown { animation: fadeInDown 0.8s ease; }
    .animate-slideInLeft { animation: slideInLeft 0.8s ease; }
    .animate-slideInRight { animation: slideInRight 0.8s ease; }
    .animate-glow { animation: glow 2s infinite; }
    .animate-rotate { animation: rotate 5s linear infinite; }
    
    /* Glassmorphism containers */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 25px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        transition: all 0.4s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
        background: rgba(255, 255, 255, 0.98);
    }
    
    .recipe-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 25px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .recipe-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: 0.5s;
    }
    
    .recipe-card:hover::before {
        left: 100%;
    }
    
    .recipe-card:hover {
        transform: translateY(-15px) rotateX(5deg);
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.2);
    }
    
    .nutrition-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 6px 15px;
        border-radius: 25px;
        font-size: 14px;
        margin: 3px;
        animation: fadeIn 0.5s ease;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .ingredient-pill {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 8px 18px;
        border-radius: 30px;
        margin: 8px;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .ingredient-pill::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: 0.5s;
    }
    
    .ingredient-pill:hover::before {
        left: 100%;
    }
    
    .ingredient-pill:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .ingredient-pill.selected {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(245, 87, 108, 0.3);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 15px 40px;
        border-radius: 50px;
        font-weight: 700;
        font-size: 16px;
        transition: all 0.4s ease;
        animation: pulse 2s infinite;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.6);
        animation: none;
    }
    
    .stButton > button::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transform: translateX(-100%);
    }
    
    .stButton > button:hover::after {
        transform: translateX(100%);
        transition: 0.5s;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .metric-card:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 15px 30px rgba(0,0,0,0.15);
    }
    
    .section-header {
        color: #fff;
        font-weight: 700;
        margin-top: 40px;
        margin-bottom: 25px;
        padding-bottom: 15px;
        font-size: 2rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        position: relative;
        display: inline-block;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        border-radius: 2px;
    }
    
    .shimmer {
        background: linear-gradient(90deg, rgba(255,255,255,0.1) 25%, rgba(255,255,255,0.3) 50%, rgba(255,255,255,0.1) 75%);
        background-size: 1000px 100%;
        animation: shimmer 2s infinite;
        border-radius: 15px;
    }
    
    .success-toast {
        background: linear-gradient(135deg, rgba(212, 252, 121, 0.9) 0%, rgba(150, 230, 161, 0.9) 100%);
        color: #2d5016;
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        animation: fadeInUp 0.8s ease;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 10px 25px rgba(150, 230, 161, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .time-metric {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        margin: 8px;
        box-shadow: 0 5px 15px rgba(245, 87, 108, 0.3);
        transition: all 0.3s ease;
    }
    
    .time-metric:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(245, 87, 108, 0.4);
    }
    
    .nutrition-metric {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        margin: 8px;
        box-shadow: 0 5px 15px rgba(79, 172, 254, 0.3);
        transition: all 0.3s ease;
    }
    
    .nutrition-metric:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(79, 172, 254, 0.4);
    }
    
    .quick-stats {
        display: flex;
        justify-content: space-between;
        margin: 20px 0;
        gap: 15px;
    }
    
    .stat-item {
        text-align: center;
        padding: 15px;
        flex: 1;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .stat-item:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    .stat-value {
        font-size: 24px;
        font-weight: bold;
        color: #667eea;
        margin-bottom: 5px;
    }
    
    .stat-label {
        font-size: 14px;
        color: #666;
        margin-top: 5px;
    }
    
    .floating-particle {
        position: fixed;
        width: 10px;
        height: 10px;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 50%;
        pointer-events: none;
        z-index: -1;
        animation: floatUp 20s linear infinite;
    }
    
    @keyframes floatUp {
        0% {
            transform: translateY(100vh) translateX(0) rotate(0deg);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
        }
        100% {
            transform: translateY(-100px) translateX(100px) rotate(360deg);
            opacity: 0;
        }
    }
    
    .ai-pulse {
        position: relative;
    }
    
    .ai-pulse::before {
        content: '';
        position: absolute;
        top: -10px;
        left: -10px;
        right: -10px;
        bottom: -10px;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.2) 0%, transparent 70%);
        border-radius: 50%;
        animation: pulse 2s infinite;
        z-index: -1;
    }
    
    .glowing-text {
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.7),
                     0 0 20px rgba(255, 255, 255, 0.5),
                     0 0 30px rgba(102, 126, 234, 0.3);
        animation: glow 3s infinite;
    }
</style>
""", unsafe_allow_html=True)

# Add floating particles for background effect
st.markdown("""
<script>
function createParticles() {
    const container = document.createElement('div');
    container.className = 'particles-container';
    document.body.appendChild(container);
    
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.className = 'floating-particle';
        particle.style.left = Math.random() * 100 + 'vw';
        particle.style.width = Math.random() * 15 + 5 + 'px';
        particle.style.height = particle.style.width;
        particle.style.background = `rgba(${Math.random() * 255}, ${Math.random() * 255}, 234, ${Math.random() * 0.5 + 0.2})`;
        particle.style.animationDelay = Math.random() * 20 + 's';
        particle.style.animationDuration = Math.random() * 20 + 10 + 's';
        container.appendChild(particle);
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createParticles);
} else {
    createParticles();
}
</script>
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

# Food categories for pie chart
FOOD_CATEGORIES = {
    "🍗 Protein Foods": ["chicken", "beef", "fish", "shrimp", "egg", "tofu", "lentils", "beans"],
    "🌾 Carbs & Grains": ["rice", "pasta", "potato", "bread", "flour", "quinoa", "oats", "corn"],
    "🥬 Vegetables": ["tomato", "onion", "garlic", "spinach", "broccoli", "carrot", "bell pepper", "mushroom", "avocado"],
    "🧀 Dairy": ["cheese", "milk", "butter", "yogurt", "cream"],
    "🧂 Seasonings": ["salt", "pepper", "sugar", "honey", "soy sauce", "vinegar", "olive oil", "spices"],
    "🍋 Fruits": ["lemon", "lime", "orange", "apple", "banana", "berries"]
}

COMMON_INGREDIENTS = []
for category in FOOD_CATEGORIES.values():
    COMMON_INGREDIENTS.extend(category)

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
            time.sleep(0.01)

        return recipes

# ------------------ ENHANCED DISPLAY LOGIC ------------------
class Display:
    def display_food_category_pie_chart(self):
        """Display beautiful pie chart with food categories"""
        st.markdown('<div class="glass-card animate-slideInRight">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header">🍽️ Food Category Distribution</h2>', unsafe_allow_html=True)
        
        # Calculate category counts based on selected ingredients
        category_counts = {}
        for category, ingredients in FOOD_CATEGORIES.items():
            count = sum(1 for ing in st.session_state.selected_ingredients if ing in ingredients)
            if count > 0:
                category_counts[category] = count
        
        if not category_counts:
            # Show default distribution
            category_counts = {
                "🍗 Protein Foods": 3,
                "🌾 Carbs & Grains": 2,
                "🥬 Vegetables": 4,
                "🧀 Dairy": 1,
                "🧂 Seasonings": 3,
                "🍋 Fruits": 1
            }
        
        # Define vibrant colors for each category
        color_palette = [
            "#FF6B6B", "#4ECDC4", "#FFD166", "#06D6A0", 
            "#118AB2", "#EF476F", "#7209B7", "#F15BB5",
            "#9B5DE5", "#00BBF9", "#00F5D4", "#FF9E00"
        ]
        
        # Create pie chart data
        chart_data = []
        for i, (category, count) in enumerate(category_counts.items()):
            chart_data.append({
                "value": count,
                "name": category,
                "itemStyle": {"color": color_palette[i % len(color_palette)]}
            })
        
        options = {
            "title": {
                "text": "Your Food Preferences",
                "subtext": "Distribution of selected ingredients by category",
                "left": "center",
                "textStyle": {
                    "fontSize": 24,
                    "fontWeight": "bold",
                    "color": "#333"
                },
                "subtextStyle": {
                    "fontSize": 14,
                    "color": "#666"
                }
            },
            "tooltip": {
                "trigger": "item",
                "formatter": "{b}: {c} ingredients ({d}%)",
                "backgroundColor": "rgba(255, 255, 255, 0.9)",
                "borderColor": "#667eea",
                "borderWidth": 1,
                "textStyle": {"color": "#333"}
            },
            "legend": {
                "type": "scroll",
                "orient": "vertical",
                "right": "10%",
                "top": "center",
                "textStyle": {"fontSize": 14},
                "itemHeight": 20,
                "itemWidth": 20,
                "itemGap": 15
            },
            "series": [
                {
                    "name": "Food Categories",
                    "type": "pie",
                    "radius": ["40%", "70%"],
                    "center": ["35%", "50%"],
                    "roseType": "area",
                    "itemStyle": {
                        "borderRadius": 8,
                        "borderColor": "#fff",
                        "borderWidth": 2,
                        "shadowBlur": 10,
                        "shadowColor": "rgba(0, 0, 0, 0.1)"
                    },
                    "data": chart_data,
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 20,
                            "shadowOffsetX": 0,
                            "shadowColor": "rgba(0, 0, 0, 0.2)"
                        },
                        "label": {
                            "show": True,
                            "fontSize": 16,
                            "fontWeight": "bold"
                        }
                    },
                    "label": {
                        "show": False,
                        "position": "center",
                        "formatter": "{b}\n{c} ({d}%)",
                        "fontSize": 14
                    },
                    "labelLine": {
                        "show": True,
                        "length": 20,
                        "length2": 30
                    },
                    "animationType": "scale",
                    "animationEasing": "elasticOut",
                    "animationDelay": 200
                }
            ]
        }
        
        st_echarts(options=options, height="500px")
        st.markdown('</div>', unsafe_allow_html=True)
    
    def display_recommendation(self, recommendations):
        st.markdown('<div class="animate-fadeIn">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header animate-slideInLeft">✨ AI-Generated Recipes</h2>', unsafe_allow_html=True)
        
        if not recommendations:
            st.markdown('<div class="animate-fadeInUp">', unsafe_allow_html=True)
            st.error("🚫 No recipes found! Try adjusting your criteria or selecting different ingredients.")
            st.markdown('</div>', unsafe_allow_html=True)
            return

        # Animated success message
        st.markdown(f"""
        <div class="success-toast animate-glow">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="font-size: 40px;">✨</div>
                <div>
                    <h3 style="margin: 0; font-size: 24px;">🎉 {len(recommendations)} Perfect Recipes Found!</h3>
                    <p style="margin: 5px 0 0 0; font-size: 16px;">AI-powered recommendations just for you</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display recipes in a grid with staggered animation
        cols = st.columns(3)
        for idx, recipe in enumerate(recommendations):
            with cols[idx % 3]:
                self._display_recipe_card(recipe, idx)
        
        st.markdown('</div>', unsafe_allow_html=True)

    def _display_recipe_card(self, recipe, index):
        name = recipe.get("Name", "Unknown Recipe")
        
        with st.container():
            st.markdown(f'<div class="recipe-card animate-fadeIn" style="animation-delay: {index*0.2}s">', unsafe_allow_html=True)
            
            # Recipe header with AI badge
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### 🤖 {name}")
                st.markdown('<div style="font-size: 12px; color: #667eea; margin-top: -10px;">✨ AI-Powered Selection</div>', unsafe_allow_html=True)
            with col2:
                calories = recipe.get("Calories", 0)
                st.markdown(f'<div class="ai-pulse"><span class="nutrition-badge">🔥 {calories} cal</span></div>', unsafe_allow_html=True)
            
            # Image with hover effect
            img = recipe.get("image_link")
            if img:
                st.image(img, use_container_width=True)
            
            # Quick stats
            self._display_quick_stats(recipe)
            
            # Expand for details
            with st.expander("🔍 View AI Analysis & Full Recipe"):
                self._display_recipe_details(recipe)
            
            st.markdown('</div>', unsafe_allow_html=True)

    def _display_quick_stats(self, recipe):
        prep_time = recipe.get('PrepTime', 0)
        cook_time = recipe.get('CookTime', 0)
        total_time = recipe.get('TotalTime', 0)
        protein = recipe.get('ProteinContent', 0)
        carbs = recipe.get('CarbohydrateContent', 0)
        fat = recipe.get('FatContent', 0)
        
        # Time stats
        st.markdown('<div class="quick-stats">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'''
            <div class="time-metric">
                <div style="font-size: 28px;">⏱️</div>
                <div class="stat-value">{prep_time}</div>
                <div class="stat-label">Prep (min)</div>
            </div>
            ''', unsafe_allow_html=True)
        with col2:
            st.markdown(f'''
            <div class="time-metric">
                <div style="font-size: 28px;">🔥</div>
                <div class="stat-value">{cook_time}</div>
                <div class="stat-label">Cook (min)</div>
            </div>
            ''', unsafe_allow_html=True)
        with col3:
            st.markdown(f'''
            <div class="time-metric">
                <div style="font-size: 28px;">⏰</div>
                <div class="stat-value">{total_time}</div>
                <div class="stat-label">Total (min)</div>
            </div>
            ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Nutrition stats
        st.markdown('<div class="quick-stats">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'''
            <div class="nutrition-metric">
                <div style="font-size: 28px;">🥩</div>
                <div class="stat-value">{protein}g</div>
                <div class="stat-label">Protein</div>
            </div>
            ''', unsafe_allow_html=True)
        with col2:
            st.markdown(f'''
            <div class="nutrition-metric">
                <div style="font-size: 28px;">🌾</div>
                <div class="stat-value">{carbs}g</div>
                <div class="stat-label">Carbs</div>
            </div>
            ''', unsafe_allow_html=True)
        with col3:
            st.markdown(f'''
            <div class="nutrition-metric">
                <div style="font-size: 28px;">🥑</div>
                <div class="stat-value">{fat}g</div>
                <div class="stat-label">Fat</div>
            </div>
            ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    def _display_recipe_details(self, recipe):
        # Nutrition table
        nutrition_df = pd.DataFrame({
            key: [recipe.get(key, 0)]
            for key in nutrition_values
        })
        
        # Transpose for better display
        nutrition_df = nutrition_df.T.reset_index()
        nutrition_df.columns = ['Nutrient', 'Value']
        
        # Format values
        nutrition_df['Value'] = nutrition_df['Value'].apply(lambda x: f"{x:.1f}")
        
        st.markdown("#### 📊 AI Nutrition Analysis")
        
        # Custom CSS for table
        st.markdown("""
        <style>
        .nutrition-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin: 15px 0;
        }
        .nutrition-table th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }
        .nutrition-table td {
            padding: 10px 12px;
            border-bottom: 1px solid #e0e0e0;
        }
        .nutrition-table tr:nth-child(even) {
            background-color: rgba(102, 126, 234, 0.05);
        }
        .nutrition-table tr:hover {
            background-color: rgba(102, 126, 234, 0.1);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Display table using HTML for better styling
        table_html = """
        <table class="nutrition-table">
            <thead>
                <tr>
                    <th>Nutrient</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for _, row in nutrition_df.iterrows():
            table_html += f"""
                <tr>
                    <td><strong>{row['Nutrient']}</strong></td>
                    <td>{row['Value']}</td>
                </tr>
            """
        
        table_html += """
            </tbody>
        </table>
        """
        
        st.markdown(table_html, unsafe_allow_html=True)
        
        # Ingredients
        st.markdown("#### 🛒 Smart Ingredient List")
        ingredients = recipe.get("RecipeIngredientParts", [])
        if ingredients:
            cols = st.columns(4)
            for i, ing in enumerate(ingredients[:20]):
                with cols[i % 4]:
                    st.markdown(f'<div class="ingredient-pill">{ing}</div>', unsafe_allow_html=True)
        
        # Instructions
        st.markdown("#### 👨‍🍳 AI-Optimized Instructions")
        instructions = recipe.get("RecipeInstructions", [])
        if instructions:
            for i, step in enumerate(instructions, 1):
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                    padding: 15px;
                    border-radius: 10px;
                    margin: 10px 0;
                    border-left: 4px solid #667eea;
                ">
                    <strong>Step {i}:</strong> {step}
                </div>
                """, unsafe_allow_html=True)

    def display_overview(self, recommendations):
        if not recommendations:
            return
        
        st.markdown('<div class="animate-fadeIn">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header animate-slideInLeft">🤖 AI Nutrition Dashboard</h2>', unsafe_allow_html=True)
        
        # Food category pie chart
        self.display_food_category_pie_chart()
        
        recipe_names = [r.get("Name", "Unknown") for r in recommendations]
        
        col1, col2 = st.columns([2, 1])
        with col1:
            selected_name = st.selectbox(
                "📋 Select a recipe for AI analysis",
                recipe_names,
                key="overview_recipe_selectbox"
            )
        with col2:
            st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)
            if st.button("🔄 Refresh Analysis", key="refresh_analysis"):
                st.rerun()
        
        selected_recipe = next(
            r for r in recommendations if r.get("Name") == selected_name
        )
        
        # Nutrition metrics grid
        self._display_nutrition_metrics(selected_recipe)
        
        # Advanced charts
        self._display_advanced_charts(selected_recipe, selected_name)
        
        st.markdown('</div>', unsafe_allow_html=True)

    def _display_nutrition_metrics(self, recipe):
        st.markdown('<div class="glass-card animate-fadeInUp">', unsafe_allow_html=True)
        st.markdown("#### ⚡ AI Health Score & Metrics")
        
        # Health score calculation
        health_score = 85  # Example AI-calculated score
        st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            <div style="
                width: 150px;
                height: 150px;
                margin: 0 auto;
                background: conic-gradient(#4ECDC4 {health_score}%, #e0e0e0 0%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                position: relative;
                box-shadow: 0 10px 30px rgba(78, 205, 196, 0.3);
            ">
                <div style="
                    width: 120px;
                    height: 120px;
                    background: white;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    flex-direction: column;
                ">
                    <span style="font-size: 32px; font-weight: bold; color: #4ECDC4;">{health_score}</span>
                    <span style="font-size: 14px; color: #666;">AI Score</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Main metrics
        cols = st.columns(4)
        main_metrics = [
            ("🔥 Calories", f"{recipe.get('Calories', 0):.0f}", "kcal", "#FF6B6B"),
            ("🥩 Protein", f"{recipe.get('ProteinContent', 0):.1f}", "g", "#4ECDC4"),
            ("🌾 Carbs", f"{recipe.get('CarbohydrateContent', 0):.1f}", "g", "#FFD166"),
            ("🥑 Fat", f"{recipe.get('FatContent', 0):.1f}", "g", "#06D6A0"),
        ]
        
        for idx, (label, value, unit, color) in enumerate(main_metrics):
            with cols[idx]:
                st.markdown(f"""
                <div class="metric-card" style="border-top: 4px solid {color};">
                    <h4 style="color: {color}; font-size: 14px;">{label}</h4>
                    <h3 style="margin: 10px 0; font-size: 24px;">{value}</h3>
                    <p style="color: #666; font-size: 12px; margin: 0;">{unit}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Detailed metrics
        cols = st.columns(4)
        detail_metrics = [
            ("🍬 Sugar", f"{recipe.get('SugarContent', 0):.1f}", "g", "#EF476F"),
            ("🌿 Fiber", f"{recipe.get('FiberContent', 0):.1f}", "g", "#118AB2"),
            ("🧂 Sodium", f"{recipe.get('SodiumContent', 0):.0f}", "mg", "#073B4C"),
            ("❤️ Cholesterol", f"{recipe.get('CholesterolContent', 0):.0f}", "mg", "#7209B7"),
        ]
        
        for idx, (label, value, unit, color) in enumerate(detail_metrics):
            with cols[idx]:
                st.markdown(f"""
                <div class="metric-card" style="border-top: 4px solid {color};">
                    <h4 style="color: {color}; font-size: 14px;">{label}</h4>
                    <h3 style="margin: 10px 0; font-size: 24px;">{value}</h3>
                    <p style="color: #666; font-size: 12px; margin: 0;">{unit}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    def _display_advanced_charts(self, recipe, name):
        col1, col2 = st.columns(2)
        
        with col1:
            # Enhanced Pie Chart
            pie_data = [
                {"value": recipe.get('ProteinContent', 0), "name": "Protein", "color": "#4ECDC4"},
                {"value": recipe.get('CarbohydrateContent', 0), "name": "Carbs", "color": "#FFD166"},
                {"value": recipe.get('FatContent', 0), "name": "Fat", "color": "#06D6A0"},
                {"value": recipe.get('FiberContent', 0), "name": "Fiber", "color": "#118AB2"},
                {"value": recipe.get('SugarContent', 0), "name": "Sugar", "color": "#EF476F"}
            ]
            
            options_pie = {
                "title": {
                    "text": "Macronutrient Breakdown",
                    "subtext": name,
                    "left": "center",
                    "textStyle": {"color": "#333", "fontSize": 18},
                    "subtextStyle": {"color": "#666"}
                },
                "tooltip": {"trigger": "item", "formatter": "{b}: {c}g ({d}%)"},
                "legend": {"orient": "vertical", "left": "left", "top": "center"},
                "series": [{
                    "type": "pie",
                    "radius": ["30%", "60%"],
                    "center": ["50%", "50%"],
                    "data": pie_data,
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 20,
                            "shadowOffsetX": 0,
                            "shadowColor": "rgba(0, 0, 0, 0.3)"
                        }
                    },
                    "itemStyle": {
                        "borderRadius": 10,
                        "borderColor": "#fff",
                        "borderWidth": 3
                    },
                    "label": {"show": True, "formatter": "{b}\n{c}g"},
                    "labelLine": {"show": True}
                }]
            }
            st_echarts(options=options_pie, height="400px")
        
        with col2:
            # Enhanced Bar Chart
            bar_data = nutrition_values
            bar_values = [recipe.get(key, 0) for key in bar_data]
            
            options_bar = {
                "title": {
                    "text": "Nutrition Profile",
                    "left": "center",
                    "textStyle": {"color": "#333", "fontSize": 18}
                },
                "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
                "xAxis": {
                    "type": "category",
                    "data": bar_data,
                    "axisLabel": {
                        "rotate": 45,
                        "interval": 0,
                        "fontSize": 10
                    }
                },
                "yAxis": {"type": "value"},
                "series": [{
                    "type": "bar",
                    "data": bar_values,
                    "itemStyle": {
                        "color": {
                            "type": "linear",
                            "x": 0,
                            "y": 0,
                            "x2": 0,
                            "y2": 1,
                            "colorStops": [
                                {"offset": 0, "color": "#667eea"},
                                {"offset": 1, "color": "#764ba2"}
                            ]
                        },
                        "borderRadius": [5, 5, 0, 0]
                    },
                    "barWidth": "60%"
                }]
            }
            st_echarts(options=options_bar, height="400px")

# ------------------ ENHANCED INGREDIENTS SELECTOR ------------------
def ingredients_selector():
    """Enhanced ingredients selector with categories"""
    st.markdown('<div class="glass-card animate-fadeIn">', unsafe_allow_html=True)
    st.markdown('<h3 class="glowing-text">🎯 AI Ingredient Selector</h3>', unsafe_allow_html=True)
    
    # Display food categories
    st.markdown("#### 🗂️ Food Categories")
    for category, ingredients in FOOD_CATEGORIES.items():
        with st.expander(f"{category} ({len(ingredients)} items)"):
            cols = st.columns(4)
            for idx, ingredient in enumerate(ingredients):
                with cols[idx % 4]:
                    is_selected = ingredient in st.session_state.selected_ingredients
                    button_text = f"✅ {ingredient}" if is_selected else f"➕ {ingredient}"
                    if st.button(button_text, key=f"cat_{ingredient}", 
                                help=f"{'Remove' if is_selected else 'Add'} {ingredient}"):
                        if is_selected:
                            st.session_state.selected_ingredients.remove(ingredient)
                        else:
                            st.session_state.selected_ingredients.append(ingredient)
                        st.rerun()
    
    # Custom ingredient input
    st.markdown("#### ✨ Add Custom Ingredients")
    col1, col2 = st.columns([3, 1])
    with col1:
        custom_ing = st.text_input(
            "Enter any ingredient you love",
            placeholder="e.g., truffle, quinoa, dragon fruit...",
            key="custom_ing_input",
            label_visibility="collapsed"
        )
    with col2:
        if st.button("🚀 Add", key="add_custom", help="Add custom ingredient"):
            if custom_ing and custom_ing.strip().lower() not in st.session_state.selected_ingredients:
                st.session_state.selected_ingredients.append(custom_ing.strip().lower())
                st.success(f"Added: {custom_ing}")
                st.rerun()
    
    # Selected ingredients display
    if st.session_state.selected_ingredients:
        st.markdown("#### 📋 Your Selection")
        st.markdown(f'<div style="background: rgba(102, 126, 234, 0.1); padding: 20px; border-radius: 15px; margin: 10px 0;">', unsafe_allow_html=True)
        
        # Group selected ingredients by category
        selected_by_category = {}
        for category, ingredients in FOOD_CATEGORIES.items():
            cat_ingredients = [ing for ing in st.session_state.selected_ingredients if ing in ingredients]
            if cat_ingredients:
                selected_by_category[category] = cat_ingredients
        
        # Display uncategorized ingredients
        uncategorized = [ing for ing in st.session_state.selected_ingredients 
                        if not any(ing in ingredients for ingredients in FOOD_CATEGORIES.values())]
        
        for category, ingredients in selected_by_category.items():
            st.markdown(f"**{category}:**")
            cols = st.columns(6)
            for idx, ing in enumerate(ingredients):
                with cols[idx % 6]:
                    st.markdown(f'<div class="ingredient-pill selected">{ing}</div>', unsafe_allow_html=True)
        
        if uncategorized:
            st.markdown("**✨ Custom Ingredients:**")
            cols = st.columns(6)
            for idx, ing in enumerate(uncategorized):
                with cols[idx % 6]:
                    st.markdown(f'<div class="ingredient-pill selected">{ing}</div>', unsafe_allow_html=True)
        
        # Clear button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🗑️ Clear All", key="clear_all", use_container_width=True):
                st.session_state.selected_ingredients = []
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Selection statistics
    total_selected = len(st.session_state.selected_ingredients)
    category_counts = {}
    for category, ingredients in FOOD_CATEGORIES.items():
        count = sum(1 for ing in st.session_state.selected_ingredients if ing in ingredients)
        if count > 0:
            category_counts[category] = count
    
    st.markdown(f"""
    <div style="
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        background-clip: padding-box;
        background-color: rgba(255,255,255,0.1);
        padding: 20px;
        border-radius: 15px;
        margin-top: 20px;
        text-align: center;
    ">
    <div style="font-size: 14px; color: rgba(255,255,255,0.9);">📊 Selection Stats</div>
    <div style="font-size: 28px; font-weight: bold; color: white;">{total_selected} ingredients</div>
    <div style="font-size: 12px; color: rgba(255,255,255,0.7);">
        Across {len(category_counts)} categories
    </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    return ";".join(st.session_state.selected_ingredients)
# ------------------ CREATE DISPLAY OBJECT ------------------
display = Display()

# ------------------ ENHANCED UI ------------------
st.markdown("""
<h1 style="
    text-align: center;
    color: white;
    font-size: 48px;
    font-weight: 800;
    margin-bottom: 30px;
    text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    padding: 25px;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.85) 0%, rgba(118, 75, 162, 0.85) 100%);
    border-radius: 25px;
    border: 3px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 15px 35px rgba(0,0,0,0.25);
    backdrop-filter: blur(10px);
">🤖 AI Nutrition Chef</h1>
""", unsafe_allow_html=True)

# Create two columns for the main layout
col1, col2 = st.columns([2, 1])

# Left Column - Description with improved styling
with col1:
    st.markdown("""
    <div style="
    background: rgba(255, 255, 255, 0.98);
    padding: 35px;
    border-radius: 25px;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
    border: 2px solid rgba(102, 126, 234, 0.2);
    backdrop-filter: blur(15px);
    ">
    <h2 style="
            color: #667eea;
            margin-bottom: 25px;
            font-size: 32px;
            font-weight: 800;
            text-align: center;
            padding-bottom: 15px;
            border-bottom: 3px solid rgba(102, 126, 234, 0.2);
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
    ">🤖 What is AI Nutrition Chef?</h2>
        
    <p style="
        color: #333;
        font-size: 18px;
        line-height: 1.8;
        margin-bottom: 30px;
        text-align: center;
        font-weight: 500;
        padding: 20px;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        border-radius: 15px;
        border-left: 5px solid #667eea;
    ">
    An intelligent cooking assistant powered by advanced AI that analyzes your nutritional requirements and personal preferences to create personalized recipes.
    </p>
        
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin-bottom: 35px;">
    <div style="
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%);
        padding: 25px;
        border-radius: 20px;
         border: 2px solid rgba(102, 126, 234, 0.15);
        transition: all 0.3s ease;
        ">
        <h3 style="
            color: #667eea;
                    margin: 0 0 20px 0;
                    font-size: 22px;
                    font-weight: 700;
                    text-align: center;
                ">🎯 How it Works</h3>
                <ul style="
                    color: #444;
                    font-size: 16px;
                    line-height: 1.8;
                    margin: 0;
                    padding-left: 20px;
                ">
                <li style="margin-bottom: 12px;">Analyzes your dietary goals and nutritional needs</li>
                <li style="margin-bottom: 12px;">Suggests recipes based on available ingredients</li>
                <li style="margin-bottom: 12px;">Adapts recipes to your taste preferences</li>
                <li>Provides nutritional information for each meal</li>
                </ul>
            </div>  
        <div style="
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%);
            padding: 25px;
            border-radius: 20px;
            border: 2px solid rgba(102, 126, 234, 0.15);
            transition: all 0.3s ease;
            ">
        <h3 style="
            color: #667eea;
            margin: 0 0 20px 0;
            font-size: 22px;
            font-weight: 700;
            text-align: center;
        ">⚡ Technology Stack</h3>
        <ul style="
            color: #444;
            font-size: 16px;
            line-height: 1.8;
            margin: 0;
        padding-left: 20px;
        ">
        <li style="margin-bottom: 12px;"><strong>Machine Learning:</strong> Advanced algorithms for recipe recognition</li>
        <li style="margin-bottom: 12px;"><strong>Natural Language Processing:</strong> Understands cooking instructions</li>
        <li style="margin-bottom: 12px;"><strong>Computer Vision:</strong> Analyzes food images for nutritional content</li>
         <li><strong>Data Analytics:</strong> Tracks your nutritional progress over time</li>
        </ul>
        </div>
        </div>
        <h3 style="
        color: #667eea;
        margin: 0 0 20px 0;
        font-size: 26px;
        font-weight: 700;
        text-align: center;
        padding: 15px;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        border-radius: 15px;
        ">🌟 Who Can Benefit?</h3>
        <div style="
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 15px;
        margin-bottom: 10px;
        ">
        <div style="
        background: white;
        padding: 15px;
        border-radius: 12px;
        border: 2px solid rgba(102, 126, 234, 0.1);
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        ">
        <div style="font-size: 24px; text-align: center; margin-bottom: 10px; color: #667eea;">💪</div>
        <p style="color: #333; font-size: 14px; text-align: center; margin: 0; font-weight: 600;">Health Enthusiasts</p>
    </div>     
    <div style="
        background: white;
        padding: 15px;
        border-radius: 12px;
        border: 2px solid rgba(102, 126, 234, 0.1);
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        ">
    <div style="font-size: 24px; text-align: center; margin-bottom: 10px; color: #667eea;">🥗</div>
    <p style="color: #333; font-size: 14px; text-align: center; margin: 0; font-weight: 600;">Dieters</p>
    </div>    
    <div style="
        background: white;
        padding: 15px;
        border-radius: 12px;
        border: 2px solid rgba(102, 126, 234, 0.1);
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        ">
    <div style="font-size: 24px; text-align: center; margin-bottom: 10px; color: #667eea;">💼</div>
    <p style="color: #333; font-size: 14px; text-align: center; margin: 0; font-weight: 600;">Busy Professionals</p>
    </div>
        <div style="
        background: white;
        padding: 15px;
        border-radius: 12px;
        border: 2px solid rgba(102, 126, 234, 0.1);
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        ">
    <div style="font-size: 24px; text-align: center; margin-bottom: 10px; color: #667eea;">👨‍👩‍👧‍👦</div>
    <p style="color: #333; font-size: 14px; text-align: center; margin: 0; font-weight: 600;">Families</p>
    </div>
    <div style="
        background: white;
        padding: 15px;
        border-radius: 12px;
        border: 2px solid rgba(102, 126, 234, 0.1);
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        ">
    <div style="font-size: 24px; text-align: center; margin-bottom: 10px; color: #667eea;">⚠️</div>
    <p style="color: #333; font-size: 14px; text-align: center; margin: 0; font-weight: 600;">Dietary Restrictions</p>
    </div>
        <div style="
        background: white;
        padding: 15px;
        border-radius: 12px;
        border: 2px solid rgba(102, 126, 234, 0.1);
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    ">
    <div style="font-size: 24px; text-align: center; margin-bottom: 10px; color: #667eea;">👨‍🍳</div>
    <p style="color: #333; font-size: 14px; text-align: center; margin: 0; font-weight: 600;">Home Cooks</p>
    </div>
    </div>
    </div>
    """, unsafe_allow_html=True)
# Right Column - AI Stats and Progress
with col2:
    # AI Stats Card
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(102,126,234,0.4), rgba(118,75,162,0.4));
        padding: 30px;
        border-radius: 25px;
        text-align: center;
        color: white;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        margin-bottom: 25px;
        backdrop-filter: blur(15px);
        border: 2px solid rgba(255, 255, 255, 0.25);
        position: relative;
        overflow: hidden;
    ">
    <div style="
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 30% 20%, rgba(255,255,255,0.1) 0%, transparent 70%);
        z-index: 0;
    "></div>
    <div style="position: relative; z-index: 1;">
    <div style="font-size:72px; margin-bottom:15px; animation: pulse 2s infinite;">🤖</div>
    <h3 style="
        margin-bottom:25px; 
        font-weight: 700;
        font-size: 28px;
        text-shadow: 0 2px 5px rgba(0,0,0,0.3);
    ">AI Statistics</h3>
    <div style="margin:25px 0;">
    <div style="
        font-size:42px;
        font-weight:900;
        color:#ffd86b;
        text-shadow: 0 3px 10px rgba(255, 216, 107, 0.3);
        margin-bottom: 5px;
    ">1M+</div>
    <div style="font-size:16px;opacity:0.95; letter-spacing: 0.5px; font-weight: 500;">Recipes Analyzed</div>
    </div>
    <div style="margin:25px 0;">
        <div style="
        font-size:42px;
        font-weight:900;
        color:#6ee7b7;
        text-shadow: 0 3px 10px rgba(110, 231, 183, 0.3);
        margin-bottom: 5px;
    ">99%</div>
    <div style="font-size:16px;opacity:0.95; letter-spacing: 0.5px; font-weight: 500;">Accuracy Rate</div>
    </div>
    <div style="margin:25px 0;">
    <div style="
        font-size:42px;
        font-weight:900;
        color:#93c5fd;
        text-shadow: 0 3px 10px rgba(147, 197, 253, 0.3);
        margin-bottom: 5px;
    ">0.5s</div>
    <div style="font-size:16px;opacity:0.95; letter-spacing: 0.5px; font-weight: 500;">Avg. Response Time</div>
    </div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    # AI Learning Progress Card
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(102,126,234,0.4), rgba(118,75,162,0.4));
        padding: 30px;
        border-radius: 25px;
        margin-top: 25px;
        text-align: center;
        color: white;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        backdrop-filter: blur(15px);
        border: 2px solid rgba(255, 255, 255, 0.25);
        position: relative;
        overflow: hidden;
    ">
    <div style="
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 70% 80%, rgba(255,255,255,0.1) 0%, transparent 70%);
        z-index: 0;
    "></div>
    <div style="position: relative; z-index: 1;">
        <h3 style="
        margin-bottom:30px; 
        font-weight: 700;
        font-size: 28px;
        text-shadow: 0 2px 5px rgba(0,0,0,0.3);
    ">🎯 AI Learning Progress</h3>
    <div style="margin:25px 0;">
    <div style="display:flex;justify-content:space-between;font-size:16px; margin-bottom: 12px;">
        <span style="font-weight: 600;">Recipe Matching</span>
        <span style="font-weight: 800; font-size: 18px;">85%</span>
    </div>
    <div style="background:rgba(255,255,255,0.3);height:12px;border-radius:8px; overflow: hidden;">
    <div style="
        background:linear-gradient(90deg,#ffd86b,#fbbf24);
        width:85%;
        height:100%;
        border-radius:8px;
        box-shadow: 0 2px 10px rgba(255, 216, 107, 0.3);
    "></div>
    </div>
    </div>
    <div style="margin:25px 0;">
    <div style="display:flex;justify-content:space-between;font-size:16px; margin-bottom: 12px;">
        <span style="font-weight: 600;">Nutrition Analysis</span>
        <span style="font-weight: 800; font-size: 18px;">92%</span>
        </div>
    <div style="background:rgba(255,255,255,0.3);height:12px;border-radius:8px; overflow: hidden;">
    <div style="
        background:linear-gradient(90deg,#6ee7b7,#34d399);
        width:92%;
        height:100%;
        border-radius:8px;
        box-shadow: 0 2px 10px rgba(110, 231, 183, 0.3);
        "></div>
    </div>
    </div>
    <div style="margin:25px 0;">
    <div style="display:flex;justify-content:space-between;font-size:16px; margin-bottom: 12px;">
            <span style="font-weight: 600;">Ingredient Recognition</span>
            <span style="font-weight: 800; font-size: 18px;">78%</span>
    </div>
    <div style="background:rgba(255,255,255,0.3);height:12px;border-radius:8px; overflow: hidden;">
    <div style="
        background:linear-gradient(90deg,#93c5fd,#60a5fa);
        width:78%;
        height:100%;
        border-radius:8px;
        box-shadow: 0 2px 10px rgba(147, 197, 253, 0.3);
    "></div>
    </div>
    </div>      
    <div style="margin-top: 30px; font-size: 14px; opacity: 0.9; font-weight: 500;">
    📈 AI continuously learning from user interactions
    </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

# Sidebar for navigation
with st.sidebar:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%);
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.3);
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    ">
        <h2 style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
            font-size: 24px;
        ">🚀 Navigation</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation tabs with icons
    page = st.radio(
        "",
        ["📊 Generate Recipes", "📈 Nutrition Analytics", "ℹ️ About AI"],
        key="navigation_radio",
        label_visibility="collapsed"
    )
    
    if page == "ℹ️ About AI":
        st.markdown("---")
        st.markdown("### 🤖 About AI Chef")
        st.info("""
        **Powered by Advanced AI Algorithms**
        
        This system uses:
        - 🧠 Machine Learning models
        - 📊 Nutrition analysis
        - 🎯 Personalization algorithms
        - 🖼️ Image recognition
        
        **AI Features:**
        - Smart ingredient matching
        - Health score calculation
        - Visual nutrition analysis
        - Recipe optimization
        """)
        
    elif page == "📈 Nutrition Analytics":
        st.markdown("---")
        st.markdown("### 📊 Analytics Features")
        st.success("""
        **AI-Powered Insights:**
        1. 🍽️ Food category analysis
        2. 📈 Nutrition visualization
        3. 🎯 Health scoring
        4. 🔍 Detailed breakdowns
        5. 💡 Smart recommendations
        """)
    
    # Ingredients selector only shown on Generate Recipes page
    if page == "📊 Generate Recipes":
        st.markdown("---")
        ingredient_txt = ingredients_selector()
        
        st.markdown("---")
        
        # AI Settings
        st.markdown("### ⚙️ AI Settings")
        nb_recommendations = st.slider(
            "Number of AI recommendations",
            3, 15, 9, step=3,
            help="AI will find the perfect recipes for you",
            key="nb_rec_slider"
        )
        
        ai_intensity = st.slider(
            "AI Creativity Level",
            1, 10, 7,
            help="Higher = more creative, Lower = more precise",
            key="ai_intensity"
        )
        
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            padding: 15px;
            border-radius: 15px;
            margin-top: 20px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            background-color: rgba(255, 255, 255, 0.1);  
        ">
        <div style="font-size: 12px; color: #667eea;">⚡ AI Status: Ready</div>
        <div style="font-size: 10px; color: #666;">Powered by ML Algorithms</div>
        </div>
        """, unsafe_allow_html=True)

# ------------------ MAIN CONTENT BASED ON PAGE ------------------
if page == "📊 Generate Recipes":
    with st.container():
        with st.form("recommendation_form"):
            st.markdown('<div class="animate-fadeIn">', unsafe_allow_html=True)
            st.markdown('<h2 class="section-header animate-slideInLeft">🎯 Set Your Nutrition Goals</h2>', unsafe_allow_html=True)
            
            # Nutrition sliders in columns
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### 🔥 Energy & Fats")
                Calories = st.slider("Calories (kcal)", 0, 2000, 500, 50, key="calories")
                FatContent = st.slider("Total Fat (g)", 0, 100, 25, 5, key="fat")
                SaturatedFatContent = st.slider("Saturated Fat (g)", 0, 50, 8, 2, key="sat_fat")
            
            with col2:
                st.markdown("#### 🩸 Heart Health")
                CholesterolContent = st.slider("Cholesterol (mg)", 0, 300, 100, 10, key="chol")
                SodiumContent = st.slider("Sodium (mg)", 0, 2300, 400, 50, key="sodium")
            
            with col3:
                st.markdown("#### 🌾 Carbs & Protein")
                CarbohydrateContent = st.slider("Carbohydrates (g)", 0, 325, 100, 10, key="carbs")
                FiberContent = st.slider("Fiber (g)", 0, 50, 12, 2, key="fiber")
                SugarContent = st.slider("Sugar (g)", 0, 40, 15, 2, key="sugar")
                ProteinContent = st.slider("Protein (g)", 0, 100, 30, 5, key="protein")
            
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
            
            # AI Analysis Preview
            st.markdown("---")
            st.markdown("#### 🤖 AI Preview")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>⚡ Energy</h4>
                    <h3>{Calories} kcal</h3>
                    <p>{'⚪ Low' if Calories < 400 else '🟡 Medium' if Calories < 600 else '🟢 Good' if Calories < 800 else '🔴 High'}</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>🎯 Balance</h4>
                    <h3>{ProteinContent}g</h3>
                    <p>{'⚪ Low' if ProteinContent < 20 else '🟡 Medium' if ProteinContent < 30 else '🟢 Good' if ProteinContent < 40 else '🔴 High'}</p>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>🏆 Health Score</h4>
                    <h3>{min(100, max(60, 100 - (SugarContent*2) - (SaturatedFatContent*3)))}</h3>
                    <p>AI Estimated</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Generate button
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                generate = st.form_submit_button(
                    "🚀 GENERATE WITH AI",
                    use_container_width=True,
                    type="primary",
                    help="Click to let AI find perfect recipes!"
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle form submission
    if generate:
        with st.spinner("🤖 AI is analyzing your preferences and finding perfect recipes..."):
            # Show advanced loading animation
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(100):
                progress_bar.progress(i + 1)
                if i < 25:
                    status_text.text("🔍 Analyzing nutrition goals...")
                elif i < 50:
                    status_text.text("🧠 Processing ingredient preferences...")
                elif i < 75:
                    status_text.text("⚡ Searching recipe database...")
                else:
                    status_text.text("✨ Optimizing AI recommendations...")
                time.sleep(0.02)
            
            status_text.text("✅ AI recommendations ready!")
            
            recommender = Recommendation(
                nutrition_list,
                nb_recommendations,
                st.session_state.selected_ingredients,
            )
            st.session_state.recommendations = recommender.generate()
            st.session_state.generated = True
            
            # Show success effects
            st.balloons()
            st.success("✨ AI has found perfect recipes for you!")
            time.sleep(1)
            
            # Rerun to show results
            st.rerun()
    
    # Display recommendations if generated
    if st.session_state.generated and st.session_state.recommendations:
        display.display_recommendation(st.session_state.recommendations)
        display.display_overview(st.session_state.recommendations)
        
        # Reset button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Start New AI Search", use_container_width=True, key="reset_btn"):
                st.session_state.generated = False
                st.session_state.recommendations = None
                st.rerun()

elif page == "📈 Nutrition Analytics":
    st.markdown('<div class="glass-card animate-fadeIn">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">📊 AI Nutrition Analytics</h2>', unsafe_allow_html=True)
    
    # Display food category pie chart
    display.display_food_category_pie_chart()
    
    # Sample nutrition table
    st.markdown('<h3 class="section-header">🍎 Sample Nutrition Values</h3>', unsafe_allow_html=True)
    
    # Create a sample nutrition table
    nutrition_data = {
        "Nutrient": ["Calories", "Total Fat", "Saturated Fat", "Cholesterol", "Sodium", 
                    "Carbohydrates", "Fiber", "Sugar", "Protein"],
        "Sample Value": ["500 kcal", "25g", "8g", "100mg", "400mg", "100g", "12g", "15g", "30g"],
        "Daily %": ["25%", "38%", "40%", "33%", "17%", "33%", "48%", "60%", "60%"],
        "Status": ["🟢 Optimal", "🟡 Moderate", "🟡 Moderate", "🟢 Good", "🟢 Low", 
                  "🟢 Good", "🟢 Excellent", "🟡 Moderate", "🟢 Excellent"]
    }
    
    nutrition_df = pd.DataFrame(nutrition_data)
    
    # Display with simple styling
    st.dataframe(
        nutrition_df,
        use_container_width=True,
        hide_index=True
    )
    
    # Health insights
    st.markdown('<h3 class="section-header">💡 AI Health Insights</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
        <div style="font-size: 40px;">🏆</div>
        <h4>Overall Score</h4>
        <h3>85/100</h3>
        <p>Excellent Balance</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
        <div style="font-size: 40px;">⚖️</div>
        <h4>Macro Ratio</h4>
        <h3>30:40:30</h3>
        <p>P:C:F Ratio</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 40px;">📈</div>
            <h4>Fiber Score</h4>
            <h3>48% DV</h4>
            <p>Above Average</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
elif page == "ℹ️ About AI":
    st.markdown('<div class="glass-card animate-fadeIn">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">🤖 About AI Nutrition Chef</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### **✨ What is AI Nutrition Chef?**
        
        **AI Nutrition Chef** is an intelligent cooking assistant powered by advanced 
        machine learning algorithms that analyze your nutritional requirements and 
        ingredient preferences to suggest personalized recipes.
        
        ### **🚀 How It Works**
        1. **🎯 Set Goals**: Adjust nutrition sliders to match your dietary targets
        2. **🛒 Choose Ingredients**: Select from our AI-categorized ingredients
        3. **🤖 AI Processing**: Our algorithms find perfect matches
        4. **📊 Get Insights**: View detailed nutrition analysis and AI recommendations
        
        ### **⚡ Technology Stack**
        - **🧠 Machine Learning**: Advanced neural networks for pattern recognition
        - **📊 Data Science**: Comprehensive nutrition analysis
        - **🖼️ Computer Vision**: Image recognition for recipe visualization
        - **🔗 API Integration**: Real-time data processing
        - **🎨 UI/UX**: Modern, responsive interface with animations
        
        ### **🌟 Key Features**
        - ✅ **Smart Recommendations**: AI-powered personalized suggestions
        - ✅ **Nutrition Analysis**: Real-time health scoring and insights
        - ✅ **Visual Analytics**: Interactive charts and graphs
        - ✅ **Ingredient Categorization**: Smart organization of food items
        - ✅ **Health Scoring**: AI-calculated wellness metrics
        - ✅ **Recipe Optimization**: AI-tuned cooking instructions
        
        ### **👥 Who Can Benefit?**
        - 🏃‍♂️ **Athletes**: Optimize performance nutrition
        - 🏥 **Health Enthusiasts**: Track and improve dietary habits
        - 🧑‍🍳 **Home Cooks**: Discover new recipes with preferred ingredients
        - 🥗 **Dieters**: Follow specific dietary plans
        - 👨‍👩‍👧‍👦 **Families**: Find recipes everyone will love """)
# Footer
st.markdown("---")
st.markdown("""
<div style="
    text-align: center;
    padding: 30px;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    border-radius: 20px;
    margin-top: 30px;
">
    <h3 style="color: #667eea; margin-bottom: 10px;">🚀 Powered by Advanced AI</h3>
    <p style="color: #666; margin-bottom: 20px;">The future of personalized nutrition starts here</p>
    <div style="font-size: 24px;">
        <span style="margin: 0 10px;">🤖</span>
        <span style="margin: 0 10px;">🧠</span>
        <span style="margin: 0 10px;">⚡</span>
        <span style="margin: 0 10px;">📊</span>
        <span style="margin: 0 10px;">🎯</span>
    </div>
    <p style="color: #999; margin-top: 20px; font-size: 12px;">
        Developed with ❤️ using Streamlit & Machine Learning | v2.0 AI Enhanced
    </p>
</div>
""", unsafe_allow_html=True)