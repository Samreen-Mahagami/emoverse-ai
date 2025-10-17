"""
EmoVerse AI - Your AI Universe of Emotional Learning
Production Version - Toggle between Demo and Real AWS Backend
"""
import streamlit as st
import requests
import time as time_module
import boto3
from io import BytesIO

# AWS Configuration
AWS_REGION = "us-east-1"
API_BASE = "https://lckrtb0j9e.execute-api.us-east-1.amazonaws.com/Prod"
S3_BUCKET = "sel-platform-uploads-089580247707"

# Try to initialize AWS clients
try:
    s3_client = boto3.client('s3', region_name=AWS_REGION)
    textract_client = boto3.client('textract', region_name=AWS_REGION)
    AWS_AVAILABLE = True
except:
    s3_client = None
    textract_client = None
    AWS_AVAILABLE = False

# Page config
st.set_page_config(
    page_title="EmoVerse AI - Emotional Learning Platform",
    page_icon="🌈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "EmoVerse AI - Your AI Universe of Emotional Learning"
    }
)

# Custom CSS for fun, colorful design
st.markdown("""
<style>
    /* Main background with gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Card-like containers - white background */
    .stTabs [data-baseweb="tab-panel"] {
        background-color: rgba(255, 255, 255, 0.98) !important;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        margin-top: 20px;
        min-height: 400px;
    }
    
    /* Ensure all content in tabs has proper spacing */
    .stTabs [data-baseweb="tab-panel"] > div {
        padding: 10px 0;
    }
    
    /* Clean, readable font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%) !important;
        background-size: 400% 400% !important;
        animation: gradient 15s ease infinite !important;
    }
    
    /* Colorful headers - Slightly larger */
    h1 {
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
        font-size: 2.4em !important;
        text-align: center;
        animation: bounce 2s ease infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    h2 {
        color: #2d3748 !important;
        font-weight: 700 !important;
        font-size: 1.6em !important;
    }
    
    h3 {
        color: #2d3748 !important;
        font-weight: 700 !important;
        font-size: 1.35em !important;
    }
    
    /* Clean readable text with proper spacing */
    p {
        font-size: 1.1rem !important;
        color: #2d3748 !important;
        line-height: 1.7 !important;
        margin: 0.8rem 0 !important;
        padding: 0 !important;
        font-weight: 600 !important;
    }
    
    label {
        font-size: 1.1rem !important;
        color: #2d3748 !important;
        font-weight: 700 !important;
        display: block !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Headers with proper spacing */
    h2 {
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        padding: 0 !important;
        clear: both !important;
    }
    
    h3 {
        margin-top: 1.5rem !important;
        margin-bottom: 0.8rem !important;
        padding: 0 !important;
        clear: both !important;
    }
    
    /* Radio buttons - Simple styling without layout changes */
    .stRadio > label {
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        color: #2d3748 !important;
        margin-bottom: 0.8rem !important;
    }
    
    .stRadio {
        padding: 10px 0 !important;
    }
    
    .stRadio > div {
        gap: 10px !important;
    }
    
    .stRadio label {
        cursor: pointer !important;
        padding: 12px !important;
        border-radius: 8px !important;
        transition: background-color 0.2s !important;
    }
    
    .stRadio label:hover {
        background-color: #f0f4ff !important;
    }
    
    /* Input fields - white background, dark text */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background-color: white !important;
        color: #2d3748 !important;
        font-size: 1.1rem !important;
        line-height: 1.5 !important;
        font-weight: 600 !important;
    }
    
    .stTextInput label, .stTextArea label, .stSelectbox label {
        margin-bottom: 0.5rem !important;
        display: block !important;
    }
    
    /* Button text */
    .stButton > button {
        font-size: 1.1rem !important;
        line-height: 1.5 !important;
    }
    
    /* Sidebar styling - Normal scrolling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        border-radius: 0 20px 20px 0;
    }
    
    /* Sidebar content */
    [data-testid="stSidebar"] > div {
        padding: 2rem 1rem !important;
    }
    
    /* Mobile hamburger menu - Make it more visible */
    [data-testid="collapsedControl"] {
        background-color: rgba(102, 126, 234, 0.9) !important;
        border-radius: 8px !important;
        padding: 8px !important;
        margin: 10px !important;
    }
    
    [data-testid="collapsedControl"] svg {
        color: white !important;
        font-size: 1.5em !important;
    }
    
    /* Mobile responsive adjustments */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem !important;
        }
        
        h1 {
            font-size: 1.8em !important;
        }
        
        .stButton > button[kind="primary"],
        .stButton > button[kind="secondary"] {
            padding: 30px 40px !important;
            font-size: 1.8em !important;
            height: 140px !important;
            min-width: 200px !important;
        }
    }
    
    /* Main content - full width */
    .main .block-container {
        max-width: 100% !important;
        padding: 2rem 3rem !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }
    
    [data-testid="stSidebar"] label {
        color: white !important;
    }
    
    [data-testid="stSidebar"] input {
        background-color: white !important;
        color: #2d3748 !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox label {
        color: white !important;
    }
    
    /* Sidebar buttons - standardized size */
    [data-testid="stSidebar"] .stButton > button {
        height: auto !important;
        padding: 14px 24px !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        min-height: 50px !important;
        max-width: 100% !important;
    }
    
    /* Button styling */
    .stButton {
        margin: 10px 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 16px 32px;
        font-size: 1.2rem;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        cursor: pointer;
        line-height: 1.5;
        height: auto;
        min-height: 55px;
        max-width: 400px;
        margin: 0 auto;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* User selection buttons - clean and aligned */
    .stButton > button[kind="primary"],
    .stButton > button[kind="secondary"] {
        padding: 50px 60px !important;
        font-size: 2.5em !important;
        height: 180px !important;
        border-radius: 12px !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.3s ease !important;
        font-weight: 800 !important;
        min-width: 300px !important;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    .stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
    }
    
    .stButton > button[kind="primary"]:hover,
    .stButton > button[kind="secondary"]:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 15px;
        border: 2px solid #667eea;
        padding: 12px;
        font-size: 1.1rem;
        line-height: 1.5;
        font-weight: 600;
    }
    
    /* Tabs - Make all visible without scrolling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        margin-bottom: 1rem;
        overflow-x: visible !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 12px 12px 0 0;
        padding: 12px 18px;
        font-size: 0.95rem;
        font-weight: 600;
        color: #667eea;
        border: 2px solid #667eea;
        line-height: 1.5;
        white-space: nowrap;
        flex-shrink: 1;
        min-width: fit-content;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    
    /* Tab content spacing */
    .stTabs [data-baseweb="tab-panel"] > div {
        padding: 1rem 0;
    }
    
    /* Ensure tabs container doesn't overflow */
    .stTabs {
        overflow: visible !important;
    }
    
    .stTabs > div {
        overflow-x: visible !important;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 15px;
        border-left: 5px solid #667eea;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2em;
        color: #667eea;
        font-weight: bold;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 20px;
        border: 3px dashed #667eea;
        margin: 15px 0;
    }
    
    /* Complete Expander Fix - No Overlapping */
    
    /* Main expander container */
    [data-testid="stExpander"] {
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 12px !important;
        margin: 20px 0 !important;
        background: white !important;
        overflow: visible !important;
    }
    
    /* Expander header */
    .streamlit-expanderHeader {
        background-color: rgba(102, 126, 234, 0.1) !important;
        padding: 20px !important;
        min-height: 70px !important;
        display: block !important;
        cursor: pointer !important;
        border-radius: 10px 10px 0 0 !important;
        position: relative !important;
    }
    
    /* Title text - make it visible and clear */
    .streamlit-expanderHeader p {
        display: inline-block !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        color: #2d3748 !important;
        margin: 0 !important;
        padding: 5px 0 !important;
        line-height: 1.8 !important;
        max-width: calc(100% - 50px) !important;
        vertical-align: middle !important;
    }
    
    /* COMPLETELY hide all text except the title */
    .streamlit-expanderHeader {
        text-indent: 0 !important;
    }
    
    .streamlit-expanderHeader span,
    .streamlit-expanderHeader div:not(:has(p)):not(:has(svg)) {
        font-size: 0 !important;
        width: 0 !important;
        height: 0 !important;
        display: none !important;
        visibility: hidden !important;
        position: absolute !important;
        left: -9999px !important;
    }
    
    /* Hide any text node that contains 'key' */
    .streamlit-expanderHeader::before {
        content: '' !important;
        font-size: 0 !important;
    }
    
    /* Show SVG icon */
    .streamlit-expanderHeader svg {
        display: inline-block !important;
        width: 30px !important;
        height: 30px !important;
        vertical-align: middle !important;
        margin-left: 10px !important;
        float: right !important;
    }
    
    /* Expander content */
    .streamlit-expanderContent {
        padding: 25px !important;
        background-color: white !important;
        border-radius: 0 0 10px 10px !important;
    }
    
    /* Clean summary styling */
    details summary {
        list-style: none !important;
        cursor: pointer !important;
    }
    
    details summary::-webkit-details-marker {
        display: none !important;
    }
    
    .streamlit-expanderContent {
        padding: 20px !important;
        background-color: rgba(255, 255, 255, 0.5) !important;
        border-radius: 0 0 10px 10px !important;
    }
    
    /* Force hide any background text/keys */
    details summary::before,
    details summary::after {
        display: none !important;
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        border-radius: 15px;
        border: 2px solid #667eea;
    }
    
    .stSelectbox select {
        font-size: 1.1rem !important;
        line-height: 1.5 !important;
        font-weight: 600 !important;
    }
    
    /* Fun emoji decorations */
    .emoji-float {
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'student_id' not in st.session_state:
    st.session_state.student_id = None
if 'grade_level' not in st.session_state:
    st.session_state.grade_level = 1
if 'processed_content' not in st.session_state:
    st.session_state.processed_content = None
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'current_story' not in st.session_state:
    st.session_state.current_story = None
if 'regenerate_count' not in st.session_state:
    st.session_state.regenerate_count = 0
if 'quiz' not in st.session_state:
    st.session_state.quiz = None
if 'use_aws' not in st.session_state:
    st.session_state.use_aws = False
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = None
if 'aws_results' not in st.session_state:
    st.session_state.aws_results = None

# AWS Helper Functions
def upload_to_s3(file, student_id):
    """Upload file to S3"""
    try:
        file_key = f"uploads/{student_id}/{file.name}"
        s3_client.upload_fileobj(file, S3_BUCKET, file_key)
        return file_key
    except Exception as e:
        st.error(f"S3 Upload Error: {str(e)}")
        return None

def extract_text_from_s3(file_key):
    """Extract text using AWS Textract"""
    try:
        response = textract_client.detect_document_text(
            Document={'S3Object': {'Bucket': S3_BUCKET, 'Name': file_key}}
        )
        
        text = ""
        for block in response['Blocks']:
            if block['BlockType'] == 'LINE':
                text += block['Text'] + "\n"
        
        return text.strip()
    except Exception as e:
        st.error(f"Textract Error: {str(e)}")
        return None

def start_content_generation(extracted_text, grade_level, story_theme="friendship", quiz_type="multiple_choice"):
    """Start async content generation"""
    try:
        response = requests.post(
            f"{API_BASE}/orchestrate",
            json={
                "extracted_text": extracted_text,
                "grade_level": f"Grade {grade_level}",
                "story_theme": story_theme,
                "quiz_type": quiz_type
            },
            timeout=10
        )
        
        if response.status_code == 202:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Request Error: {str(e)}")
        return None

def check_job_status(job_id):
    """Check job status"""
    try:
        response = requests.get(f"{API_BASE}/status/{job_id}", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

# Main app
def main():
    # Large EmoVerse AI title
    st.markdown("""
        <h1 style='text-align: center; color: White; font-size: 3.4em; 
                   text-shadow: 3px 3px 6px rgba(0,0,0,0.3); 
                   font-weight: 900; margin-top: 5px; margin-bottom: 5px;'>
            🌈 Welcome to EmoVerse AI 🚀
        </h1>
    """, unsafe_allow_html=True)
    
    # Tagline below title
    st.markdown("""
        <div style='text-align: center; color: Black; font-size: 1.2em; 
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3); 
                    margin-bottom: 30px; font-weight: 600;'>
            ✨ Your AI Universe of Emotional Learning ✨
        </div>
    """, unsafe_allow_html=True)
    
    # User type selection
    if st.session_state.user_type is None:
        # Main heading with gap
        st.markdown("""
            <div style='text-align: center; color: white; font-size: 2em; 
                        text-shadow: 2px 2px 4px rgba(0,0,0,0.3); 
                        margin: 40px 0 40px 0;
                        font-weight: 700;'>
                🎯 Who Are You?
            </div>
        """, unsafe_allow_html=True)
        
        # Center the buttons with proper spacing
        col_left, col1, col_gap, col2, col_right = st.columns([1.1, 1.4, 1.4, 1.4, 1])
        
        with col1:
            # Student button
            if st.button("👨‍🎓 Student", key="student_btn", use_container_width=True, type="primary"):
                st.session_state.user_type = "student"
                st.rerun()
            # Tagline directly below student button
            st.markdown("""
                <div style='text-align: center; color: white; font-size: 1.1em; 
                            margin-top: 20px; font-weight: 600;
                            text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
                            white-space: nowrap;'>
                    📚 Start your emotional learning adventure
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Teacher button
            if st.button("👩‍🏫 Teacher", key="teacher_btn", use_container_width=True, type="secondary"):
                st.session_state.user_type = "teacher"
                st.rerun()
            # Tagline directly below teacher button
            st.markdown("""
                <div style='text-align: center; color: white; font-size: 1.1em; 
                            margin-top: 20px; font-weight: 600;
                            text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
                            white-space: nowrap;'>
                    🎓 Create lesson plans & track progress
                </div>
            """, unsafe_allow_html=True)
    
    elif st.session_state.user_type == "student":
        student_interface()
    
    elif st.session_state.user_type == "teacher":
        teacher_interface()

def student_interface():
    # Student ID input in main area
    if not st.session_state.student_id:
        st.markdown("""
            <div style='text-align: center; color: white; font-size: 2em; 
                        text-shadow: 2px 2px 4px rgba(0,0,0,0.3); 
                        margin: 30px 0 40px 0;
                        font-weight: 700;'>
                🎨 Student Portal - Login
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1.5, 2, 1.5])
        with col2:
            student_id_input = st.text_input("Enter Student ID", placeholder="e.g., student123", key="student_id_input")
            grade_level = st.selectbox("Select Grade Level", range(1, 11), key="grade_select")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🚀 Start Learning", use_container_width=True, key="start_learning_btn"):
                if student_id_input:
                    st.session_state.student_id = student_id_input
                    st.session_state.grade_level = grade_level
                    st.rerun()
                else:
                    st.error("Please enter a Student ID")
            
            if st.button("⬅️ Back to Main Menu", use_container_width=True, key="student_back_btn"):
                st.session_state.user_type = None
                st.rerun()
    else:
        # Show student info in header
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 15px; border-radius: 15px; text-align: center; 
                            color: white; font-size: 1.1em; margin-bottom: 20px;'>
                    👨‍🎓 <strong>Student:</strong> {st.session_state.student_id} | 
                    📚 <strong>Grade:</strong> {st.session_state.grade_level}
                </div>
            """, unsafe_allow_html=True)
    
    if st.session_state.student_id:
        # Fun welcome message
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 12px; border-radius: 15px; text-align: center; 
                        color: white; font-size: 1.05em; margin-bottom: 15px;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
                🎉 Welcome, {st.session_state.student_id}! Let's learn together! 🌟
            </div>
        """, unsafe_allow_html=True)
        
        # AWS Toggle
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if AWS_AVAILABLE:
                st.session_state.use_aws = st.checkbox(
                    "🚀 Use Real AWS Backend (processes real PDFs)", 
                    value=st.session_state.use_aws,
                    help="Check to use real AWS Textract + Bedrock AI. Uncheck for instant demo."
                )
                if st.session_state.use_aws:
                    st.info("✅ AWS Mode: Will process real documents with Textract + Bedrock")
                else:
                    st.info("⚡ Demo Mode: Instant results with sample content")
            else:
                st.warning("⚠️ AWS not configured. Using demo mode.")
                st.session_state.use_aws = False
        
        # File upload section
        st.markdown("### 📚 Upload Your Learning Material")
        if st.session_state.use_aws:
            st.markdown("*Upload a real PDF - AWS will extract text and generate content!* ✨")
        else:
            st.markdown("*Drop a PDF or image here and watch the magic happen!* ✨")
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'png', 'jpg', 'jpeg'],
            help="Upload a PDF or image to start learning!"
        )
        
        if uploaded_file:
            st.success(f"📄 Got it! File: {uploaded_file.name}")
            
        if uploaded_file:
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1.5, 2, 1.5])
            with col2:
                if st.session_state.use_aws:
                    process_button = st.button("🚀 Process with AWS!", use_container_width=True)
                else:
                    process_button = st.button("🚀 Process My Document!", use_container_width=True)
        
        if uploaded_file and process_button:
            if st.session_state.use_aws and AWS_AVAILABLE:
                # REAL AWS PROCESSING
                process_with_aws(uploaded_file)
            else:
                # DEMO PROCESSING
                with st.spinner("🔮 Processing your document with AI magic..."):
                    import time
                    time.sleep(1)  # Simulate processing
                    
                st.balloons()
                st.success("✨ Document processed! Check out the tabs below! 👇")
                
                # Demo content
                st.session_state.processed_content = {
                    'cleaned_text': "This is a sample text about friendship and kindness. Friends help each other and show empathy. Being a good friend means listening and caring about others' feelings. When we are kind to others, it makes everyone feel happy and valued.",
                    'sentiment': {
                        'sentiment': 'POSITIVE',
                        'confidence': {
                            'Positive': 0.85,
                            'Neutral': 0.10,
                            'Negative': 0.05
                        }
                    }
                }
        
        # Display processed content
        if st.session_state.processed_content:
            display_processed_content()
        
        # Logout button at the bottom
        st.markdown("<br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1.5, 2, 1.5])
        with col2:
            if st.button("🚪 Logout", use_container_width=True, key="student_logout_btn"):
                # Reset to initial state
                st.session_state.user_type = None
                st.session_state.student_id = None
                st.session_state.grade_level = 1
                st.session_state.processed_content = None
                st.session_state.conversation_history = []
                st.session_state.current_story = None
                st.session_state.regenerate_count = 0
                st.session_state.quiz = None
                st.rerun()

def process_with_aws(uploaded_file):
    """Process document with real AWS services"""
    
    # Step 1: Upload to S3
    with st.spinner("📤 Step 1/4: Uploading to AWS S3..."):
        file_key = upload_to_s3(uploaded_file, st.session_state.student_id)
        if not file_key:
            st.error("Failed to upload file")
            return
        st.success(f"✅ Uploaded to S3")
        time_module.sleep(1)
    
    # Step 2: Extract text with Textract
    with st.spinner("🔍 Step 2/4: Extracting text with AWS Textract..."):
        extracted_text = extract_text_from_s3(file_key)
        if not extracted_text:
            st.error("Failed to extract text")
            return
        st.success(f"✅ Extracted {len(extracted_text)} characters")
        st.session_state.extracted_text = extracted_text
        time_module.sleep(1)
    
    # Step 3: Start content generation
    with st.spinner("🤖 Step 3/4: Starting AI content generation..."):
        job_data = start_content_generation(
            extracted_text,
            st.session_state.grade_level,
            story_theme="friendship",
            quiz_type="multiple_choice"
        )
        
        if not job_data:
            st.error("Failed to start generation")
            return
        
        job_id = job_data['job_id']
        st.success(f"✅ Generation started! Job ID: {job_id}")
        time_module.sleep(1)
    
    # Step 4: Poll for completion
    st.markdown("### ⏳ Step 4/4: Generating Content with AWS Bedrock...")
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    start_time = time_module.time()
    max_wait = 90
    
    for i in range(max_wait // 2):
        status_data = check_job_status(job_id)
        
        if status_data:
            story_status = status_data.get('story_status', 'pending')
            quiz_status = status_data.get('quiz_status', 'pending')
            lesson_status = status_data.get('lesson_status', 'pending')
            
            completed = 0
            if story_status == 'completed': completed += 1
            if quiz_status == 'completed': completed += 1
            if lesson_status == 'completed': completed += 1
            
            progress = int((completed / 3) * 100)
            elapsed = int(time_module.time() - start_time)
            
            progress_bar.progress(progress)
            status_text.info(
                f"⏳ Generating... {completed}/3 complete ({elapsed}s)\n\n"
                f"📖 Story: {story_status}\n"
                f"❓ Quiz: {quiz_status}\n"
                f"📚 Lesson: {lesson_status}"
            )
            
            if status_data.get('status') == 'completed':
                st.balloons()
                st.success("✨ All content generated successfully!")
                st.session_state.aws_results = status_data
                st.session_state.processed_content = {
                    'cleaned_text': extracted_text,
                    'sentiment': {'sentiment': 'POSITIVE'},
                    'aws_data': status_data
                }
                time_module.sleep(1)
                st.rerun()
                return
        
        time_module.sleep(2)
    
    st.warning("⏰ Generation is taking longer than expected. Content may still be processing.")

def display_processed_content():
    content = st.session_state.processed_content
    
    # Fun tabs with emojis - Separate Stories and Quizzes
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📖 Read the Text", 
        "😊 Feel the Emotions", 
        "❓ Ask Questions", 
        "📚 Stories",
        "🎯 Quizzes"
    ])
    
    with tab1:
        st.markdown("### 📖 Here's What We Found!")
        st.markdown("*Read the text below - it's all about learning and growing!* 🌱")
        
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%); 
                        padding: 25px; border-radius: 15px; 
                        font-size: 1.1em; line-height: 1.7;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
                {content.get('cleaned_text', '')}
            </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 😊 How Does This Text Feel?")
        st.markdown("*Our AI detected these emotions in the text!* 🎭")
        
        sentiment = content.get('sentiment', {})
        
        # Big emoji display based on sentiment
        sentiment_emoji = {
            'POSITIVE': '😊',
            'NEGATIVE': '😢',
            'NEUTRAL': '😐',
            'MIXED': '🤔'
        }
        
        current_sentiment = sentiment.get('sentiment', 'NEUTRAL')
        st.markdown(f"""
            <div style='text-align: center; font-size: 5em; margin: 20px 0;'>
                {sentiment_emoji.get(current_sentiment, '😊')}
            </div>
            <div style='text-align: center; font-size: 1.5em; color: #667eea; font-weight: bold;'>
                This text feels {current_sentiment}!
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Confidence scores with different colors
        confidence = sentiment.get('confidence', {})
        if confidence:
            st.markdown("#### 🎨 Emotion Levels:")
            
            # Custom colored progress bars
            emoji_map = {'Positive': '😊', 'Neutral': '😐', 'Negative': '😢'}
            color_map = {
                'Positive': '#10b981',  # Green
                'Neutral': '#f59e0b',   # Orange
                'Negative': '#ef4444'   # Red
            }
            
            for emotion, score in confidence.items():
                st.markdown(f"**{emoji_map.get(emotion, '✨')} {emotion}**")
                
                # Create custom colored progress bar
                bar_color = color_map.get(emotion, '#667eea')
                percentage = int(score * 100)
                st.markdown(f"""
                    <div style='background-color: #e5e7eb; border-radius: 10px; height: 30px; 
                                margin: 10px 0 20px 0; overflow: hidden;'>
                        <div style='background: linear-gradient(90deg, {bar_color} 0%, {bar_color}dd 100%); 
                                    height: 100%; width: {percentage}%; 
                                    display: flex; align-items: center; justify-content: center;
                                    color: white; font-weight: 600; font-size: 0.95rem;
                                    transition: width 0.5s ease;'>
                            {percentage}%
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### ❓ Got Questions? Ask Away!")
        st.markdown("*I'm here to help you understand the text better!* 🤖✨")
        
        col1, col2 = st.columns([4, 1])
        
        with col1:
            question = st.text_input(
                "💭 What would you like to know?",
                placeholder="e.g., What is friendship? How can I be kind?",
                help="Type any question about the text!",
                key="question_input"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🎤 Voice", help="Click to ask by voice", use_container_width=True):
                st.info("🎤 Voice input will be available in full version with AWS Transcribe!")
        
        if st.button("🔍 Get My Answer!", use_container_width=True) and question:
            with st.spinner("🤔 Thinking..."):
                import time
                time.sleep(1)
            
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                            padding: 25px; border-radius: 15px; margin-top: 20px;
                            box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
                    <div style='font-size: 1.3em; color: #2d3748; font-weight: bold; margin-bottom: 12px;'>
                        🤖 Here's what I think:
                    </div>
                    <div style='font-size: 1.1em; line-height: 1.7; color: #2d3748;'>
                        Friendship is about caring for others, showing empathy, and being there when someone needs help. 
                        It means listening to your friends and making them feel valued! 💙
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.balloons()
    
    with tab4:
        st.markdown("### 📚 Story Time!")
        if st.session_state.use_aws and st.session_state.aws_results:
            st.markdown("*AI-generated story from your PDF using AWS Bedrock!* ✨📖")
        else:
            st.markdown("*Here's an amazing story just for you!* ✨📖")
        
        # Check if we have AWS results
        if st.session_state.use_aws and st.session_state.aws_results:
            results = st.session_state.aws_results.get('results', {})
            story_result = results.get('story', {})
            
            if story_result.get('status') == 'completed':
                story_data = story_result.get('result', {})
                
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
                                padding: 25px; border-radius: 20px; 
                                box-shadow: 0 8px 32px rgba(0,0,0,0.1); margin-bottom: 20px;'>
                        <div style='text-align: center; font-size: 1.8em; color: #667eea; 
                                    font-weight: bold; margin-bottom: 15px;'>
                            {story_data.get('title', 'Your Story')}
                        </div>
                        <div style='font-size: 1.1em; line-height: 1.8; color: #333; white-space: pre-line;'>
                            {story_data.get('story', '')}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                if story_data.get('reflection_question'):
                    st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                                    padding: 20px; border-radius: 15px; margin: 20px 0;'>
                            <div style='font-size: 1.2em; color: #667eea; font-weight: bold; margin-bottom: 10px;'>
                                💭 Think About This:
                            </div>
                            <div style='font-size: 1.05em; color: #333; line-height: 1.6;'>
                                {story_data.get('reflection_question', '')}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Story is still generating...")
        # Auto-generate demo story if not exists
        elif 'current_story' not in st.session_state or st.session_state.current_story is None:
            st.session_state.current_story = {
                'source': 'claude',
                'story': {
                    'title': '🌟 The Helpful Friend 🌟',
                    'story': 'Once upon a time, there was a kind student named Alex who always helped others. One day, Alex noticed a classmate sitting alone looking sad. 😢\n\nAlex went over and asked, "Hey, are you okay?" The classmate shared that they were having trouble with homework and felt frustrated. 📚\n\nAlex smiled and said, "Don\'t worry! Let\'s work on it together!" They sat down and Alex patiently explained the problems. Soon, both friends were smiling and laughing! 😊\n\nAlex learned that helping others makes everyone feel good. The classmate felt happy and grateful, and Alex felt proud of being a good friend! 💙',
                    'reflection_question': '💭 How do you think Alex felt after helping their classmate? Have you ever helped someone and felt good about it?',
                    'grade_level': st.session_state.grade_level
                },
                'story_hash': 'demo123',
                'regenerate_count': 0
            }
        
        # Display story with fun styling
        if st.session_state.current_story:
            story_data = st.session_state.current_story
            story = story_data['story']
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
                            padding: 25px; border-radius: 20px; 
                            box-shadow: 0 8px 32px rgba(0,0,0,0.1);'>
                    <div style='text-align: center; font-size: 1.8em; color: #667eea; 
                                font-weight: bold; margin-bottom: 15px;'>
                        {story.get('title', 'Your Story')}
                    </div>
                    <div style='font-size: 1.1em; line-height: 1.8; color: #333; 
                                white-space: pre-line;'>
                        {story.get('story', '')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Reflection question in a special box
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                            padding: 20px; border-radius: 15px; margin: 20px 0;
                            box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
                    <div style='font-size: 1.2em; color: #667eea; font-weight: bold; margin-bottom: 10px;'>
                        💭 Think About This:
                    </div>
                    <div style='font-size: 1.05em; color: #333; line-height: 1.6;'>
                        {story.get('reflection_question', '')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Feedback with fun buttons
            st.markdown("#### 🎭 Did you like this story?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 Love it!", use_container_width=True):
                    st.balloons()
                    st.success("🎉 Awesome! I'm so glad you enjoyed it!")
            
            with col2:
                if st.button("👎 Not really...", use_container_width=True):
                    st.session_state.regenerate_count += 1
                    
                    if st.session_state.regenerate_count >= 2:
                        st.info("🌐 In the full version, I'll search the web for more stories just for you!")
                    else:
                        st.info("✨ In the full version, I'll create a completely different story!")
        
    
    with tab5:
        # Display quiz directly without button
        display_quiz_with_tabs()

def display_quiz_with_tabs():
    """Display quiz with separate tabs for each question type"""
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
                    padding: 25px; border-radius: 20px; text-align: center;
                    box-shadow: 0 8px 32px rgba(0,0,0,0.1); margin-bottom: 30px;'>
            <div style='font-size: 2em; color: #2d3748; font-weight: bold;'>
                🎯 Understanding Friendship Quiz
            </div>
            <div style='font-size: 1.2em; color: #2d3748; margin-top: 10px;'>
                Complete each section and submit to see your score! ⭐
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for scores
    if 'mcq_score' not in st.session_state:
        st.session_state.mcq_score = None
    if 'fill_score' not in st.session_state:
        st.session_state.fill_score = None
    if 'tf_score' not in st.session_state:
        st.session_state.tf_score = None
    if 'match_score' not in st.session_state:
        st.session_state.match_score = None
    
    # Create tabs for each question type
    quiz_tab1, quiz_tab2, quiz_tab3, quiz_tab4 = st.tabs([
        "📝 MCQ ",
        "✍️ Fill in the Blanks ",
        "✓ True/False ",
        "🔗 Match the Pair "
    ])
    
    # Tab 1: MCQ
    with quiz_tab1:
        st.markdown("### 📝 Multiple Choice Questions")
        st.markdown("*Choose the best answer for each question*")
        st.markdown("<br>", unsafe_allow_html=True)
        
        mcq_questions = [
            {"q": "What did Alex do when they saw their classmate looking sad?", "options": ["Ignored them", "Asked if they were okay", "Laughed at them", "Walked away"], "correct": 1},
            {"q": "What makes a good friend?", "options": ["Being selfish", "Listening and caring", "Ignoring others", "Only thinking about yourself"], "correct": 1},
            {"q": "How should you respond when a friend needs help?", "options": ["Walk away", "Make fun of them", "Offer to help", "Tell them to figure it out"], "correct": 2},
            {"q": "What emotion do people feel when they help others?", "options": ["Angry", "Sad", "Happy and proud", "Bored"], "correct": 2},
            {"q": "What is empathy?", "options": ["Not caring about others", "Understanding others' feelings", "Being mean", "Ignoring people"], "correct": 1}
        ]
        
        mcq_answers = []
        for i, q in enumerate(mcq_questions):
            st.markdown(f"**Question {i+1}:** {q['q']}")
            answer = st.radio("Select your answer:", q['options'], key=f"mcq_{i}", label_visibility="collapsed", horizontal=True)
            mcq_answers.append(q['options'].index(answer) if answer else None)
            st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Submit MCQ Section", use_container_width=True, key="submit_mcq"):
                correct = sum(1 for i, q in enumerate(mcq_questions) if mcq_answers[i] == q['correct'])
                st.session_state.mcq_score = correct
        
        if st.session_state.mcq_score is not None:
            st.success(f"✅ You have completed the MCQ section!")
            st.info(f"**Your Score: {st.session_state.mcq_score} correct out of 5**")
            st.markdown("👉 *Proceed to the next tab: Fill in the Blanks*")
    
    # Tab 2: Fill in the Blanks
    with quiz_tab2:
        st.markdown("### ✍️ Fill in the Blanks")
        st.markdown("*Complete each sentence with the correct word*")
        st.markdown("<br>", unsafe_allow_html=True)
        
        fill_questions = [
            {"q": "Being a good friend means _______ to others.", "correct": "listening"},
            {"q": "When someone is sad, we should show _______.", "correct": "empathy"},
            {"q": "Helping others makes everyone feel _______.", "correct": "happy"},
            {"q": "A true friend is always _______ when you need them.", "correct": "there"},
            {"q": "Showing _______ means caring about others' feelings.", "correct": "kindness"}
        ]
        
        fill_answers = []
        for i, q in enumerate(fill_questions):
            st.markdown(f"**Question {i+1}:** {q['q']}")
            answer = st.text_input(f"Your answer:", key=f"fill_{i}", placeholder="Type your answer here...", label_visibility="collapsed")
            fill_answers.append(answer.lower().strip())
            st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Submit Fill in the Blanks", use_container_width=True, key="submit_fill"):
                correct = sum(1 for i, q in enumerate(fill_questions) if fill_answers[i] == q['correct'])
                st.session_state.fill_score = correct
        
        if st.session_state.fill_score is not None:
            st.success(f"✅ You have completed the Fill in the Blanks section!")
            st.info(f"**Your Score: {st.session_state.fill_score} correct out of 5**")
            st.markdown("👉 *Proceed to the next tab: True/False*")
    
    # Tab 3: True/False
    with quiz_tab3:
        st.markdown("### ✓ True or False")
        st.markdown("*Decide if each statement is True or False*")
        st.markdown("<br>", unsafe_allow_html=True)
        
        tf_questions = [
            {"q": "Helping others makes everyone feel good.", "correct": "True"},
            {"q": "Good friends ignore each other when someone is sad.", "correct": "False"},
            {"q": "Empathy means understanding how others feel.", "correct": "True"},
            {"q": "It's okay to laugh at someone who needs help.", "correct": "False"},
            {"q": "Being kind makes friendships stronger.", "correct": "True"}
        ]
        
        tf_answers = []
        for i, q in enumerate(tf_questions):
            st.markdown(f"**Statement {i+1}:** {q['q']}")
            answer = st.radio("Select your answer:", ["True", "False"], key=f"tf_{i}", label_visibility="collapsed", horizontal=True)
            tf_answers.append(answer)
            st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Submit True/False Section", use_container_width=True, key="submit_tf"):
                correct = sum(1 for i, q in enumerate(tf_questions) if tf_answers[i] == q['correct'])
                st.session_state.tf_score = correct
        
        if st.session_state.tf_score is not None:
            st.success(f"✅ You have completed the True/False section!")
            st.info(f"**Your Score: {st.session_state.tf_score} correct out of 5**")
            st.markdown("👉 *Proceed to the next tab: Match the Pair*")
    
    # Tab 4: Match the Pair
    with quiz_tab4:
        st.markdown("### 🔗 Match the Pair")
        st.markdown("*Match each emotion with the correct situation*")
        st.markdown("<br>", unsafe_allow_html=True)
        
        match_pairs = [
            {"left": "Happy 😊", "right": "When friends help each other", "correct": "When friends help each other"},
            {"left": "Sad 😢", "right": "When someone feels alone", "correct": "When someone feels alone"},
            {"left": "Proud 🌟", "right": "When you help someone successfully", "correct": "When you help someone successfully"},
            {"left": "Grateful 🙏", "right": "When someone helps you", "correct": "When someone helps you"},
            {"left": "Excited 🎉", "right": "When making new friends", "correct": "When making new friends"}
        ]
        
        all_options = [p["right"] for p in match_pairs]
        match_answers = []
        
        for i, pair in enumerate(match_pairs):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"**{pair['left']}**")
            with col2:
                answer = st.selectbox(f"Match with:", all_options, key=f"match_{i}", label_visibility="collapsed")
                match_answers.append(answer)
            st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Submit Match the Pair", use_container_width=True, key="submit_match"):
                correct = sum(1 for i, pair in enumerate(match_pairs) if match_answers[i] == pair['correct'])
                st.session_state.match_score = correct
        
        if st.session_state.match_score is not None:
            st.success(f"✅ You have completed the Match the Pair section!")
            st.info(f"**Your Score: {st.session_state.match_score} correct out of 5**")
            st.markdown("🎉 *Great job! You've completed all quiz sections!*")

def teacher_interface():
    # Initialize teacher_id in session state if not exists
    if 'teacher_id' not in st.session_state:
        st.session_state.teacher_id = None
    
    # Teacher ID input in main area
    if not st.session_state.teacher_id:
        st.markdown("""
            <div style='text-align: center; color: white; font-size: 2em; 
                        text-shadow: 2px 2px 4px rgba(0,0,0,0.3); 
                        margin: 30px 0 40px 0;
                        font-weight: 700;'>
                👩‍🏫 Teacher Portal - Login
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1.5, 2, 1.5])
        with col2:
            teacher_id_input = st.text_input("Teacher ID", placeholder="e.g., teacher456", key="teacher_id_input")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🚀 Start Teaching", use_container_width=True, key="start_teaching_btn"):
                if teacher_id_input:
                    st.session_state.teacher_id = teacher_id_input
                    st.rerun()
                else:
                    st.error("Please enter a Teacher ID")
            
            if st.button("⬅️ Back to Main Menu", use_container_width=True, key="teacher_back_btn"):
                st.session_state.user_type = None
                st.rerun()
    else:
        # Show teacher info in header
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                            padding: 15px; border-radius: 15px; text-align: center; 
                            color: white; font-size: 1.1em; margin-bottom: 20px;'>
                    👩‍🏫 <strong>Teacher:</strong> {st.session_state.teacher_id}
                </div>
            """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["📝 Lesson Planner", "📊 Student Analytics"])
        
        with tab1:
            st.header("Auto-Generate Lesson Plans")
            
            uploaded_file = st.file_uploader(
                "Upload content for lesson plan",
                type=['pdf', 'png', 'jpg', 'jpeg']
            )
            
            col1, col2 = st.columns(2)
            with col1:
                grade_level = st.selectbox("Grade Level", range(1, 11))
            with col2:
                duration = st.selectbox("Duration (minutes)", [30, 45, 60])
            
            # Center the Generate Lesson Plan button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                generate_button = st.button("Generate Lesson Plan", use_container_width=True)
            
            if generate_button:
                # Auto-scroll to top of generated content
                st.markdown('<div id="lesson-plan-top"></div>', unsafe_allow_html=True)
                
                # JavaScript to scroll to top
                st.markdown("""
                    <script>
                        window.scrollTo({top: 0, behavior: 'smooth'});
                    </script>
                """, unsafe_allow_html=True)
                
                st.success("✅ Lesson plan generated successfully!")
                st.info("📋 Showing demo lesson plan below...")
                
                # Demo lesson plan with dynamic duration
                # Calculate phase durations based on total duration - rounded to 5 minute intervals
                def round_to_5(value):
                    return max(5, round(value / 5) * 5)
                
                warmup_time = round_to_5(duration * 0.20)  # 20% of total
                main_time = round_to_5(duration * 0.45)    # 45% of total
                extension_time = round_to_5(duration * 0.25)  # 25% of total
                assessment_time = max(5, duration - warmup_time - main_time - extension_time)  # Remaining time
                
                lesson_plan = {
                    'lesson_title': 'Understanding Emotions and Empathy',
                    'grade_level': grade_level,
                    'duration_minutes': duration,
                    'learning_objectives': [
                        'Students will identify different emotions',
                        'Students will practice empathy skills',
                        'Students will understand how to help others'
                    ],
                    'sel_competencies': ['Self-awareness', 'Social awareness', 'Relationship skills'],
                    'phases': {
                        'warmup': {
                            'duration_minutes': warmup_time,
                            'activities': ['Emotion charades game', 'Share how you feel today']
                        },
                        'main_activity': {
                            'duration_minutes': main_time,
                            'activities': ['Read story about friendship', 'Discuss characters\' feelings', 'Role-play scenarios']
                        },
                        'extension': {
                            'duration_minutes': extension_time,
                            'activities': ['Create emotion cards', 'Write about a time you helped someone']
                        },
                        'assessment': {
                            'duration_minutes': assessment_time,
                            'methods': ['Exit ticket: Name 3 emotions', 'Share one way to show empathy']
                        }
                    }
                }
                
                display_lesson_plan(lesson_plan)
        
        with tab2:
            st.header("Student Analytics Dashboard")
            
            student_id = st.text_input("Enter Student ID to view analytics", placeholder="e.g., student123")
            
            # Center the Load Analytics button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                load_button = st.button("Load Analytics", use_container_width=True)
            
            if student_id and load_button:
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                padding: 30px; border-radius: 20px; text-align: center;
                                color: white; margin-bottom: 30px; margin-top: 20px;'>
                        <div style='font-size: 2.5em; font-weight: bold;'>
                            📊 Student Analytics Dashboard
                        </div>
                        <div style='font-size: 1.3em; margin-top: 10px;'>
                            Student: {student_id}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Metrics in cards - All same size
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("""
                        <div style='background: white; padding: 25px; border-radius: 15px; 
                                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center;
                                    min-height: 180px; display: flex; flex-direction: column; 
                                    justify-content: center;'>
                            <div style='font-size: 3em; margin-bottom: 10px;'>📚</div>
                            <div style='font-size: 2.5em; color: #667eea; font-weight: bold; margin-bottom: 10px;'>12</div>
                            <div style='font-size: 1.2em; color: #2d3748;'>Total Assessments</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                        <div style='background: white; padding: 25px; border-radius: 15px; 
                                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center;
                                    min-height: 180px; display: flex; flex-direction: column; 
                                    justify-content: center;'>
                            <div style='font-size: 3em; margin-bottom: 10px;'>⭐</div>
                            <div style='font-size: 2.5em; color: #667eea; font-weight: bold; margin-bottom: 10px;'>85%</div>
                            <div style='font-size: 1.2em; color: #2d3748;'>Average Score</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown("""
                        <div style='background: white; padding: 25px; border-radius: 15px; 
                                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center;
                                    min-height: 180px; display: flex; flex-direction: column; 
                                    justify-content: center;'>
                            <div style='font-size: 3em; margin-bottom: 10px;'>😊</div>
                            <div style='font-size: 2.5em; color: #667eea; font-weight: bold; margin-bottom: 10px;'>POSITIVE</div>
                            <div style='font-size: 1.2em; color: #2d3748;'>Recent Sentiment</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br><br>", unsafe_allow_html=True)
                
                # Detailed metrics
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 📈 Performance Trends")
                    st.markdown("""
                        <div style='background: white; padding: 20px; border-radius: 15px; 
                                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
                            <div style='font-size: 1.2em; color: #2d3748; margin: 10px 0;'>
                                ✓ Completed 12 quizzes<br>
                                ✓ Read 8 stories<br>
                                ✓ Asked 24 questions<br>
                                ✓ Engagement: <strong style='color: #667eea;'>High</strong>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("### 💭 Emotional Journey")
                    st.markdown("""
                        <div style='background: white; padding: 20px; border-radius: 15px; 
                                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
                            <div style='font-size: 1.2em; color: #2d3748; margin: 10px 0;'>
                                ✓ 15 emotional check-ins<br>
                                ✓ Emotional growth: <strong style='color: #667eea;'>+12%</strong><br>
                                ✓ Most common: <strong style='color: #667eea;'>Happy 😊</strong><br>
                                ✓ Progress: <strong style='color: #667eea;'>Excellent</strong>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
        
        # Logout button at the bottom
        st.markdown("<br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1.5, 2, 1.5])
        with col2:
            if st.button("🚪 Logout", use_container_width=True, key="teacher_logout_btn"):
                st.session_state.user_type = None
                st.session_state.teacher_id = None
                st.rerun()

def display_lesson_plan(plan):
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 30px; border-radius: 20px; text-align: center;
                    color: white; margin-bottom: 30px;'>
            <div style='font-size: 2.5em; font-weight: bold;'>
                📚 {plan.get('lesson_title', 'Lesson Plan')}
            </div>
            <div style='font-size: 1.3em; margin-top: 10px;'>
                Grade {plan.get('grade_level')} | {plan.get('duration_minutes')} minutes
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Download button
    lesson_text = f"""
LESSON PLAN: {plan.get('lesson_title', 'Lesson Plan')}
Grade Level: {plan.get('grade_level')}
Duration: {plan.get('duration_minutes')} minutes

LEARNING OBJECTIVES:
{chr(10).join('- ' + obj for obj in plan.get('learning_objectives', []))}

SEL COMPETENCIES:
{', '.join(plan.get('sel_competencies', []))}

WARM-UP PHASE ({plan.get('phases', {}).get('warmup', {}).get('duration_minutes', 0)} minutes):
{chr(10).join('- ' + act for act in plan.get('phases', {}).get('warmup', {}).get('activities', []))}

MAIN ACTIVITY ({plan.get('phases', {}).get('main_activity', {}).get('duration_minutes', 0)} minutes):
{chr(10).join('- ' + act for act in plan.get('phases', {}).get('main_activity', {}).get('activities', []))}

EXTENSION ({plan.get('phases', {}).get('extension', {}).get('duration_minutes', 0)} minutes):
{chr(10).join('- ' + act for act in plan.get('phases', {}).get('extension', {}).get('activities', []))}

ASSESSMENT ({plan.get('phases', {}).get('assessment', {}).get('duration_minutes', 0)} minutes):
{chr(10).join('- ' + method for method in plan.get('phases', {}).get('assessment', {}).get('methods', []))}
"""
    
    st.download_button(
        label="📥 Download Lesson Plan",
        data=lesson_text,
        file_name=f"lesson_plan_{plan.get('lesson_title', 'plan').replace(' ', '_')}.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display lesson plan details
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🎯 Learning Objectives")
        for obj in plan.get('learning_objectives', []):
            st.markdown(f"✓ {obj}")
    
    with col2:
        st.markdown("### 💡 SEL Competencies")
        for comp in plan.get('sel_competencies', []):
            st.markdown(f"⭐ {comp}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    phases = plan.get('phases', {})
    
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    
    # Warm-up Phase - Simple card layout
    warmup = phases.get('warmup', {})
    st.markdown("""
        <div style='background: rgba(255, 107, 107, 0.1); padding: 20px; border-radius: 12px; margin: 15px 0; border-left: 5px solid #ff6b6b;'>
            <h3 style='color: #ff6b6b; margin: 0 0 15px 0;'>🔥 Warm-up Phase</h3>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(f"**Duration:** {warmup.get('duration_minutes')} minutes")
    st.markdown("**Activities:**")
    for activity in warmup.get('activities', []):
        st.markdown(f"• {activity}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main Activity - Simple card layout
    main = phases.get('main_activity', {})
    st.markdown("""
        <div style='background: rgba(102, 126, 234, 0.1); padding: 20px; border-radius: 12px; margin: 15px 0; border-left: 5px solid #667eea;'>
            <h3 style='color: #667eea; margin: 0 0 15px 0;'>📚 Main Activity</h3>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(f"**Duration:** {main.get('duration_minutes')} minutes")
    st.markdown("**Activities:**")
    for activity in main.get('activities', []):
        st.markdown(f"• {activity}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Extension - Simple card layout
    ext = phases.get('extension', {})
    st.markdown("""
        <div style='background: rgba(245, 158, 11, 0.1); padding: 20px; border-radius: 12px; margin: 15px 0; border-left: 5px solid #f59e0b;'>
            <h3 style='color: #f59e0b; margin: 0 0 15px 0;'>🚀 Extension</h3>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(f"**Duration:** {ext.get('duration_minutes')} minutes")
    st.markdown("**Activities:**")
    for activity in ext.get('activities', []):
        st.markdown(f"• {activity}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Assessment - Simple card layout
    assess = phases.get('assessment', {})
    st.markdown("""
        <div style='background: rgba(16, 185, 129, 0.1); padding: 20px; border-radius: 12px; margin: 15px 0; border-left: 5px solid #10b981;'>
            <h3 style='color: #10b981; margin: 0 0 15px 0;'>✅ Assessment</h3>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(f"**Duration:** {assess.get('duration_minutes')} minutes")
    st.markdown("**Methods:**")
    for method in assess.get('methods', []):
        st.markdown(f"• {method}")

if __name__ == "__main__":
    main()
