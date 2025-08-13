import streamlit as st
import json
import random
from pathlib import Path
import os

# Page configuration
st.set_page_config(
    page_title="Class 9 Social Science Quiz Portal",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS for styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

    * {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .main {
        padding: 0rem 1rem;
        font-family: 'Inter', sans-serif;
    }

    .quiz-header {
        text-align: center;
        background: linear-gradient(135deg, #D16BA5 0%, #86A8E7 50%, #5FFBF1 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 3rem;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }

    .quiz-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%);
        pointer-events: none;
    }

    .quiz-title {
        font-family: 'Poppins', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        position: relative;
        z-index: 1;
    }

    .quiz-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        font-weight: 400;
        margin-top: 0.8rem;
        opacity: 0.95;
        position: relative;
        z-index: 1;
    }

    .subject-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }

    .subject-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        border: 1px solid rgba(0,0,0,0.05);
        position: relative;
        overflow: hidden;
    }

    .subject-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--accent-color);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }

    .subject-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 50px rgba(0,0,0,0.15);
    }

    .subject-card:hover::before {
        transform: scaleX(1);
    }

    .history-card { --accent-color: linear-gradient(135deg, #0061ff, #60efff); }
    .geography-card { --accent-color: linear-gradient(135deg, #95f9c3, #0b3866); }
    .civics-card { --accent-color: linear-gradient(135deg, #f7a2a1, #ffed00); }
    .economics-card { --accent-color: linear-gradient(135deg, #145277, #83d0cb); }

    .subject-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }

    .subject-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }

    .subject-description {
        font-size: 0.95rem;
        color: #6c757d;
        line-height: 1.5;
    }

    .chapter-card {
        background: white;
        border-radius: 16px;
        padding: 1.8rem;
        margin: 1rem 0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border-left: 5px solid transparent;
        cursor: pointer;
        position: relative;
    }

    .chapter-card:hover {
        transform: translateX(8px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
        border-left-color: #667eea;
    }

    .section-card {
        background: linear-gradient(135deg, #6d90b9 0%, #bbc7dc 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
        border: 1px solid rgba(0,0,0,0.05);
    }

    .section-card:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transform: scale(1.03);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }

    .quiz-question {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 8px 30px rgba(0,0,0,0.1);
        font-family: 'Inter', sans-serif;
        border: 1px solid rgba(0,0,0,0.05);
    }

    .question-text {
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 2rem;
        color: #2c3e50;
        line-height: 1.6;
    }

    .quiz-options {
        display: grid;
        gap: 1rem;
        margin-top: 1.5rem;
    }

    # Enhanced Custom CSS for 2x2 grid and color feedback
    .quiz-options-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-template-rows: 1fr 1fr;
        gap: 1rem;
        margin: 1.5rem 0;
    }

    .option-box {
        background: white;
        border: 2px solid #e9ecef;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        font-weight: 700;
        color: #495057;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-family: 'Poppins', sans-serif;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        position: relative;
        font-size: 1.2rem;
    }

    .option-box:hover {
        border-color: #667eea;
        background: linear-gradient(135deg, #f8f9fd 0%, #ffffff 100%);
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
    }

    .option-letter {
        font-size: 1.6rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
        display: block;
    }

    .option-text {
        line-height: 1.4;
        font-size: 1.2rem;
    }

    .option-correct {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%) !important;
        border: 3px solid #28a745 !important;
        color: #155724 !important;
        font-weight: 700 !important;
        box-shadow: 0 10px 30px rgba(40, 167, 69, 0.5) !important;
        transform: scale(1.08) !important;
        animation: glow-green 0.5s ease-in-out;
    }

    .option-correct::after {
        content: '✓';
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 1.5rem;
        font-weight: bold;
        color: #28a745;
        background: rgba(255,255,255,0.8);
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .option-incorrect {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%) !important;
        border: 3px solid #dc3545 !important;
        color: #721c24 !important;
        font-weight: 700 !important;
        box-shadow: 0 10px 30px rgba(220, 53, 69, 0.5) !important;
        transform: scale(1.03) !important;
        animation: shake 0.5s ease-in-out;
    }

    .option-incorrect::after {
        content: '✗';
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 1.5rem;
        font-weight: bold;
        color: #dc3545;
        background: rgba(255,255,255,0.8);
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .option-neutral {
        background: #f8f9fa !important;
        border: 2px solid #dee2e6 !important;
        color: #6c757d !important;
        opacity: 0.6 !important;
        transform: scale(0.95) !important;
    }

    @keyframes glow-green {
        0% { box-shadow: 0 0 5px rgba(40, 167, 69, 0.3); }
        50% { box-shadow: 0 0 25px rgba(40, 167, 69, 0.8); }
        100% { box-shadow: 0 10px 30px rgba(40, 167, 69, 0.5); }
    }

    @keyframes shake {
        0%, 100% { transform: scale(1.03) translateX(0); }
        25% { transform: scale(1.03) translateX(-2px); }
        75% { transform: scale(1.03) translateX(2px); }
    }

    .quiz-stats {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }

    .quiz-stats::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%);
        pointer-events: none;
    }

    .stats-content {
        position: relative;
        z-index: 1;
    }

    .explanation-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
        border-left: 5px solid #2196f3;
        padding: 1.5rem;
        margin-top: 1.5rem;
        border-radius: 12px;
        font-style: italic;
        box-shadow: 0 4px 15px rgba(33, 150, 243, 0.1);
    }

    .progress-container {
        background: rgba(102, 126, 234, 0.1);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
    }

    .navigation-buttons {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 2rem 0;
        gap: 1rem;
    }

    .btn-primary {
        background: linear-gradient(135deg, #858e96 0%, #60696b 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        cursor: pointer;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }

    .btn-primary:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }

    .btn-secondary {
        background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        cursor: pointer;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(108, 117, 125, 0.3);
    }

    .btn-secondary:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(108, 117, 125, 0.4);
    }

    .footer {
        text-align: center;
        padding: 3rem 2rem;
        color: #6c757d;
        font-style: italic;
        margin-top: 4rem;
        background: linear-gradient(135deg, #f8f9fd 0%, #ffffff 100%);
        border-radius: 20px;
        border-top: 3px solid #667eea;
    }

    /* Override Streamlit's default button styles with higher specificity */
    
    
    
    
    .stApp .main .block-container .stButton > button,
    .stApp button[kind="primary"],
    .stApp button[kind="secondary"],
    .stApp .stButton > button {
        background: linear-gradient(135deg, #08203e 0%, #557c93 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        width: 100% !important;
        height: auto !important;
    }

    .stApp .main .block-container .stButton > button:hover,
    .stApp button[kind="primary"]:hover,
    .stApp button[kind="secondary"]:hover,
    .stApp .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
        background: linear-gradient(135deg, #9d80cb 0%, #f7c2e6 100%) !important;
    }

    /* Subject-specific button colors with maximum specificity */
    .stApp .main .block-container div[data-testid="column"]:nth-child(1) .stButton > button,
    .stApp div[data-testid="column"]:first-child button[kind="secondary"],
    .stApp div[data-testid="column"]:first-child .stButton > button {
        background: linear-gradient(135deg, #0061ff 0%, #60efff 100%) !important;
        box-shadow: 0 4px 15px rgba(0, 97, 255, 0.3) !important;
    }

    .stApp .main .block-container div[data-testid="column"]:nth-child(1) .stButton > button:hover,
    .stApp div[data-testid="column"]:first-child button[kind="secondary"]:hover,
    .stApp div[data-testid="column"]:first-child .stButton > button:hover {
        background: linear-gradient(135deg, #0061ff 0%, #60efff 100%) !important;
        box-shadow: 0 8px 25px rgba(0, 97, 255, 0.4) !important;
    }

    .stApp .main .block-container div[data-testid="column"]:nth-child(2) .stButton > button,
    .stApp div[data-testid="column"]:nth-child(2) button[kind="secondary"],
    .stApp div[data-testid="column"]:nth-child(2) .stButton > button {
        background: linear-gradient(135deg, #95f9c3 0%, #0b3866 100%) !important;
        box-shadow: 0 4px 15px rgba(149, 249, 195, 0.3) !important;
    }

    .stApp .main .block-container div[data-testid="column"]:nth-child(2) .stButton > button:hover,
    .stApp div[data-testid="column"]:nth-child(2) button[kind="secondary"]:hover,
    .stApp div[data-testid="column"]:nth-child(2) .stButton > button:hover {
        background: linear-gradient(135deg, #95f9c3 0%, #0b3866 100%) !important;
        box-shadow: 0 8px 25px rgba(149, 249, 195, 0.4) !important;
    }

    /* For the second row of buttons */
    .stApp .main .block-container div[data-testid="column"]:nth-child(3) .stButton > button,
    .stApp div[data-testid="column"]:nth-child(3) button[kind="secondary"],
    .stApp div[data-testid="column"]:nth-child(3) .stButton > button {
        background: linear-gradient(135deg, #f7a2a1 0%, #ffed00 100%) !important;
        box-shadow: 0 4px 15px rgba(247, 162, 161, 0.3) !important;
    }

    .stApp .main .block-container div[data-testid="column"]:nth-child(3) .stButton > button:hover,
    .stApp div[data-testid="column"]:nth-child(3) button[kind="secondary"]:hover,
    .stApp div[data-testid="column"]:nth-child(3) .stButton > button:hover {
        background: linear-gradient(135deg, #f7a2a1 0%, #ffed00 100%) !important;
        box-shadow: 0 8px 25px rgba(247, 162, 161, 0.4) !important;
    }

    .stApp .main .block-container div[data-testid="column"]:nth-child(4) .stButton > button,
    .stApp div[data-testid="column"]:nth-child(4) button[kind="secondary"],
    .stApp div[data-testid="column"]:nth-child(4) .stButton > button {
        background: linear-gradient(135deg, #145277 0%, #83d0cb 100%) !important;
        box-shadow: 0 4px 15px rgba(20, 82, 119, 0.3) !important;
    }

    .stApp .main .block-container div[data-testid="column"]:nth-child(4) .stButton > button:hover,
    .stApp div[data-testid="column"]:nth-child(4) button[kind="secondary"]:hover,
    .stApp div[data-testid="column"]:nth-child(4) .stButton > button:hover {
        background: linear-gradient(135deg, #145277 0%, #83d0cb 100%) !important;
        box-shadow: 0 8px 25px rgba(20, 82, 119, 0.4) !important;
    }

    /* Alternative approach using button key attributes */
    .stApp button[key="history"] {
        background: linear-gradient(135deg, #0061ff 0%, #60efff 100%) !important;
        box-shadow: 0 4px 15px rgba(0, 97, 255, 0.3) !important;
    }

    .stApp button[key="history"]:hover {
        background: linear-gradient(135deg, #0061ff 0%, #60efff 100%) !important;
        box-shadow: 0 8px 25px rgba(0, 97, 255, 0.4) !important;
    }

    .stApp button[key="geography"] {
        background: linear-gradient(135deg, #95f9c3 0%, #0b3866 100%) !important;
        box-shadow: 0 4px 15px rgba(149, 249, 195, 0.3) !important;
    }

    .stApp button[key="geography"]:hover {
        background: linear-gradient(135deg, #95f9c3 0%, #0b3866 100%) !important;
        box-shadow: 0 8px 25px rgba(149, 249, 195, 0.4) !important;
    }

    .stApp button[key="civics"] {
        background: linear-gradient(135deg, #f7a2a1 0%, #ffed00 100%) !important;
        box-shadow: 0 4px 15px rgba(247, 162, 161, 0.3) !important;
    }

    .stApp button[key="civics"]:hover {
        background: linear-gradient(135deg, #f7a2a1 0%, #ffed00 100%) !important;
        box-shadow: 0 8px 25px rgba(247, 162, 161, 0.4) !important;
    }

    .stApp button[key="economics"] {
        background: linear-gradient(135deg, #145277 0%, #83d0cb 100%) !important;
        box-shadow: 0 4px 15px rgba(20, 82, 119, 0.3) !important;
    }

    .stApp button[key="economics"]:hover {
        background: linear-gradient(135deg, #145277 0%, #83d0cb 100%) !important;
        box-shadow: 0 8px 25px rgba(20, 82, 119, 0.4) !important;
    }

    .stProgress > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }

    .metric-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }

    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        text-align: center;
        border-top: 4px solid #667eea;
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin: 0;
    }

    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .animate-fade-in {
        animation: fadeIn 0.5s ease-in;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .animate-scale-in {
        animation: scaleIn 0.3s ease-out;
    }

    @keyframes scaleIn {
        from { transform: scale(0.9); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'selected_subject' not in st.session_state:
    st.session_state.selected_subject = None
if 'selected_chapter' not in st.session_state:
    st.session_state.selected_chapter = None
if 'selected_section' not in st.session_state:
    st.session_state.selected_section = None
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = None
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = None


def load_quiz_data():
    """Load quiz data from JSON files"""
    data = {}
    data_dir = Path("./quiz_data")

    if not data_dir.exists():
        st.error("📁 Quiz data directory not found!")
        return data

    for json_file in data_dir.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                file_data = json.load(f)
                data.update(file_data)
        except Exception as e:
            st.error(f"❌ Error loading {json_file}: {e}")

    return data


def show_homepage():
    """Display the enhanced homepage"""
    st.markdown("""
    <div class="quiz-header animate-fade-in">
        <h1 class="quiz-title">📚 Class 9 Social Science Quiz Portal</h1>
        <p class="quiz-subtitle">Practice your chapter knowledge</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ◎ Choose Your Learning Adventure")

    # Create custom styled buttons using columns and forms
    col1, col2 = st.columns(2)

    subjects = [
        {"name": "History", "icon": "📜", "gradient": "linear-gradient(135deg, #0061ff 0%, #60efff 100%)"},
        {"name": "Geography", "icon": "🌍", "gradient": "linear-gradient(135deg, #95f9c3 0%, #0b3866 100%)"},
        {"name": "Civics", "icon": "🗳️", "gradient": "linear-gradient(135deg, #f7a2a1 0%, #ffed00 100%)"},
        {"name": "Economics", "icon": "💰", "gradient": "linear-gradient(135deg, #145277 0%, #83d0cb 100%)"}
    ]

    # History button
    with col1:
        st.markdown(f"""
        <div style="margin-bottom: 1rem;">
            <div style="
                background: linear-gradient(135deg, #0061ff 0%, #60efff 100%);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 1.2rem 2rem;
                font-weight: 600;
                font-size: 1.1rem;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(0, 97, 255, 0.3);
                width: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
                font-family: 'Inter', sans-serif;
            ">
                <span style="font-size: 1.5rem;">📜</span>
                <span>History</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Select History", key="history", use_container_width=True, type="primary"):
            st.session_state.selected_subject = "History"
            st.session_state.current_page = 'chapters'
            st.rerun()

    # Geography button
    with col2:
        st.markdown(f"""
        <div style="margin-bottom: 1rem;">
            <div style="
                background: linear-gradient(135deg, #95f9c3 0%, #0b3866 100%);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 1.2rem 2rem;
                font-weight: 600;
                font-size: 1.1rem;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(149, 249, 195, 0.3);
                width: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
                font-family: 'Inter', sans-serif;
            ">
                <span style="font-size: 1.5rem;">🌍</span>
                <span>Geography</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Select Geography", key="geography", use_container_width=True, type="primary"):
            st.session_state.selected_subject = "Geography"
            st.session_state.current_page = 'chapters'
            st.rerun()

    # Civics button
    with col1:
        st.markdown(f"""
        <div style="margin-bottom: 1rem;">
            <div style="
                background: linear-gradient(135deg, #f7a2a1 0%, #ffed00 100%);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 1.2rem 2rem;
                font-weight: 600;
                font-size: 1.1rem;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(247, 162, 161, 0.3);
                width: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
                font-family: 'Inter', sans-serif;
            ">
                <span style="font-size: 1.5rem;">🗳️</span>
                <span>Civics</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Select Civics", key="civics", use_container_width=True, type="primary"):
            st.session_state.selected_subject = "Civics"
            st.session_state.current_page = 'chapters'
            st.rerun()

    # Economics button
    with col2:
        st.markdown(f"""
        <div style="margin-bottom: 1rem;">
            <div style="
                background: linear-gradient(135deg, #145277 0%, #83d0cb 100%);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 1.2rem 2rem;
                font-weight: 600;
                font-size: 1.1rem;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(20, 82, 119, 0.3);
                width: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
                font-family: 'Inter', sans-serif;
            ">
                <span style="font-size: 1.5rem;">💰</span>
                <span>Economics</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Select Economics", key="economics", use_container_width=True, type="primary"):
            st.session_state.selected_subject = "Economics"
            st.session_state.current_page = 'chapters'
            st.rerun()

    # Add CSS to hide the Streamlit buttons visually but keep them functional
    st.markdown("""
    <style>
    /* Hide the actual Streamlit buttons but keep them clickable */
    button[kind="primary"] {
        opacity: 0 !important;
        position: absolute !important;
        z-index: 10 !important;
        width: 100% !important;
        height: 80px !important;
        margin-top: -80px !important;
        cursor: pointer !important;
    }
    </style>
    """, unsafe_allow_html=True)


def show_chapters():
    """Display enhanced chapters for selected subject"""
    quiz_data = load_quiz_data()

    st.markdown(f"""
    <div class="animate-fade-in">
        <h2>📚 {st.session_state.selected_subject} - Chapters</h2>
        <p>Select a chapter to explore its quiz sections</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⬅️ Back to Home", key="back_to_home"):
        st.session_state.current_page = 'home'
        st.rerun()

    subject_data = quiz_data.get(st.session_state.selected_subject, {})

    if not subject_data:
        st.warning(f"📭 No data found for {st.session_state.selected_subject}")
        return

    st.markdown("---")

    for chapter_name, chapter_data in subject_data.items():
        with st.expander(f"📖 {chapter_name}", expanded=False):
            sections_count = len(chapter_data)
            total_questions = sum(len(questions) for questions in chapter_data.values())

            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"**Sections:** {sections_count} | **Total Questions:** {total_questions}")
            with col2:
                st.markdown("📊 **Difficulty:** Mixed")
            with col3:
                if st.button(f"Start Chapter", key=f"chapter_{chapter_name}", use_container_width=True):
                    st.session_state.selected_chapter = chapter_name
                    st.session_state.current_page = 'sections'
                    st.rerun()


def show_sections():
    """Display enhanced sections for selected chapter"""
    quiz_data = load_quiz_data()

    st.markdown(f"""
    <div class="animate-fade-in">
        <h2>📑 {st.session_state.selected_chapter}</h2>
        <p><strong>Subject:</strong> {st.session_state.selected_subject}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⬅️ Back to Chapters", key="back_to_chapters"):
        st.session_state.current_page = 'chapters'
        st.rerun()

    chapter_data = quiz_data.get(st.session_state.selected_subject, {}).get(st.session_state.selected_chapter, {})

    if not chapter_data:
        st.warning("📭 No sections found for this chapter")
        return

    st.markdown("### 🎯 Available Quiz Sections")
    st.markdown("---")

    for section_name, questions in chapter_data.items():
        with st.container():
            col1, col2, col3 = st.columns([4, 1, 1])
            with col1:
                st.markdown(f"**📝 {section_name}**")
                st.markdown(f"*Test your understanding of {section_name.lower()}*")
            with col2:
                st.markdown(f"**{len(questions)}** questions")
            with col3:
                if st.button("🚀 Start Quiz", key=f"section_{section_name}", use_container_width=True):
                    st.session_state.selected_section = section_name
                    st.session_state.quiz_data = questions
                    st.session_state.current_question = 0
                    st.session_state.answers = {}
                    st.session_state.show_answer = False
                    st.session_state.selected_option = None
                    st.session_state.current_page = 'quiz'
                    st.rerun()
            st.markdown("---")


def show_quiz():
    """Display the enhanced quiz interface with colored answer feedback"""
    if not st.session_state.quiz_data:
        st.error("❌ No quiz data available!")
        return

    questions = st.session_state.quiz_data
    current_q = st.session_state.current_question

    # Quiz header with better styling
    st.markdown(f"""
    <div class="animate-fade-in">
        <h2>🎯 {st.session_state.selected_section}</h2>
        <p><strong>Chapter:</strong> {st.session_state.selected_chapter}</p>
    </div>
    """, unsafe_allow_html=True)

    # Enhanced progress tracking
    progress = (current_q + 1) / len(questions)
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    st.progress(progress)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"**Question {current_q + 1} of {len(questions)}** • {progress * 100:.0f}% Complete")
    st.markdown('</div>', unsafe_allow_html=True)

    # Navigation
    if st.button("⬅️ Back to Sections", key="back_to_sections"):
        st.session_state.current_page = 'sections'
        st.rerun()

    # Current question with enhanced styling
    question_data = questions[current_q]

    st.markdown(f"""
    <div class="quiz-question animate-scale-in">
        <div class="question-text">
            <strong>Q{current_q + 1}:</strong> {question_data['question']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Enhanced answer options in 2x2 grid with color feedback
    st.markdown("### Select your answer:")

    # Create 2x2 grid for options
    row1_col1, row1_col2 = st.columns(2, gap="medium")
    row2_col1, row2_col2 = st.columns(2, gap="medium")

    option_columns = [row1_col1, row1_col2, row2_col1, row2_col2]

    for i, option in enumerate(question_data['options']):
        button_key = f"option_{current_q}_{i}"
        option_letter = chr(65 + i)  # A, B, C, D

        # Use the appropriate column for 2x2 layout
        with option_columns[i]:
            # Determine button appearance based on answer state
            if st.session_state.show_answer and current_q in st.session_state.answers:
                selected_answer = st.session_state.answers[current_q]
                correct_answer = question_data['correct_answer']

                if i == correct_answer:
                    # Correct answer - always green
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
                        border: 3px solid #28a745;
                        border-radius: 15px;
                        padding: 1.5rem;
                        text-align: center;
                        color: #155724;
                        font-weight: 700;
                        font-size: 1.2rem;
                        min-height: 120px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        box-shadow: 0 8px 25px rgba(40, 167, 69, 0.4);
                        transform: scale(1.05);
                        transition: all 0.3s ease;
                        position: relative;
                        overflow: hidden;
                        margin-bottom: 1rem;
                    ">
                        <div style="font-size: 1.6rem; margin-bottom: 0.5rem;">
                            <strong>{option_letter}</strong> ✅
                        </div>
                        <div style="line-height: 1.4;">{option}</div>
                    </div>
                    """, unsafe_allow_html=True)
                elif i == selected_answer and i != correct_answer:
                    # Wrong selection - red
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
                        border: 3px solid #dc3545;
                        border-radius: 15px;
                        padding: 1.5rem;
                        text-align: center;
                        color: #721c24;
                        font-weight: 700;
                        font-size: 1.2rem;
                        min-height: 120px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        box-shadow: 0 8px 25px rgba(220, 53, 69, 0.4);
                        transform: scale(1.02);
                        transition: all 0.3s ease;
                        margin-bottom: 1rem;
                    ">
                        <div style="font-size: 1.6rem; margin-bottom: 0.5rem;">
                            <strong>{option_letter}</strong> ❌
                        </div>
                        <div style="line-height: 1.4;">{option}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Other options - grey/dimmed
                    st.markdown(f"""
                    <div style="
                        background: #f8f9fa;
                        border: 2px solid #dee2e6;
                        border-radius: 15px;
                        padding: 1.5rem;
                        text-align: center;
                        color: #6c757d;
                        font-weight: 500;
                        font-size: 1.2rem;
                        min-height: 120px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        opacity: 0.6;
                        transition: all 0.3s ease;
                        margin-bottom: 1rem;
                    ">
                        <div style="font-size: 1.6rem; margin-bottom: 0.5rem;">
                            <strong>{option_letter}</strong>
                        </div>
                        <div style="line-height: 1.4;">{option}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                # Before answering - show clickable Streamlit buttons
                button_style = f"""
                    <style>
                    div[data-testid="column"]:nth-child({(i % 2) + 1}) .stButton > button {{
                        background: white !important;
                        border: 2px solid #e9ecef !important;
                        border-radius: 15px !important;
                        padding: 1.5rem !important;
                        font-weight: 600 !important;
                        color: #495057 !important;
                        min-height: 120px !important;
                        font-size: 1.1rem !important;
                        transition: all 0.3s ease !important;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
                    }}

                    div[data-testid="column"]:nth-child({(i % 2) + 1}) .stButton > button:hover {{
                        border-color: #667eea !important;
                        background: linear-gradient(135deg, #f8f9fd 0%, #ffffff 100%) !important;
                        transform: translateY(-5px) scale(1.02) !important;
                        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3) !important;
                    }}
                    </style>
                """
                st.markdown(button_style, unsafe_allow_html=True)

                if st.button(f"{option}", key=button_key, use_container_width=True):
                    st.session_state.answers[current_q] = i
                    st.session_state.selected_option = i
                    st.session_state.show_answer = True
                    st.rerun()

    # Show answer feedback with enhanced styling
    if st.session_state.show_answer and current_q in st.session_state.answers:
        selected_answer = st.session_state.answers[current_q]
        correct_answer = question_data['correct_answer']

        if selected_answer == correct_answer:
            st.success("🎉 **Excellent!** You got it right!")
        else:
            st.error(
                f"❌ **Not quite right.** The correct answer is: **{chr(65 + correct_answer)}. {question_data['options'][correct_answer]}**")

        # Enhanced explanation box
        st.markdown(f"""
        <div class="explanation-box">
            <strong>💡 Explanation:</strong><br>
            {question_data['explanation']}
        </div>
        """, unsafe_allow_html=True)

        # Enhanced navigation buttons
        st.markdown('<div class="navigation-buttons">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if current_q > 0:
                if st.button("⬅️ Previous Question", key="prev_btn", use_container_width=True):
                    st.session_state.current_question -= 1
                    st.session_state.show_answer = False
                    st.session_state.selected_option = None
                    st.rerun()

        with col2:
            # Show current position
            st.markdown(
                f'<div style="text-align: center; padding: 0.8rem; color: #6c757d;">Question {current_q + 1}/{len(questions)}</div>',
                unsafe_allow_html=True)

        with col3:
            if current_q < len(questions) - 1:
                if st.button("Next Question ➡️", key="next_btn", use_container_width=True):
                    st.session_state.current_question += 1
                    st.session_state.show_answer = False
                    st.session_state.selected_option = None
                    st.rerun()
            else:
                if st.button("🏁 View Results", key="finish_btn", use_container_width=True):
                    st.session_state.current_page = 'results'
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


def show_results():
    """Display enhanced quiz results"""
    if not st.session_state.quiz_data or not st.session_state.answers:
        st.error("❌ No quiz results available!")
        return

    questions = st.session_state.quiz_data
    answers = st.session_state.answers

    # Calculate comprehensive statistics
    correct_answers = 0
    total_questions = len(questions)

    for q_idx, user_answer in answers.items():
        if user_answer == questions[q_idx]['correct_answer']:
            correct_answers += 1

    score_percentage = (correct_answers / total_questions) * 100
    wrong_answers = total_questions - correct_answers

    # Enhanced results display
    st.markdown(f"""
    <div class="quiz-stats animate-fade-in">
        <div class="stats-content">
            <h2>🎊 Quiz Complete!</h2>
            <h1 style="font-size: 4rem; margin: 1rem 0;">{score_percentage:.0f}%</h1>
            <h3>Your Score: {correct_answers}/{total_questions}</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Detailed metrics
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{correct_answers}</div>
            <div class="metric-label">Correct</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{wrong_answers}</div>
            <div class="metric-label">Wrong</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_questions}</div>
            <div class="metric-label">Total</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        accuracy = "A+" if score_percentage >= 90 else "A" if score_percentage >= 80 else "B" if score_percentage >= 70 else "C" if score_percentage >= 60 else "D"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{accuracy}</div>
            <div class="metric-label">Grade</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Enhanced performance message with better styling
    if score_percentage >= 90:
        st.success("🌟 **Outstanding Performance!** You have truly mastered this topic! Keep up the excellent work!")
    elif score_percentage >= 80:
        st.success("🎯 **Great Job!** You have a strong understanding of this topic. Well done!")
    elif score_percentage >= 70:
        st.info("👍 **Good Work!** You're on the right track. A little more practice will make you perfect!")
    elif score_percentage >= 60:
        st.warning("📚 **Keep Learning!** You have a basic understanding. Review the chapter and try again!")
    else:
        st.warning("💪 **Don't Give Up!** Learning takes time. Review the material and practice more!")

    # Enhanced action buttons
    st.markdown("### 🎯 What's Next?")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔄 Retake This Quiz", key="retake", use_container_width=True):
            st.session_state.current_question = 0
            st.session_state.answers = {}
            st.session_state.show_answer = False
            st.session_state.selected_option = None
            st.session_state.current_page = 'quiz'
            st.rerun()

    with col2:
        if st.button("📚 Try Another Section", key="another_section", use_container_width=True):
            st.session_state.current_page = 'sections'
            st.rerun()

    with col3:
        if st.button("🏠 Back to Home", key="home", use_container_width=True):
            st.session_state.current_page = 'home'
            st.session_state.selected_subject = None
            st.session_state.selected_chapter = None
            st.session_state.selected_section = None
            st.rerun()

    # Show detailed question-by-question results
    if st.expander("📋 Detailed Results", expanded=False):
        for q_idx, question_data in enumerate(questions):
            if q_idx in answers:
                user_answer = answers[q_idx]
                correct_answer = question_data['correct_answer']
                is_correct = user_answer == correct_answer

                status_icon = "✅" if is_correct else "❌"
                status_color = "#28a745" if is_correct else "#dc3545"

                st.markdown(f"""
                <div style="background: white; padding: 1rem; margin: 0.5rem 0; border-radius: 10px; 
                     border-left: 4px solid {status_color}; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                    <strong>Q{q_idx + 1}: {status_icon}</strong> {question_data['question']}<br>
                    <strong>Your Answer:</strong> {chr(65 + user_answer)}. {question_data['options'][user_answer]}<br>
                    <strong>Correct Answer:</strong> {chr(65 + correct_answer)}. {question_data['options'][correct_answer]}
                </div>
                """, unsafe_allow_html=True)


# Main app logic with enhanced error handling
def main():
    try:
        if st.session_state.current_page == 'home':
            show_homepage()
        elif st.session_state.current_page == 'chapters':
            show_chapters()
        elif st.session_state.current_page == 'sections':
            show_sections()
        elif st.session_state.current_page == 'quiz':
            show_quiz()
        elif st.session_state.current_page == 'results':
            show_results()
        else:
            # Fallback to home page
            st.session_state.current_page = 'home'
            show_homepage()

    except Exception as e:
        st.error(f"⚠️ An error occurred: {str(e)}")
        st.info("Please refresh the page or go back to the home page.")

        if st.button("🏠 Go to Home"):
            st.session_state.current_page = 'home'
            st.rerun()

    # Enhanced footer
    st.markdown("""
    <div class="footer">
        <h4>📚 Class 9 Social Science Quiz Portal</h4>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()