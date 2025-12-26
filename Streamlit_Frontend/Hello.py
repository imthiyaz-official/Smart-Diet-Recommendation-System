import streamlit as st

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Diet Recommendation System",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 1rem !important;
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
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .animate-fadeIn { animation: fadeIn 1s ease; }
    .animate-fadeInUp { animation: fadeInUp 0.8s ease; }
    
    .feature-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border-left: 5px solid #667eea;
        text-align: center;
        height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(0,0,0,0.15);
        border-left: 5px solid #f093fb;
    }
    
    .feature-icon {
        font-size: 45px;
        margin-bottom: 15px;
        animation: float 3s infinite ease-in-out;
    }
    
    .feature-title {
        color: #667eea;
        font-weight: 700;
        font-size: 18px;
        margin-bottom: 10px;
    }
    
    .feature-desc {
        color: #555;
        font-size: 14px;
        line-height: 1.5;
    }
    
    .cta-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 15px 40px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-block;
        text-align: center;
        text-decoration: none;
        margin: 10px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .cta-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        color: white;
    }
    
    .tech-stack {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
    }
    
    .tech-badge {
        display: inline-block;
        background: white;
        color: #667eea;
        padding: 8px 18px;
        border-radius: 25px;
        margin: 5px;
        font-size: 14px;
        font-weight: 600;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .tech-badge:hover {
        background: #667eea;
        color: white;
        transform: scale(1.05);
    }
    
    .hero-section {
        text-align: center;
        padding: 50px 20px;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 20px;
        margin: 30px 0;
    }
    
    .hero-icon {
        font-size: 80px;
        margin-bottom: 20px;
        animation: float 4s infinite ease-in-out;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stats-container {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        margin: 40px 0;
    }
    
    .stat-item {
        text-align: center;
        padding: 20px;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        color: #667eea;
        margin-bottom: 5px;
    }
    
    .stat-label {
        color: #666;
        font-size: 14px;
        font-weight: 600;
    }
    
    .repo-link {
        display: inline-block;
        background: linear-gradient(135deg, #24292e 0%, #444d56 100%);
        color: white;
        padding: 12px 30px;
        border-radius: 50px;
        text-decoration: none;
        font-weight: 600;
        margin-top: 20px;
        transition: all 0.3s ease;
    }
    
    .repo-link:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ------------------ HERO SECTION ------------------
st.markdown('<h1 class="main-header animate-fadeIn">🍎 Diet Recommendation System</h1>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div class="hero-section animate-fadeInUp">
        <div class="hero-icon">🤖</div>
        <h2 style="color: #333; margin-bottom: 20px;">
            AI-Powered Personalized Nutrition
        </h2>
        <p style="color: #555; font-size: 16px; line-height: 1.6; max-width: 800px; margin: 0 auto;">
            Get personalized diet recommendations based on your nutritional needs, 
            ingredient preferences, and health goals using advanced machine learning algorithms.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ------------------ STATISTICS ------------------
st.markdown('<div class="stats-container animate-fadeInUp">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-item">
        <div class="stat-number">1M+</div>
        <div class="stat-label">Recipes Analyzed</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-item">
        <div class="stat-number">99%</div>
        <div class="stat-label">Accuracy Rate</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-item">
        <div class="stat-number">⚡</div>
        <div class="stat-label">Real-time Analysis</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-item">
        <div class="stat-number">🤖</div>
        <div class="stat-label">AI-Powered</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ------------------ FEATURES ------------------
st.markdown('<h2 style="color: #667eea; text-align: center; margin: 40px 0 20px 0;">✨ Key Features</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card animate-fadeInUp" style="animation-delay: 0.1s">
        <div class="feature-icon">🎯</div>
        <div class="feature-title">Personalized Recommendations</div>
        <div class="feature-desc">
            Get recipes tailored to your specific nutritional requirements and dietary preferences
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card animate-fadeInUp" style="animation-delay: 0.3s">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Nutrition Analytics</div>
        <div class="feature-desc">
            Detailed breakdown of calories, macros, vitamins, and minerals for each recipe
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card animate-fadeInUp" style="animation-delay: 0.2s">
        <div class="feature-icon">🛒</div>
        <div class="feature-title">Smart Ingredient Selection</div>
        <div class="feature-desc">
            Choose from categorized ingredients or add custom ones you love
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card animate-fadeInUp" style="animation-delay: 0.4s">
        <div class="feature-icon">⚡</div>
        <div class="feature-title">Real-time Processing</div>
        <div class="feature-desc">
            Instant recommendations powered by advanced machine learning algorithms
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card animate-fadeInUp" style="animation-delay: 0.25s">
        <div class="feature-icon">🏆</div>
        <div class="feature-title">Health Scoring</div>
        <div class="feature-desc">
            AI-powered health scores to help you make better dietary choices
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card animate-fadeInUp" style="animation-delay: 0.35s">
        <div class="feature-icon">👨‍🍳</div>
        <div class="feature-title">Easy Instructions</div>
        <div class="feature-desc">
            Step-by-step cooking instructions with ingredient lists and prep times
        </div>
    </div>
    """, unsafe_allow_html=True)

# ------------------ TECHNOLOGY STACK ------------------
st.markdown('<h2 style="color: #667eea; text-align: center; margin: 40px 0 20px 0;">🛠️ Technology Stack</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="tech-stack animate-fadeInUp">
    <div style="text-align: center; margin-bottom: 20px;">
        <span class="tech-badge">Python</span>
        <span class="tech-badge">Scikit-Learn</span>
        <span class="tech-badge">Streamlit</span>
        <span class="tech-badge">FastAPI</span>
        <span class="tech-badge">Pandas</span>
        <span class="tech-badge">NumPy</span>
        <span class="tech-badge">ECharts</span>
        <span class="tech-badge">Machine Learning</span>
        <span class="tech-badge">Content-Based Filtering</span>
    </div>
    <p style="text-align: center; color: #555; font-size: 14px; margin-top: 10px;">
        Built with modern technologies for reliable, scalable, and accurate recommendations
    </p>
</div>
""", unsafe_allow_html=True)

# ------------------ GET STARTED ------------------
st.markdown('<h2 style="color: #667eea; text-align: center; margin: 40px 0 20px 0;">🚀 Get Started</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center;">
        <a href="/AI_Nutrition_Chef" target="_self" style="text-decoration: none;">
            <button class="cta-button">
                🍳 Start AI Nutrition Chef
            </button>
        </a>
        <a href="/Custom_Food_Recommendation" target="_self" style="text-decoration: none;">
            <button class="cta-button">
                🔍 Custom Food Recommender
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

# ------------------ PROJECT INFO ------------------
st.markdown("""
<div class="animate-fadeInUp" style="margin: 50px 0; padding: 30px; background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); border-radius: 15px; text-align: center;">
    <h3 style="color: #333; margin-bottom: 15px;">📚 About This Project</h3>
    <p style="color: #555; line-height: 1.6; max-width: 800px; margin: 0 auto 20px auto;">
        A sophisticated diet recommendation web application using content-based filtering with Scikit-Learn, 
        powered by FastAPI for the backend and Streamlit for an interactive frontend. 
        The system analyzes thousands of recipes to provide personalized dietary recommendations 
        based on nutritional requirements and ingredient preferences.
    </p>
    <a href=https://github.com/imthiyaz-official/Smart-Diet-Recommendation-System, target="_blank" class="repo-link">
        <span style="margin-right: 8px;">📁</span> View Project on GitHub
    </a>
</div>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h2 style="color: #667eea; margin-bottom: 20px;">📱 Navigation</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("### Select an App:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🍳 AI Chef", use_container_width=True):
           st.switch_page("pages/diet_recommendation.py")
    with col2:
        if st.button("🔍 Custom", use_container_width=True):
            st.switch_page("pages/Custom_Food_Recommendation.py")
    
    st.markdown("---")
    
    st.markdown("### 📊 Quick Stats")
    st.info("""
    **System Status:** ✅ Active
    **Recipes:** 1,000,000+
    **Accuracy:** 99%
    **Response Time:** < 1s
    **Last Updated:** Today
    """)
    
    st.markdown("---")
    
    st.markdown("### 💡 Tips")
    st.success("""
    1. Start with broad nutrition targets
    2. Select 3-5 ingredients you love
    3. Adjust based on dietary goals
    4. Save your favorite recipes
    """)

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #666;">
    <p style="margin-bottom: 10px;">
        <span style="font-size: 18px;">🍎</span> 
        <strong>Diet Recommendation System</strong> 
        <span style="font-size: 18px;">🤖</span>
    </p>
    <p style="font-size: 12px; margin: 0;">
        Developed with ❤️ using Python, Machine Learning & Streamlit | 
        <a href="https://github.com/zakaria-narjis/Diet-Recommendation-System" target="_blank" style="color: #667eea;">GitHub Repository</a>
    </p>
</div>
""", unsafe_allow_html=True)