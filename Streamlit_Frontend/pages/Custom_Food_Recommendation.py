import streamlit as st
import pandas as pd
import numpy as np
import time
import requests
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
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .animate-fadeIn { animation: fadeIn 1s ease; }
    .animate-fadeInUp { animation: fadeInUp 0.8s ease; }
    .animate-fadeInDown { animation: fadeInDown 0.8s ease; }
    .animate-slideInLeft { animation: slideInLeft 0.8s ease; }
    .animate-slideInRight { animation: slideInRight 0.8s ease; }
    .animate-glow { animation: glow 2s infinite; }
    .animate-rotate { animation: rotate 5s linear infinite; }
    .animate-bounce { animation: bounce 2s infinite; }
    .animate-pulse { animation: pulse 2s infinite; }
    
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
    
    .hover-3d {
        transform-style: preserve-3d;
        transition: transform 0.5s ease;
    }
    
    .hover-3d:hover {
        transform: rotateY(10deg) rotateX(5deg);
    }
    
    .gradient-border {
        position: relative;
        background: linear-gradient(white, white) padding-box,
                    linear-gradient(45deg, #667eea, #764ba2, #f093fb) border-box;
        border: 3px solid transparent;
    }
    
    .sparkle {
        position: relative;
        overflow: hidden;
    }
    
    .sparkle::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, transparent 70%);
        animation: rotate 4s linear infinite;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .sparkle:hover::after {
        opacity: 0.3;
    }
    
    .neon-text {
        color: #fff;
        text-shadow: 
            0 0 5px #fff,
            0 0 10px #fff,
            0 0 20px #667eea,
            0 0 30px #667eea,
            0 0 40px #667eea;
        animation: neon-pulse 1.5s infinite alternate;
    }
    
    @keyframes neon-pulse {
        from {
            text-shadow: 
                0 0 5px #fff,
                0 0 10px #fff,
                0 0 20px #667eea,
                0 0 30px #667eea,
                0 0 40px #667eea;
        }
        to {
            text-shadow: 
                0 0 10px #fff,
                0 0 20px #fff,
                0 0 30px #764ba2,
                0 0 40px #764ba2,
                0 0 50px #764ba2;
        }
    }
    
    .card-glow {
        box-shadow: 
            0 0 20px rgba(102, 126, 234, 0.3),
            0 0 40px rgba(118, 75, 162, 0.2),
            0 0 60px rgba(240, 147, 251, 0.1);
        transition: box-shadow 0.3s ease;
    }
    
    .card-glow:hover {
        box-shadow: 
            0 0 30px rgba(102, 126, 234, 0.5),
            0 0 60px rgba(118, 75, 162, 0.3),
            0 0 90px rgba(240, 147, 251, 0.2);
    }
    
    .custom-tip {
        background: linear-gradient(135deg, rgba(173, 216, 230, 0.9) 0%, rgba(224, 255, 255, 0.9) 100%);
        color: #2c3e50;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 10px 25px rgba(173, 216, 230, 0.3);
        backdrop-filter: blur(10px);
        animation: fadeInUp 0.8s ease;
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
    
    for (let i = 0; i < 30; i++) {
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

# Food categories for enhanced UI
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

# Fallback images for food categories with more variety
FOOD_CATEGORY_IMAGES = {
    "chicken": "https://images.unsplash.com/photo-1604503468505-ee68d8e8c8b8?w=400&h=300&fit=crop&auto=format",
    "beef": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=400&h=300&fit=crop&auto=format",
    "fish": "https://images.unsplash.com/photo-1599156612521-8d96973c5c2c?w=400&h=300&fit=crop&auto=format",
    "shrimp": "https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=400&h=300&fit=crop&auto=format",
    "egg": "https://images.unsplash.com/photo-1587486913049-53fc88980f79?w=400&h=300&fit=crop&auto=format",
    "rice": "https://images.unsplash.com/photo-1516684732162-798a0062be99?w=400&h=300&fit=crop&auto=format",
    "pasta": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=400&h=300&fit=crop&auto=format",
    "potato": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400&h=300&fit=crop&auto=format",
    "bread": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&h=300&fit=crop&auto=format",
    "flour": "https://images.unsplash.com/photo-1627222297885-69174b5dc725?w=400&h=300&fit=crop&auto=format",
    "tomato": "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=400&h=300&fit=crop&auto=format",
    "onion": "https://images.unsplash.com/photo-1508015926936-4eddcc6d4866?w=400&h=300&fit=crop&auto=format",
    "garlic": "https://images.unsplash.com/photo-1601524909163-21c68088d458?w=400&h=300&fit=crop&auto=format",
    "spinach": "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=400&h=300&fit=crop&auto=format",
    "broccoli": "https://images.unsplash.com/photo-1459411552884-841db9b3cc2a?w=400&h=300&fit=crop&auto=format",
    "carrot": "https://images.unsplash.com/photo-1598170845058-78131a90f4bf?w=400&h=300&fit=crop&auto=format",
    "bell pepper": "https://images.unsplash.com/photo-1563565375-f3fdfdbefa49?w=400&h=300&fit=crop&auto=format",
    "mushroom": "https://images.unsplash.com/photo-1568111467145-9f0d1486a7eb?w=400&h=300&fit=crop&auto=format",
    "cheese": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400&h=300&fit=crop&auto=format",
    "milk": "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=400&h=300&fit=crop&auto=format",
    "butter": "https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=400&h=300&fit=crop&auto=format",
    "oil": "https://images.unsplash.com/photo-1533050487297-09b450131914?w=400&h=300&fit=crop&auto=format",
    "salt": "https://images.unsplash.com/photo-1599936632836-89e59b2e5b1c?w=400&h=300&fit=crop&auto=format",
    "pepper": "https://images.unsplash.com/photo-1601286621078-71e72a4d6e6a?w=400&h=300&fit=crop&auto=format",
    "sugar": "https://images.unsplash.com/photo-1621947081315-dce56d366a91?w=400&h=300&fit=crop&auto=format",
    "lemon": "https://images.unsplash.com/photo-1587496679742-bad502958fbf?w=400&h=300&fit=crop&auto=format",
    "lime": "https://images.unsplash.com/photo-1590856029823-f4d2f6f60735?w=400&h=300&fit=crop&auto=format",
    "honey": "https://images.unsplash.com/photo-1587049352851-8d4e89133924?w=400&h=300&fit=crop&auto=format",
    "soy sauce": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=300&fit=crop&auto=format",
    "vinegar": "https://images.unsplash.com/photo-1608039755401-742074f0548d?w=400&h=300&fit=crop&auto=format",
    "tofu": "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=400&h=300&fit=crop&auto=format",
    "avocado": "https://images.unsplash.com/photo-1523049673857-eb18f1d7b578?w=400&h=300&fit=crop&auto=format",
    "quinoa": "https://images.unsplash.com/photo-1598974357801-cbca100e5d10?w=400&h=300&fit=crop&auto=format",
    "oats": "https://images.unsplash.com/photo-1623659940008-77950d1b6757?w=400&h=300&fit=crop&auto=format",
    "yogurt": "https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=400&h=300&fit=crop&auto=format"
}

# ------------------ SESSION STATE ------------------
if "generated" not in st.session_state:
    st.session_state.generated = False
    st.session_state.recommendations = None
if "selected_ingredients" not in st.session_state:
    st.session_state.selected_ingredients = []
if "food_images_cache" not in st.session_state:
    st.session_state.food_images_cache = {}
if "animation_played" not in st.session_state:
    st.session_state.animation_played = False

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

        try:
            generator = Generator(self.nutrition_list, self.ingredients_list, params)
            recipes = generator.generate()
            
            # Check if recipes is a list/dict or if it needs JSON parsing
            if recipes is None:
                st.error("No recipes generated. Please check your input parameters.")
                return None
                
            # If recipes is a response object with json() method
            if hasattr(recipes, 'json'):
                recipes = recipes.json()
            
            # If recipes is a dict with 'output' key
            if isinstance(recipes, dict):
                recipes = recipes.get("output", [])
            
            # Ensure we have a list
            if not isinstance(recipes, list):
                st.error(f"Unexpected response format: {type(recipes)}")
                return None

            # Add images with loading animation and fallback
            for recipe in recipes:
                recipe_name = recipe.get("Name", "")
                try:
                    # Try to get image from ImageFinder
                    image_link = find_image(recipe_name)
                    if not image_link or image_link == "":
                        # Try to get fallback image based on ingredients
                        for ingredient in FOOD_CATEGORY_IMAGES:
                            if ingredient.lower() in recipe_name.lower():
                                image_link = FOOD_CATEGORY_IMAGES[ingredient]
                                break
                        else:
                            # Default fallback image
                            image_link = "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop&auto=format"
                    
                    recipe["image_link"] = image_link
                except Exception as e:
                    st.warning(f"Could not load image for {recipe_name}: {str(e)}")
                    recipe["image_link"] = "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop&auto=format"
                
                # Simulate some processing delay for animation
                time.sleep(0.01)

            return recipes
            
        except Exception as e:
            st.error(f"Error generating recommendations: {str(e)}")
            return None

# ------------------ ENHANCED DISPLAY LOGIC ------------------
class Display:
    def display_recommendation(self, recommendations):
        st.markdown('<div class="animate-fadeIn">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header animate-slideInLeft neon-text">✨ AI-Generated Recipes</h2>', unsafe_allow_html=True)
        
        if not recommendations:
            st.markdown('<div class="animate-fadeInUp">', unsafe_allow_html=True)
            st.error("🚫 No recipes found! Try adjusting your criteria or selecting different ingredients.")
            st.markdown('</div>', unsafe_allow_html=True)
            return

        # Animated success message
        st.markdown(f"""
        <div class="success-toast animate-glow card-glow">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="font-size: 40px;" class="animate-bounce">✨</div>
                <div>
                    <h3 style="margin: 0; font-size: 24px;" class="neon-text">🎉 {len(recommendations)} Perfect Recipes Found!</h3>
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
            st.markdown(f'<div class="recipe-card animate-fadeIn hover-3d card-glow sparkle" style="animation-delay: {index*0.2}s">', unsafe_allow_html=True)
            
            # Recipe header with AI badge
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### 🤖 {name}")
                st.markdown('<div style="font-size: 12px; color: #667eea; margin-top: -10px; animation: pulse 2s infinite;">✨ AI-Powered Selection</div>', unsafe_allow_html=True)
            with col2:
                calories = recipe.get("Calories", 0)
                st.markdown(f'<div class="ai-pulse"><span class="nutrition-badge gradient-border">🔥 {calories} cal</span></div>', unsafe_allow_html=True)
            
            # Image with hover effect
            img = recipe.get("image_link")
            if img:
                st.image(img, use_container_width=True, caption=name)
            else:
                # Fallback image
                st.image("https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop&auto=format", 
                        use_container_width=True, 
                        caption="Delicious Food")
            
            # Quick stats
            self._display_quick_stats(recipe)
            
            # Expand for details
            with st.expander("🔍 View AI Analysis & Full Recipe", expanded=False):
                self._display_recipe_details(recipe)
            
            st.markdown('</div>', unsafe_allow_html=True)

    def _display_quick_stats(self, recipe):
        prep_time = recipe.get('PrepTime', 0)
        cook_time = recipe.get('CookTime', 0)
        total_time = recipe.get('TotalTime', 0) or prep_time + cook_time
        protein = recipe.get('ProteinContent', 0)
        carbs = recipe.get('CarbohydrateContent', 0)
        fat = recipe.get('FatContent', 0)
        
        # Time stats
        st.markdown('<div class="quick-stats">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'''
            <div class="time-metric hover-3d">
                <div style="font-size: 28px;" class="animate-bounce">⏱️</div>
                <div class="stat-value">{prep_time}</div>
                <div class="stat-label">Prep (min)</div>
            </div>
            ''', unsafe_allow_html=True)
        with col2:
            st.markdown(f'''
            <div class="time-metric hover-3d">
                <div style="font-size: 28px;" class="animate-bounce">🔥</div>
                <div class="stat-value">{cook_time}</div>
                <div class="stat-label">Cook (min)</div>
            </div>
            ''', unsafe_allow_html=True)
        with col3:
            st.markdown(f'''
            <div class="time-metric hover-3d">
                <div style="font-size: 28px;" class="animate-bounce">⏰</div>
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
            <div class="nutrition-metric hover-3d">
                <div style="font-size: 28px;" class="animate-bounce">🥩</div>
                <div class="stat-value">{protein}g</div>
                <div class="stat-label">Protein</div>
            </div>
            ''', unsafe_allow_html=True)
        with col2:
            st.markdown(f'''
            <div class="nutrition-metric hover-3d">
                <div style="font-size: 28px;" class="animate-bounce">🌾</div>
                <div class="stat-value">{carbs}g</div>
                <div class="stat-label">Carbs</div>
            </div>
            ''', unsafe_allow_html=True)
        with col3:
            st.markdown(f'''
            <div class="nutrition-metric hover-3d">
                <div style="font-size: 28px;" class="animate-bounce">🥑</div>
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
            transform: scale(1.01);
            transition: transform 0.2s ease;
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
        if isinstance(ingredients, str):
            ingredients = [ing.strip() for ing in ingredients.split(';') if ing.strip()]
        
        if ingredients:
            cols = st.columns(4)
            for i, ing in enumerate(ingredients[:20]):
                with cols[i % 4]:
                    st.markdown(f'<div class="ingredient-pill hover-3d">{ing}</div>', unsafe_allow_html=True)
        
        # Instructions
        st.markdown("#### 👨‍🍳 AI-Optimized Instructions")
        instructions = recipe.get("RecipeInstructions", [])
        if isinstance(instructions, str):
            instructions = [step.strip() for step in instructions.split('.') if step.strip()]
        
        if instructions:
            for i, step in enumerate(instructions, 1):
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                    padding: 15px;
                    border-radius: 10px;
                    margin: 10px 0;
                    border-left: 4px solid #667eea;
                    transition: all 0.3s ease;
                    cursor: pointer;
                " onmouseover="this.style.transform='translateX(10px)';" onmouseout="this.style.transform='translateX(0)';">
                    <strong>Step {i}:</strong> {step}
                </div>
                """, unsafe_allow_html=True)

    def display_overview(self, recommendations):
        if not recommendations:
            return
        
        st.markdown('<div class="animate-fadeIn">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header animate-slideInLeft neon-text">🤖 AI Nutrition Dashboard</h2>', unsafe_allow_html=True)
        
        recipe_names = [r.get("Name", "Unknown") for r in recommendations]
        
        selected_name = st.selectbox(
            "📋 Select a recipe for AI analysis",
            recipe_names,
            key="overview_recipe_selectbox"
        )
        
        selected_recipe = next(
            (r for r in recommendations if r.get("Name") == selected_name),
            recommendations[0]
        )
        
        # Nutrition metrics grid
        self._display_nutrition_metrics(selected_recipe)
        
        # Advanced charts
        self._display_advanced_charts(selected_recipe, selected_name)
        
        st.markdown('</div>', unsafe_allow_html=True)

    def _display_nutrition_metrics(self, recipe):
        st.markdown('<div class="glass-card animate-fadeInUp card-glow">', unsafe_allow_html=True)
        st.markdown("#### ⚡ AI Health Score & Metrics")
        
        # Calculate health score based on recipe data
        calories = recipe.get('Calories', 0)
        protein = recipe.get('ProteinContent', 0)
        carbs = recipe.get('CarbohydrateContent', 0)
        fat = recipe.get('FatContent', 0)
        fiber = recipe.get('FiberContent', 0)
        sugar = recipe.get('SugarContent', 0)
        sat_fat = recipe.get('SaturatedFatContent', 0)
        
        health_score = 100
        if calories > 800: health_score -= 20
        elif calories > 500: health_score -= 10
        
        if protein < 20: health_score -= 10
        elif protein > 30: health_score += 10
        
        if carbs > 100: health_score -= 10
        elif carbs < 30: health_score -= 5
        
        if fat > 30: health_score -= 10
        elif fat < 10: health_score -= 5
        
        if fiber < 5: health_score -= 10
        elif fiber > 10: health_score += 10
        
        if sugar > 20: health_score -= 15
        elif sugar > 10: health_score -= 5
        
        if sat_fat > 10: health_score -= 10
        
        health_score = max(0, min(100, health_score))
        
        # Determine color based on score
        if health_score >= 80:
            score_color = "#06D6A0"
            score_text = "Excellent"
        elif health_score >= 60:
            score_color = "#FFD166"
            score_text = "Good"
        else:
            score_color = "#EF476F"
            score_text = "Needs Improvement"
        
        # Animated health score circle
        st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            <div style="
                width: 150px;
                height: 150px;
                margin: 0 auto;
                background: conic-gradient({score_color} {health_score}%, #e0e0e0 0%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                position: relative;
                box-shadow: 0 10px 30px rgba(78, 205, 196, 0.3);
                animation: pulse 2s infinite;
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
                    <span style="font-size: 32px; font-weight: bold; color: {score_color};">{health_score}</span>
                    <span style="font-size: 14px; color: #666;">{score_text}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Main metrics with hover effects
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
                <div class="metric-card hover-3d" style="border-top: 4px solid {color};">
                    <h4 style="color: {color}; font-size: 14px; animation: pulse 3s infinite;">{label}</h4>
                    <h3 style="margin: 10px 0; font-size: 24px; animation: bounce 2s infinite;">{value}</h3>
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
                <div class="metric-card hover-3d" style="border-top: 4px solid {color};">
                    <h4 style="color: {color}; font-size: 14px;">{label}</h4>
                    <h3 style="margin: 10px 0; font-size: 24px;">{value}</h3>
                    <p style="color: #666; font-size: 12px; margin: 0;">{unit}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    def _display_advanced_charts(self, recipe, name):
        col1, col2 = st.columns(2)
        
        with col1:
            # Enhanced Pie Chart with 3D effect
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
                    "labelLine": {"show": True},
                    "animationType": "scale",
                    "animationEasing": "elasticOut"
                }]
            }
            st_echarts(options=options_pie, height="400px")
        
        with col2:
            # Enhanced Bar Chart with gradient
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
                                {"offset": 0.5, "color": "#764ba2"},
                                {"offset": 1, "color": "#f093fb"}
                            ]
                        },
                        "borderRadius": [5, 5, 0, 0],
                        "shadowBlur": 10,
                        "shadowColor": "rgba(102, 126, 234, 0.5)"
                    },
                    "barWidth": "60%"
                }]
            }
            st_echarts(options=options_bar, height="400px")

# ------------------ ENHANCED INGREDIENTS SELECTOR ------------------
def ingredients_selector():
    """Enhanced ingredients selector with categories and animations"""
    st.markdown('<div class="glass-card animate-fadeIn card-glow">', unsafe_allow_html=True)
    st.markdown('<h3 class="glowing-text">🎯 AI Ingredient Selector</h3>', unsafe_allow_html=True)
    
    # Display food categories with animations
    st.markdown("#### 🗂️ Food Categories")
    for category, ingredients in FOOD_CATEGORIES.items():
        with st.expander(f"{category} ({len(ingredients)} items)", expanded=False):
            cols = st.columns(4)
            for idx, ingredient in enumerate(ingredients):
                with cols[idx % 4]:
                    is_selected = ingredient in st.session_state.selected_ingredients
                    button_text = f"✅ {ingredient}" if is_selected else f"➕ {ingredient}"
                    if st.button(button_text, key=f"cat_{ingredient}", 
                                help=f"{'Remove' if is_selected else 'Add'} {ingredient}",
                                use_container_width=True):
                        if is_selected:
                            st.session_state.selected_ingredients.remove(ingredient)
                        else:
                            st.session_state.selected_ingredients.append(ingredient)
                        st.rerun()
    
    # Custom ingredient input with floating animation
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
        if st.button("🚀 Add", key="add_custom", help="Add custom ingredient", use_container_width=True):
            if custom_ing and custom_ing.strip().lower() not in st.session_state.selected_ingredients:
                st.session_state.selected_ingredients.append(custom_ing.strip().lower())
                st.success(f"Added: {custom_ing}")
                st.rerun()
    
    # Selected ingredients display with 3D effects
    if st.session_state.selected_ingredients:
        st.markdown("#### 📋 Your Selection")
        st.markdown(f'<div style="background: rgba(102, 126, 234, 0.1); padding: 20px; border-radius: 15px; margin: 10px 0;" class="gradient-border">', unsafe_allow_html=True)
        
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
                    # Show ingredient with image if available
                    ing_image = FOOD_CATEGORY_IMAGES.get(ing, "")
                    if ing_image:
                        st.image(ing_image, width=60, caption=ing)
                    else:
                        st.markdown(f'<div class="ingredient-pill selected hover-3d">{ing}</div>', unsafe_allow_html=True)
        
        if uncategorized:
            st.markdown("**✨ Custom Ingredients:**")
            cols = st.columns(6)
            for idx, ing in enumerate(uncategorized):
                with cols[idx % 6]:
                    st.markdown(f'<div class="ingredient-pill selected hover-3d">{ing}</div>', unsafe_allow_html=True)
        
        # Clear button with animation
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🗑️ Clear All", key="clear_all", use_container_width=True):
                st.session_state.selected_ingredients = []
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Selection statistics with animated counter
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
        border: 2px solid transparent;
        background: linear-gradient(white, white) padding-box,
                    linear-gradient(45deg, #667eea, #764ba2, #f093fb) border-box;
        animation: pulse 3s infinite;
    ">
    <div style="font-size: 14px; color: rgba(255,255,255,0.9);">📊 Selection Stats</div>
    <div style="font-size: 28px; font-weight: bold; color: white; animation: bounce 2s infinite;">{total_selected} ingredients</div>
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
    animation: floatTitle 3s ease-in-out infinite;
" class="neon-text">🤖 AI Nutrition Chef</h1>
""", unsafe_allow_html=True)

# Sidebar for ingredients selection
with st.sidebar:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%);
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.3);
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    ">
        <h2 style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
            font-size: 24px;
            font-weight: 700;
        ">⚙️ Configuration</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Ingredients selector in sidebar
    st.markdown("### 🛒 Ingredients Selection")
    ingredient_txt = ingredients_selector()
    
    st.markdown("---")
    
    # Recipe options in sidebar with slider effects
    st.markdown("### ⚙️ Recipe Options")
    nb_recommendations = st.slider(
        "Number of recommendations",
        5, 20, 10, step=1,
        help="Choose how many recipes you want to see",
        key="nb_rec_slider"
    )
    
    # Add AI creativity slider
    ai_creativity = st.slider(
        "AI Creativity Level",
        1, 10, 7,
        help="Higher = more creative recipes, Lower = more traditional",
        key="ai_creativity"
    )
    
    st.markdown("---")
    
    # Quick tips with animated icons - FIXED: Using markdown instead of info
    st.markdown("### 💡 Tips")
    st.markdown("""
    <div class="custom-tip">
        <div style="animation: pulse 3s infinite;">
        1. 🎯 Select 2-5 ingredients for best results<br>
        2. ⚡ Adjust sliders based on your diet goals<br>
        3. 🔄 Try different combinations<br>
        4. 📊 Check the nutrition charts<br>
        5. 🌟 Images are fetched automatically
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # AI Status indicator
    st.markdown("---")
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
        animation: pulse 2s infinite;
    ">
    <div style="font-size: 12px; color: #667eea;">🤖 AI Status: <span style="color: #06D6A0; font-weight: bold;">Ready</span></div>
    <div style="font-size: 10px; color: #666; margin-top: 5px;">Powered by Advanced ML</div>
    </div>
    """, unsafe_allow_html=True)

# Main content area with enhanced tabs
tab1, tab2 = st.tabs(["🎯 Nutrition Targets", "🌟 How It Works"])

with tab1:
    with st.form("recommendation_form"):
        st.markdown('<div class="animate-fadeIn">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header animate-slideInLeft neon-text">🎯 Set Your Nutritional Targets</h2>', unsafe_allow_html=True)
        
        # Nutrition sliders in columns with hover effects
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
        
        # Generate button with enhanced effects
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            generate = st.form_submit_button(
                "🚀 GENERATE RECOMMENDATIONS",
                use_container_width=True,
                type="primary"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="glass-card animate-fadeIn">', unsafe_allow_html=True)
    st.markdown("""
    ## 🌟 How It Works
    
    ### 🎯 **Set Nutritional Goals**
    - ⚡ Adjust sliders to match your dietary requirements
    - 🎯 Target specific macronutrient ratios
    - 🩸 Control sodium, cholesterol, and sugar intake
    
    ### 🛒 **Select Ingredients**
    - 🗂️ Choose from categorized ingredients
    - ✨ Add custom ingredients with ease
    - 🎨 Recipes include your selected ingredients
    
    ### 🔍 **Get AI Recommendations**
    - 🤖 Advanced AI analyzes thousands of recipes
    - 🎯 Matches your nutritional targets perfectly
    - 🔄 Filters by your preferred ingredients
    
    ### 📊 **Analyze Results**
    - 📈 View detailed nutrition breakdowns
    - 📊 Compare recipes side by side
    - 👨‍🍳 Get cooking instructions and ingredient lists
    - 🖼️ See beautiful food images for each recipe
    
    ### ✨ **Advanced Features**
    - 🌈 Animated UI with particle effects
    - 🎨 Glassmorphism design elements
    - ⚡ Real-time health scoring
    - 🔄 Interactive 3D charts
    - 🌟 Gradient borders and neon effects
    
    ---
    
    **💡 Tips for Best Results:**
    1. 🎯 Start with broad targets, then refine
    2. 🗂️ Select 2-5 ingredients for best matches
    3. 📊 Use the charts to visualize nutrition
    4. 💾 Save your favorite recipes for later
    5. 🌟 Check the images for recipe inspiration
    6. 🔄 Try different AI creativity levels
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ RUN ------------------
if generate:
    with st.spinner("🤖 AI is analyzing your preferences..."):
        # Show enhanced loading animation
        placeholder = st.empty()
        with placeholder.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown("""
                <div style="text-align: center; padding: 40px;">
                    <div style="font-size: 60px; margin-bottom: 20px; animation: rotate 2s linear infinite;">🌀</div>
                    <div class="shimmer" style="height: 100px; border-radius: 15px; margin: 20px 0;"></div>
                    <p style="text-align: center; color: #667eea; font-size: 18px; font-weight: 600;" class="neon-text">
                        🤖 AI is finding perfect recipes for you...
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        # Add progressive loading with stages
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        loading_stages = [
            "🔍 Analyzing your nutritional goals...",
            "🧠 Processing ingredient preferences...",
            "⚡ Searching through thousands of recipes...",
            "🎯 Finding perfect matches...",
            "🖼️ Fetching beautiful food images...",
            "✨ Finalizing AI recommendations..."
        ]
        
        for i, stage in enumerate(loading_stages):
            progress = int((i + 1) * (100 / len(loading_stages)))
            progress_bar.progress(progress)
            status_text.text(stage)
            time.sleep(0.3)
        
        try:
            recommender = Recommendation(
                nutrition_list,
                nb_recommendations,
                st.session_state.selected_ingredients,
            )
            st.session_state.recommendations = recommender.generate()
            st.session_state.generated = True
            
            # Clear loading animation
            placeholder.empty()
            progress_bar.empty()
            status_text.empty()
            
            # Show success effects
            st.balloons()
            st.markdown("""
            <div style="text-align: center;">
                <div style="font-size: 40px; animation: bounce 2s infinite;">✨</div>
                <h3 style="color: #06D6A0;">AI Recommendations Ready!</h3>
                <p>Perfect recipes found based on your preferences</p>
            </div>
            """, unsafe_allow_html=True)
            
            time.sleep(1.5)
            
            # Rerun to show results
            st.rerun()
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.session_state.generated = False

if st.session_state.generated and st.session_state.recommendations:
    display.display_recommendation(st.session_state.recommendations)
    display.display_overview(st.session_state.recommendations)
    
    # Reset button with animation
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Generate New Recommendations", 
                    use_container_width=True, 
                    key="reset_btn",
                    type="secondary"):
            st.session_state.generated = False
            st.session_state.recommendations = None
            st.rerun()
else:
    if st.session_state.generated:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <div style="font-size: 40px;">⚠️</div>
            <h3>No recommendations were generated</h3>
            <p>Please try adjusting your parameters or selecting different ingredients</p>
        </div>
        """, unsafe_allow_html=True)

# Enhanced Footer
st.markdown("---")
st.markdown("""
<div style="
    text-align: center;
    padding: 40px;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    border-radius: 25px;
    margin-top: 50px;
    border: 2px solid transparent;
    background: linear-gradient(white, white) padding-box,
                linear-gradient(45deg, #667eea, #764ba2, #f093fb) border-box;
    animation: glow 3s infinite;
">
    <h3 style="color: #667eea; margin-bottom: 15px; animation: pulse 3s infinite;" class="neon-text">🚀 Powered by Advanced AI</h3>
    <p style="color: #666; margin-bottom: 25px; font-size: 16px;">The future of personalized nutrition starts here</p>
    <div style="font-size: 32px; margin-bottom: 20px;">
        <span style="margin: 0 15px; animation: bounce 2s infinite;">🤖</span>
        <span style="margin: 0 15px; animation: bounce 2s infinite 0.2s;">🧠</span>
        <span style="margin: 0 15px; animation: bounce 2s infinite 0.4s;">⚡</span>
        <span style="margin: 0 15px; animation: bounce 2s infinite 0.6s;">📊</span>
        <span style="margin: 0 15px; animation: bounce 2s infinite 0.8s;">🎯</span>
    </div>
    <p style="color: #999; margin-top: 20px; font-size: 12px;">
        Developed with ❤️ using Streamlit & Machine Learning | v3.0 AI Enhanced
    </p>
</div>
""", unsafe_allow_html=True)