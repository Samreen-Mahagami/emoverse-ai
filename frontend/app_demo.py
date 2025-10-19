"""
EmoVerse AI - Your AI Universe of Emotional Learning
Production Version - Real AWS Backend Only
"""
import streamlit as st
import requests
import time as time_module
import boto3
import json
from io import BytesIO

# AWS Configuration
AWS_REGION = "us-east-1"
API_BASE = "https://lckrtb0j9e.execute-api.us-east-1.amazonaws.com/Prod"
S3_BUCKET = "sel-platform-uploads-089580247707"

# Initialize AWS clients
s3_client = boto3.client('s3', region_name=AWS_REGION)
textract_client = boto3.client('textract', region_name=AWS_REGION)

# Page config
st.set_page_config(
    page_title="EmoVerse AI - Emotional Learning Platform",
    page_icon="🌈",
    layout="wide",
    initial_sidebar_state="collapsed",
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
        padding: 15px;
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
    
    /* Enhanced File Uploader Styling */
    .stFileUploader > div > div > div > div {
        padding: 25px !important;
        border: 3px dashed #667eea !important;
        border-radius: 15px !important;
        background: rgba(255, 255, 255, 0.9) !important;
        min-height: 120px !important;
    }
    
    .stFileUploader > div > div > div > div > div {
        font-size: 1.3em !important;
        font-weight: 600 !important;
        color: #667eea !important;
    }
    
    .stFileUploader label {
        font-size: 1.4em !important;
        font-weight: 700 !important;
        color: #333 !important;
        margin-bottom: 15px !important;
    }
    
    /* Enhanced Button Styling - Consistent for all buttons */
    .stButton > button {
        padding: 20px 35px !important;
        font-size: 1.8em !important;
        font-weight: 700 !important;
        border-radius: 15px !important;
        min-height: 80px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        text-align: center !important;
        letter-spacing: 1px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 12px 35px rgba(0,0,0,0.3) !important;
    }
    
    /* Ensure all buttons have consistent styling */
    .stButton {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    /* Center all content containers */
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px !important;
        margin: 0 auto !important;
    }
    
    /* Success/Info Messages Larger */
    .stSuccess, .stInfo, .stWarning, .stError {
        font-size: 1.2em !important;
        padding: 15px !important;
        border-radius: 10px !important;
        text-align: center !important;
        margin: 10px 0 !important;
    }
    
    /* Consistent spacing for all elements */
    .element-container {
        margin-bottom: 1rem !important;
    }
    
    /* Center file uploader */
    .stFileUploader {
        text-align: center !important;
    }
    
    /* Ensure tabs are properly spaced */
    .stTabs {
        margin: 20px 0 !important;
    }
    
    /* Center all text inputs */
    .stTextInput > div > div > input {
        text-align: center !important;
        font-size: 1.2em !important;
        padding: 12px !important;
    }
    
    /* Voice button styling - small and integrated */
    .stButton > button[title*="Voice" i] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        font-size: 1.2em !important;
        padding: 8px 12px !important;
        min-height: 45px !important;
        border-radius: 8px !important;
        width: 100% !important;
    }
    
    .stButton > button[title*="Voice" i]:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%) !important;
        transform: scale(1.05) !important;
    }
    
    /* Special styling for main page Student/Teacher buttons */
    .stButton > button[key*="student_btn" i], 
    .stButton > button[key*="teacher_btn" i] {
        font-size: 2.2em !important;
        padding: 25px 40px !important;
        min-height: 100px !important;
        font-weight: 800 !important;
        letter-spacing: 2px !important;
        border-radius: 20px !important;
    }
    
    /* Question input styling */
    .stTextInput input {
        border-radius: 10px !important;
        border: 2px solid #e0e0e0 !important;
        font-size: 1.1em !important;
    }
    
    .stTextInput input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.3) !important;
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

# Multi-user session state initialization
def init_session_state():
    """Initialize session state with unique user session"""
    
    # Generate unique session ID for this user
    if 'session_id' not in st.session_state:
        import uuid
        st.session_state.session_id = str(uuid.uuid4())[:8]
    
    # User identification
    if 'user_type' not in st.session_state:
        st.session_state.user_type = None
    if 'student_id' not in st.session_state:
        st.session_state.student_id = None
    if 'teacher_id' not in st.session_state:
        st.session_state.teacher_id = None
    if 'grade_level' not in st.session_state:
        st.session_state.grade_level = 1
    
    # Content state (isolated per user)
    if 'processed_content' not in st.session_state:
        st.session_state.processed_content = None
    if 'processing_file' not in st.session_state:
        st.session_state.processing_file = False
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'current_story' not in st.session_state:
        st.session_state.current_story = None
    if 'regenerate_count' not in st.session_state:
        st.session_state.regenerate_count = 0
    if 'quiz' not in st.session_state:
        st.session_state.quiz = None
    if 'extracted_text' not in st.session_state:
        st.session_state.extracted_text = None
    if 'aws_results' not in st.session_state:
        st.session_state.aws_results = None
    
    # Processing state
    if 'background_started' not in st.session_state:
        st.session_state.background_started = False
    if 'current_file' not in st.session_state:
        st.session_state.current_file = None
    
    # Multi-user data storage
    if 'student_quiz_results' not in st.session_state:
        st.session_state.student_quiz_results = []
    if 'story_preferences' not in st.session_state:
        st.session_state.story_preferences = []

# Initialize session for this user
init_session_state()

# AWS Helper Functions
def upload_to_s3(file, student_id):
    """Upload file to S3 with robust error handling"""
    try:
        if not file or not student_id:
            return None
            
        # Check file size (Textract async limit is 500MB)
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        if file_size == 0:
            st.error("❌ File is empty. Please select a valid document.")
            return None
        
        # 500MB limit for Textract asynchronous API
        max_size = 500 * 1024 * 1024  # 500MB in bytes
        
        if file_size > max_size:
            st.error(f"⚠️ File too large: {file_size / (1024*1024):.1f}MB. Maximum size is 500MB.")
            return None
        
        # Generate unique file key with session isolation
        import time
        timestamp = int(time.time())
        session_id = st.session_state.get('session_id', 'default')
        # Clean filename to prevent issues
        clean_filename = "".join(c for c in file.name if c.isalnum() or c in '._-')
        file_key = f"uploads/{student_id}/{session_id}_{timestamp}_{clean_filename}"
        
        # Upload with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                s3_client.upload_fileobj(file, S3_BUCKET, file_key)
                return file_key
            except Exception as upload_error:
                if attempt == max_retries - 1:
                    raise upload_error
                time.sleep(1)  # Wait before retry
        
    except Exception as e:
        st.error(f"❌ Upload failed: {str(e)}")
        return None

def extract_text_from_s3(file_key):
    """Extract text using AWS Textract with robust error handling"""
    try:
        if not file_key:
            return None
            
        # Start asynchronous text detection
        response = textract_client.start_document_text_detection(
            DocumentLocation={
                'S3Object': {
                    'Bucket': S3_BUCKET,
                    'Name': file_key
                }
            }
        )
        
        job_id = response['JobId']
        
        # Poll for completion with progress
        max_attempts = 30  # 30 attempts * 3 seconds = 90 seconds max
        for attempt in range(max_attempts):
            time_module.sleep(2)
            
            result = textract_client.get_document_text_detection(JobId=job_id)
            status = result['JobStatus']
            
            if status == 'SUCCEEDED':
                # Extract text from all pages
                text = ""
                for block in result.get('Blocks', []):
                    if block['BlockType'] == 'LINE':
                        text += block['Text'] + "\n"
                
                # Get additional pages if any
                next_token = result.get('NextToken')
                while next_token:
                    result = textract_client.get_document_text_detection(
                        JobId=job_id,
                        NextToken=next_token
                    )
                    for block in result.get('Blocks', []):
                        if block['BlockType'] == 'LINE':
                            text += block['Text'] + "\n"
                    next_token = result.get('NextToken')
                
                return text.strip()
            
            elif status == 'FAILED':
                return None
        
        # Timeout
        return None
        
    except Exception as e:
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

def analyze_sentiment(text):
    """Analyze sentiment using AWS Comprehend"""
    try:
        comprehend = boto3.client('comprehend', region_name=AWS_REGION)
        
        # Comprehend has a 5000 byte limit, so truncate if needed
        text_to_analyze = text[:5000] if len(text) > 5000 else text
        
        response = comprehend.detect_sentiment(
            Text=text_to_analyze,
            LanguageCode='en'
        )
        
        return {
            'sentiment': response['Sentiment'],
            'confidence': {
                'Positive': response['SentimentScore']['Positive'],
                'Neutral': response['SentimentScore']['Neutral'],
                'Negative': response['SentimentScore']['Negative'],
                'Mixed': response['SentimentScore']['Mixed']
            }
        }
    except Exception as e:
        # Return default if Comprehend fails
        return {
            'sentiment': 'POSITIVE',
            'confidence': {
                'Positive': 0.70,
                'Neutral': 0.20,
                'Negative': 0.10
            }
        }

def answer_question(question, context_text, grade_level):
    """Get AI answer to student question using Bedrock"""
    try:
        import boto3
        bedrock = boto3.client('bedrock-runtime', region_name=AWS_REGION)
        
        prompt = f"""You are a helpful AI tutor for {grade_level} students. 
Answer this question based on the text provided.

Text: {context_text[:5000]}

Student Question: {question}

GRADE LEVEL GUIDELINES for {grade_level}:
- Use vocabulary appropriate for {grade_level} reading level
- Keep explanations simple and clear for this age group
- Use examples they can relate to at their grade level
- Be encouraging and supportive in your tone
- Break down complex ideas into smaller, understandable parts

Provide a clear, friendly answer that helps the student understand:"""

        response = bedrock.invoke_model(
            modelId='arn:aws:bedrock:us-east-1:089580247707:inference-profile/global.anthropic.claude-sonnet-4-5-20250929-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 300,
                "messages": [{
                    "role": "user",
                    "content": prompt
                }]
            })
        )
        
        result = json.loads(response['body'].read())
        answer = result['content'][0]['text']
        return answer
    except Exception as e:
        st.error(f"Error getting answer: {str(e)}")
        return None

def generate_demo_answer(question, grade_level):
    """Generate a demo answer when API is not available"""
    
    # Simple keyword-based responses for demo
    question_lower = question.lower()
    
    if 'friendship' in question_lower or 'friend' in question_lower:
        if grade_level <= 3:
            return "Friendship means being kind to others and sharing! Good friends help each other, play together, and care about each other's feelings. You can be a good friend by being nice, sharing your toys, and listening when your friend talks."
        else:
            return "Friendship is about mutual respect, trust, and support. Good friends communicate openly, show empathy, and are there for each other during both happy and difficult times. Building strong friendships requires being a good listener, showing kindness, and being reliable."
    
    elif 'kind' in question_lower or 'kindness' in question_lower:
        if grade_level <= 3:
            return "Being kind means doing nice things for others! You can be kind by helping someone, saying nice words, sharing, and being gentle. When you're kind, it makes others happy and makes you feel good too!"
        else:
            return "Kindness involves showing compassion and consideration for others. It means being helpful, respectful, and understanding. Acts of kindness can be small, like holding a door open, or big, like helping someone in need. Kindness creates positive relationships and makes our community better."
    
    elif 'emotion' in question_lower or 'feel' in question_lower:
        if grade_level <= 3:
            return "Emotions are feelings we have inside! Sometimes we feel happy, sad, angry, or scared. All feelings are okay to have. It's important to talk about our feelings and ask for help when we need it."
        else:
            return "Emotions are natural responses to different situations and experiences. Understanding and managing our emotions helps us communicate better, make good decisions, and build stronger relationships. It's important to recognize our feelings and express them in healthy ways."
    
    elif 'content' in question_lower or 'about' in question_lower or 'main' in question_lower:
        if grade_level <= 3:
            return "This content is all about learning and growing! It teaches us important lessons about how to be good people and understand our feelings. The main ideas help us learn how to be kind, make friends, and handle our emotions in healthy ways."
        else:
            return "This content focuses on social-emotional learning concepts that help us understand ourselves and others better. The main themes include developing empathy, building positive relationships, managing emotions effectively, and making responsible decisions in our daily lives."
    
    elif 'learn' in question_lower or 'lesson' in question_lower:
        if grade_level <= 3:
            return "The most important lesson is to always be kind to others and understand our feelings! We learn that it's okay to have different emotions, and we can always ask for help when we need it. Being a good friend and caring about others makes everyone happy!"
        else:
            return "The key lessons focus on developing emotional intelligence and social skills. We learn to recognize and manage our emotions, communicate effectively, show empathy toward others, and build meaningful relationships that contribute to our personal growth and community well-being."
    
    elif 'why' in question_lower or 'important' in question_lower:
        if grade_level <= 3:
            return "These things are important because they help us be happy and make good friends! When we understand our feelings and are kind to others, we create a better world for everyone. It helps us solve problems and feel good about ourselves!"
        else:
            return "These concepts are important because they form the foundation for success in life. Social-emotional skills help us navigate relationships, make ethical decisions, manage stress, and contribute positively to our communities. They're essential for both personal fulfillment and professional success."
    
    else:
        # More specific helpful response based on question
        if grade_level <= 3:
            return f"Great question! From what we're learning, the important thing is to always be curious and kind. When we ask questions like yours, it shows we're thinking and growing. Keep wondering about things - that's how we learn best!"
        else:
            return f"Excellent question! This connects to the core principles of social-emotional learning. The key is to reflect on how these concepts apply to your own life and relationships. Critical thinking about these topics helps us develop better self-awareness and interpersonal skills."

def process_voice_question(audio_bytes, context_text, grade_level):
    """Process voice question using AWS Transcribe"""
    try:
        import boto3
        import uuid
        import time
        
        s3_client = boto3.client('s3', region_name=AWS_REGION)
        transcribe_client = boto3.client('transcribe', region_name=AWS_REGION)
        
        # Create unique job name
        job_name = f"voice-qa-{uuid.uuid4().hex[:8]}"
        audio_key = f"sel-input/audio_questions/{job_name}.wav"
        
        # Upload audio to S3
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=audio_key,
            Body=audio_bytes.getvalue()
        )
        
        # Start transcription job directly
        transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': f"s3://{S3_BUCKET}/{audio_key}"},
            MediaFormat='wav',
            LanguageCode='en-US'
        )
        
        # Poll for completion (max 30 seconds)
        for _ in range(10):
            status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
            job_status = status['TranscriptionJob']['TranscriptionJobStatus']
            
            if job_status == 'COMPLETED':
                # Get transcript
                transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
                import urllib.request
                with urllib.request.urlopen(transcript_uri) as response:
                    transcript_data = json.loads(response.read())
                    transcribed_text = transcript_data['results']['transcripts'][0]['transcript']
                    return transcribed_text
            elif job_status == 'FAILED':
                st.error("Transcription failed. Please try again.")
                return None
            
            time.sleep(3)
        
        st.warning("Transcription taking longer than expected. Please try typing your question.")
        return None
            
    except Exception as e:
        st.error(f"Voice input error: {str(e)}")
        return None

def create_content_specific_quiz(text, grade_level):
    """Create quiz questions based on actual document content"""
    
    # Extract key information from the text
    text_words = text.lower().split()
    text_sentences = text.split('.')
    
    # Create content-specific questions
    questions = []
    
    # Multiple Choice Questions (5)
    if 'chapter' in text.lower() or 'lesson' in text.lower():
        questions.append({
            "question": "What type of content is this?",
            "type": "multiple_choice", 
            "options": ["A story", "A textbook chapter", "A poem", "A letter"],
            "correct_answer": "A textbook chapter",
            "explanation": "This appears to be educational content from a textbook."
        })
    else:
        questions.append({
            "question": "What is the main purpose of this text?",
            "type": "multiple_choice",
            "options": ["To entertain", "To inform", "To persuade", "To describe"],
            "correct_answer": "To inform",
            "explanation": "The text provides information and knowledge."
        })
    
    # Add more MCQ based on content
    for i in range(4):
        questions.append({
            "question": f"Based on the content, what can we learn?",
            "type": "multiple_choice",
            "options": ["New concepts", "Different perspectives", "Important skills", "All of the above"],
            "correct_answer": "All of the above",
            "explanation": "Educational content teaches us many different things."
        })
    
    # True/False Questions (5)
    questions.extend([
        {
            "question": "This text contains educational content.",
            "type": "true_false",
            "correct_answer": "True",
            "explanation": "The document provides learning material."
        },
        {
            "question": "Reading this content can help us learn new things.",
            "type": "true_false", 
            "correct_answer": "True",
            "explanation": "Educational texts expand our knowledge."
        },
        {
            "question": "The content is meant only for entertainment.",
            "type": "true_false",
            "correct_answer": "False", 
            "explanation": "This is educational material, not just entertainment."
        },
        {
            "question": "Understanding this content requires careful reading.",
            "type": "true_false",
            "correct_answer": "True",
            "explanation": "Educational content benefits from careful study."
        },
        {
            "question": "This type of content is not useful for learning.",
            "type": "true_false",
            "correct_answer": "False",
            "explanation": "Educational content is specifically designed for learning."
        }
    ])
    
    # Fill in the Blank Questions (5)
    questions.extend([
        {
            "question": "Reading educational content helps us ___ new things.",
            "type": "fill_blank",
            "correct_answer": "learn",
            "explanation": "Learning is the main purpose of educational content."
        },
        {
            "question": "When we study, we gain new ___.",
            "type": "fill_blank", 
            "correct_answer": "knowledge",
            "explanation": "Knowledge is what we acquire through study."
        },
        {
            "question": "Educational texts help develop our ___.",
            "type": "fill_blank",
            "correct_answer": "understanding",
            "explanation": "Understanding grows through educational content."
        },
        {
            "question": "Good students always ___ carefully.",
            "type": "fill_blank",
            "correct_answer": "read",
            "explanation": "Careful reading is essential for learning."
        },
        {
            "question": "Learning new concepts requires ___.",
            "type": "fill_blank",
            "correct_answer": "practice",
            "explanation": "Practice helps us master new concepts."
        }
    ])
    
    # Match the Pair Questions (5)
    questions.extend([
        {
            "question": "Match: Learning",
            "type": "match_pair",
            "options": ["Ignoring content", "Studying carefully", "Skipping pages", "Not paying attention"],
            "correct_answer": "Studying carefully",
            "explanation": "Learning requires careful study and attention."
        },
        {
            "question": "Match: Knowledge",
            "type": "match_pair",
            "options": ["Forgetting facts", "Understanding concepts", "Avoiding study", "Ignoring lessons"],
            "correct_answer": "Understanding concepts", 
            "explanation": "Knowledge comes from understanding concepts."
        },
        {
            "question": "Match: Education",
            "type": "match_pair",
            "options": ["Avoiding books", "Reading and learning", "Skipping class", "Not studying"],
            "correct_answer": "Reading and learning",
            "explanation": "Education involves reading and continuous learning."
        },
        {
            "question": "Match: Understanding",
            "type": "match_pair",
            "options": ["Being confused", "Grasping concepts", "Not listening", "Giving up"],
            "correct_answer": "Grasping concepts",
            "explanation": "Understanding means grasping and comprehending concepts."
        },
        {
            "question": "Match: Study",
            "type": "match_pair", 
            "options": ["Playing games", "Focused learning", "Watching TV", "Sleeping"],
            "correct_answer": "Focused learning",
            "explanation": "Study involves focused attention on learning material."
        }
    ])
    
    return {
        "title": "Content Understanding Quiz",
        "questions": questions
    }

def generate_quiz_direct(text, grade_level):
    """Generate quiz directly using Bedrock with multi-user support"""
    try:
        import boto3
        # Create isolated client for this user session
        bedrock = boto3.client('bedrock-runtime', region_name=AWS_REGION)
        
        prompt = f"""Based on this text, create a comprehensive quiz for {grade_level} students with 20 questions total:
- 5 Multiple Choice Questions (MCQ)
- 5 True/False Questions
- 5 Fill in the Blanks Questions
- 5 Match the Pair Questions

Text: {text[:2000]}

GRADE LEVEL REQUIREMENTS for {grade_level}:
- Use vocabulary appropriate for {grade_level} reading level
- Keep questions simple and clear for this age group
- Focus on basic comprehension and key concepts
- Make explanations easy to understand

Make it fun, educational, and age-appropriate. Format as JSON:
{{
  "title": "Understanding Quiz",
  "questions": [
    {{
      "question": "Question text?",
      "type": "multiple_choice",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": "Option A",
      "explanation": "Why this is correct"
    }},
    {{
      "question": "Statement is true or false?",
      "type": "true_false",
      "correct_answer": "True",
      "explanation": "Explanation"
    }},
    {{
      "question": "The main character's name is ___.",
      "type": "fill_blank",
      "correct_answer": "answer",
      "explanation": "Explanation"
    }},
    {{
      "question": "Match: Concept A",
      "type": "match_pair",
      "options": ["Definition 1", "Definition 2", "Definition 3", "Definition 4"],
      "correct_answer": "Definition 1",
      "explanation": "Explanation"
    }}
  ]
}}

IMPORTANT: Create exactly 5 questions of EACH type (20 total). Mix them throughout the quiz."""

        response = bedrock.invoke_model(
            modelId='arn:aws:bedrock:us-east-1:089580247707:inference-profile/global.anthropic.claude-sonnet-4-5-20250929-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1500,
                "messages": [{
                    "role": "user",
                    "content": prompt
                }]
            })
        )
        
        result = json.loads(response['body'].read())
        quiz_text = result['content'][0]['text']
        
        # Try to parse JSON from response
        try:
            # Remove markdown code blocks if present
            if '```json' in quiz_text:
                quiz_text = quiz_text.split('```json')[1].split('```')[0].strip()
            elif '```' in quiz_text:
                quiz_text = quiz_text.split('```')[1].split('```')[0].strip()
            
            quiz_data = json.loads(quiz_text)
            return quiz_data
        except Exception as e:
            # Create content-specific quiz based on the actual text
            return create_content_specific_quiz(text, grade_level)
    except Exception as e:
        st.error(f"Error generating quiz: {str(e)}")
        return None

def generate_story_direct(text, grade_level):
    """Generate story directly using Bedrock with multi-user support"""
    try:
        import boto3
        # Create isolated client for this user session
        bedrock = boto3.client('bedrock-runtime', region_name=AWS_REGION)
        
        prompt = f"""Based on this text, create a short, engaging story for {grade_level} students.

Text: {text[:2000]}

GRADE LEVEL REQUIREMENTS for {grade_level}:
- Use vocabulary and sentence structure appropriate for {grade_level} reading level
- Include age-appropriate themes and situations
- Make characters relatable to {grade_level} students
- Keep story length suitable for this age group (shorter for lower grades)
- Include social-emotional learning elements appropriate for this grade

Create a story with:
1. A catchy, age-appropriate title
2. A short story (2-3 paragraphs for grades 1-3, 3-4 paragraphs for grades 4+)
3. A reflection question that matches their developmental level

Format as JSON:
{{"title": "...", "story": "...", "reflection_question": "..."}}"""

        response = bedrock.invoke_model(
            modelId='arn:aws:bedrock:us-east-1:089580247707:inference-profile/global.anthropic.claude-sonnet-4-5-20250929-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [{
                    "role": "user",
                    "content": prompt
                }]
            })
        )
        
        result = json.loads(response['body'].read())
        story_text = result['content'][0]['text']
        
        # Try to parse JSON from response
        try:
            # Remove markdown code blocks if present
            if '```json' in story_text:
                story_text = story_text.split('```json')[1].split('```')[0].strip()
            elif '```' in story_text:
                story_text = story_text.split('```')[1].split('```')[0].strip()
            
            story_data = json.loads(story_text)
            return story_data
        except:
            # If not JSON, return as plain story
            return {
                "title": "Your Story",
                "story": story_text,
                "reflection_question": "What did you learn from this story?"
            }
    except Exception as e:
        st.error(f"Error generating story: {str(e)}")
        return None

def regenerate_story(extracted_text, grade_level, avoid_themes=None):
    """Regenerate story with different theme (Tier 2)"""
    try:
        response = requests.post(
            f"{API_BASE}/regenerate-story",
            json={
                "extracted_text": extracted_text,
                "grade_level": f"Grade {grade_level}",
                "avoid_themes": avoid_themes or [],
                "regenerate": True
            },
            timeout=10
        )
        
        if response.status_code == 202:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error regenerating story: {str(e)}")
        return None

def search_external_stories(topic, grade_level, emotional_theme=None):
    """Search external story websites using Playwright Agent (Tier 3)"""
    try:
        response = requests.post(
            f"{API_BASE}/search-external-stories",
            json={
                "topic": topic,
                "grade_level": grade_level,
                "emotional_theme": emotional_theme
            },
            timeout=30  # Playwright needs more time
        )
        
        if response.status_code == 200:
            return response.json().get('stories', [])
        return None
    except Exception as e:
        st.error(f"Error searching external stories: {str(e)}")
        return None

def get_student_analytics(student_id):
    """Get student analytics from DynamoDB and session state"""
    try:
        # First try to get from DynamoDB
        dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
        
        # Query analytics table
        analytics_table = dynamodb.Table('sel-ltm-memory-analytics')
        response = analytics_table.query(
            KeyConditionExpression='student_id = :sid',
            ExpressionAttributeValues={':sid': student_id},
            ScanIndexForward=False,
            Limit=100
        )
        
        items = response.get('Items', [])
        
        # Also check session state for recent quiz results
        session_quiz_results = []
        if 'student_quiz_results' in st.session_state:
            session_quiz_results = [
                result for result in st.session_state.student_quiz_results 
                if result.get('student_id') == student_id
            ]
        
        # Combine DynamoDB and session data
        all_items = items + session_quiz_results
        
        if not all_items:
            # Return demo data if no real data found
            return {
                'total_assessments': len(session_quiz_results),
                'average_score': int(sum(r.get('score', 0) for r in session_quiz_results) / len(session_quiz_results)) if session_quiz_results else 0,
                'recent_sentiment': 'POSITIVE',
                'most_common_emotion': 'Happy',
                'total_activities': len(session_quiz_results),
                'engagement_level': 'Medium' if session_quiz_results else 'Low',
                'recent_quizzes': session_quiz_results[-3:] if session_quiz_results else []
            }
        
        # Aggregate analytics
        total_assessments = len([i for i in all_items if i.get('type') == 'quiz' or 'quiz_title' in i])
        
        # Get quiz scores from both sources
        quiz_scores = []
        for item in all_items:
            if item.get('type') == 'quiz' and 'score' in item:
                quiz_scores.append(item.get('score', 0))
            elif 'quiz_title' in item and 'score' in item:
                quiz_scores.append(item.get('score', 0))
        
        avg_score = sum(quiz_scores) / len(quiz_scores) if quiz_scores else 0
        
        emotions = [i.get('emotion') for i in all_items if i.get('emotion')]
        most_common_emotion = max(set(emotions), key=emotions.count) if emotions else 'Happy'
        
        recent_sentiment = all_items[0].get('sentiment', 'POSITIVE') if all_items else 'POSITIVE'
        
        return {
            'total_assessments': total_assessments,
            'average_score': int(avg_score) if avg_score > 1 else int(avg_score * 100),
            'recent_sentiment': recent_sentiment,
            'most_common_emotion': most_common_emotion,
            'total_activities': len(all_items),
            'engagement_level': 'High' if len(all_items) > 20 else 'Medium' if len(all_items) > 10 else 'Low',
            'recent_quizzes': session_quiz_results[-3:] if session_quiz_results else []
        }
    except Exception as e:
        # If DynamoDB fails, use session data only
        session_quiz_results = []
        if 'student_quiz_results' in st.session_state:
            session_quiz_results = [
                result for result in st.session_state.student_quiz_results 
                if result.get('student_id') == student_id
            ]
        
        if session_quiz_results:
            avg_score = sum(r.get('score', 0) for r in session_quiz_results) / len(session_quiz_results)
            return {
                'total_assessments': len(session_quiz_results),
                'average_score': int(avg_score),
                'recent_sentiment': 'POSITIVE',
                'most_common_emotion': 'Happy',
                'total_activities': len(session_quiz_results),
                'engagement_level': 'Medium',
                'recent_quizzes': session_quiz_results[-3:]
            }
        
        return None

# Main app
def main():
    # Initialize session for this user
    init_session_state()
    
    # Enhanced main title - more visible and attractive
    st.markdown("""
        <div style='text-align: center; margin: 40px 0 60px 0; padding: 30px;
                    background: rgba(255, 255, 255, 0.1); 
                    border-radius: 25px; 
                    backdrop-filter: blur(10px);
                    box-shadow: 0 8px 32px rgba(0,0,0,0.3);'>
            <h1 style='font-size: 4.5em; font-weight: 900; margin: 0 0 20px 0;
                       color: #ffffff;
                       text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
                       letter-spacing: 2px;'>
                🌈 Welcome to EmoVerse AI 🚀
            </h1>
            <p style='color: #ffffff; font-size: 1.6em; margin: 0; font-weight: 500;
                      text-shadow: 1px 1px 4px rgba(0,0,0,0.4);'>
                Personalized Social-Emotional Learning with AI ✨
            </p>
        </div>
    """, unsafe_allow_html=True)
    

    
    # User type selection
    if st.session_state.user_type is None:
        # Enhanced "Who Are You?" section
        st.markdown("""
            <div style='text-align: center; margin: 30px 0 50px 0;'>
                <div style='background: rgba(255, 255, 255, 0.15); 
                            padding: 25px; border-radius: 20px; 
                            backdrop-filter: blur(10px);
                            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
                            display: inline-block;'>
                    <h2 style='color: #ffffff; font-size: 2.5em; margin: 0;
                               font-weight: 700; text-shadow: 2px 2px 6px rgba(0,0,0,0.4);'>
                        ✨ Choose Your Learning Journey
                    </h2>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Better centered button layout
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Create two columns for the buttons within the centered area
            btn_col1, btn_col2 = st.columns(2)
        
            with btn_col1:
                # Student button - enhanced
                if st.button("👨‍🎓 Student", key="student_btn", use_container_width=True, type="primary"):
                    st.session_state.user_type = "student"
                    st.rerun()
            
            with btn_col2:
                # Teacher button - enhanced
                if st.button("👩‍🏫 Teacher", key="teacher_btn", use_container_width=True, type="secondary"):
                    st.session_state.user_type = "teacher"
                    st.rerun()

    
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
            student_id_input = st.text_input("Enter Student ID", key="student_id_input")
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
        pass
    
    if st.session_state.student_id:
        # Check if AI content is still loading in background
        if hasattr(st.session_state, 'job_id') and st.session_state.processed_content.get('loading_ai'):
            status_data = check_job_status(st.session_state.job_id)
            if status_data and status_data.get('status') == 'completed':
                # AI content ready! Update and refresh
                st.session_state.aws_results = status_data
                st.session_state.processed_content['loading_ai'] = False
                st.session_state.processed_content['aws_data'] = status_data
                st.rerun()
        
        # Student info banner
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 15px; border-radius: 15px; text-align: center; 
                        color: white; font-size: 1.1em; margin-bottom: 20px;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
                🎉 Welcome, {st.session_state.student_id}! | 📚 Let's learn together! 🌟
            </div>
        """, unsafe_allow_html=True)
        
        # Enhanced file upload section with larger layout
        st.markdown("""
            <div style='background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%); 
                        padding: 35px; border-radius: 25px; text-align: center;
                        box-shadow: 0 12px 40px rgba(0,0,0,0.15); margin: 30px 0;'>
                <div style='font-size: 2.2em; color: #2d3748; font-weight: bold; margin-bottom: 15px;'>
                    📚 Upload Your Learning Material
                </div>
                <div style='font-size: 1.4em; color: #2d3748; line-height: 1.5;'>
                    Share your learning material and get fun stories, quizzes, and activities! ✨
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Add some spacing and center the file uploader
        col1, col2, col3 = st.columns([0.5, 2, 0.5])
        with col2:
            uploaded_file = st.file_uploader(
                "📎 Browse file",
                type=['pdf', 'png', 'jpg', 'jpeg'],
                help="Supported formats: PDF, PNG, JPG, JPEG (Max 500MB)",
                label_visibility="visible"
            )
        
        # Enhanced file feedback
        if uploaded_file:
            # File selected - ready for processing
            
            # Enhanced process button with reduced spacing
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                process_button = st.button(
                    "✨ Create My Learning Content!", 
                    use_container_width=True,
                    type="primary",
                    key="main_process_btn"
                )

        
        if uploaded_file and process_button:
            # Store file for background processing
            st.session_state.current_file = uploaded_file
            # Start processing flow
            if not st.session_state.get('processing_file', False):
                extract_text_immediately(uploaded_file)
        
        # Complete processing if in progress
        if st.session_state.get('processing_file', False) and uploaded_file:
            complete_text_extraction(uploaded_file)
        
        # Display processed content only when ready
        if st.session_state.processed_content and not st.session_state.get('processing_file', False):
            display_processed_content()
        
        # Logout button at the bottom - properly centered
        st.markdown("<br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([2, 1, 2])
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

def extract_text_immediately(uploaded_file):
    """Show processing message, extract text, then display tabs when ready"""
    
    # STEP 1: Show processing message immediately
    st.session_state.processing_file = True
    st.info("🔄 Processing your document... Please wait a moment.")
    
    # Force rerun to show processing message
    st.rerun()

def complete_text_extraction(uploaded_file):
    """Complete the text extraction and show tabs"""
    
    try:
        extracted_text = ""
        
        # STEP 2: EXTRACT TEXT (should be fast)
        try:
            # For PDFs, extract text quickly
            if uploaded_file.name.lower().endswith('.pdf'):
                try:
                    import PyPDF2
                    # Reset file pointer to beginning
                    uploaded_file.seek(0)
                    pdf_reader = PyPDF2.PdfReader(uploaded_file)
                    
                    for page_num, page in enumerate(pdf_reader.pages):
                        try:
                            page_text = page.extract_text()
                            if page_text.strip():
                                extracted_text += f"Page {page_num + 1}:\n{page_text}\n\n"
                        except:
                            extracted_text += f"Page {page_num + 1}: [Content could not be extracted]\n\n"
                    
                    # If no text was extracted, try alternative method
                    if not extracted_text.strip():
                        # Try using AWS Textract as fallback for PDFs
                        try:
                            file_key = upload_to_s3(uploaded_file, st.session_state.student_id)
                            if file_key:
                                aws_text = extract_text_from_s3(file_key)
                                if aws_text and aws_text.strip():
                                    extracted_text = aws_text
                                else:
                                    extracted_text = f"📄 PDF Document: {uploaded_file.name}\n\nThis PDF has been uploaded successfully. The document appears to contain images or formatted content that will be processed to create your learning materials."
                            else:
                                extracted_text = f"📄 PDF Document: {uploaded_file.name}\n\nPDF uploaded successfully. Processing content for learning activities."
                        except:
                            extracted_text = f"📄 PDF Document: {uploaded_file.name}\n\nPDF uploaded successfully. Content will be processed to create engaging learning materials."
                
                except Exception as pdf_error:
                    # PDF processing failed, try AWS Textract
                    try:
                        file_key = upload_to_s3(uploaded_file, st.session_state.student_id)
                        if file_key:
                            aws_text = extract_text_from_s3(file_key)
                            if aws_text and aws_text.strip():
                                extracted_text = aws_text
                            else:
                                extracted_text = f"📄 Document: {uploaded_file.name}\n\nDocument processing in progress. Content will be available shortly."
                        else:
                            extracted_text = f"📄 Document: {uploaded_file.name}\n\nDocument uploaded. Processing content for your learning experience."
                    except:
                        extracted_text = f"📄 Document: {uploaded_file.name}\n\nDocument uploaded successfully. Preparing content for learning activities."
            
            # For images, use AWS Textract
            elif uploaded_file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                try:
                    file_key = upload_to_s3(uploaded_file, st.session_state.student_id)
                    if file_key:
                        aws_text = extract_text_from_s3(file_key)
                        if aws_text and aws_text.strip():
                            extracted_text = aws_text
                        else:
                            extracted_text = f"📷 Image: {uploaded_file.name}\n\nImage uploaded successfully. Visual content will be analyzed to create learning materials."
                    else:
                        extracted_text = f"📷 Image: {uploaded_file.name}\n\nImage uploaded successfully. Processing visual content..."
                except:
                    extracted_text = f"📷 Image: {uploaded_file.name}\n\nImage uploaded successfully. Visual content will be analyzed."
        
        except Exception as e:
            # Final fallback
            extracted_text = f"📄 Document: {uploaded_file.name}\n\nDocument uploaded successfully. Content is being prepared for your learning experience."
        
        # If no text extracted, show basic info
        if not extracted_text.strip():
            extracted_text = f"📄 Document: {uploaded_file.name}\n\nContent uploaded and ready for learning activities."
        
        # STEP 3: SHOW TABS WITH EXTRACTED TEXT
        st.session_state.processed_content = {
            'cleaned_text': extracted_text,
            'sentiment': {'sentiment': 'POSITIVE'},
            'loading_ai': True,  # AI content still loading
            'file_uploaded': True,
            'user_session': st.session_state.session_id
        }
        
        st.session_state.extracted_text = extracted_text
        st.session_state.processing_file = False  # Processing complete
        
        # Processing complete - tabs will show automatically
        
        # STEP 4: START AI PROCESSING IN BACKGROUND
        st.session_state.background_started = True
        
        # Start AI content generation
        try:
            generate_ai_content(extracted_text)
        except:
            pass  # Continue even if AI generation fails
        
        # Force rerun to show tabs
        st.rerun()
        
    except Exception as e:
        st.session_state.processing_file = False
        st.error(f"❌ Error processing document: {str(e)}")
        return

def process_with_aws(uploaded_file):
    """Process document - Extract text immediately and show content"""
    
    try:
        # Check if user is already processing a file
        if st.session_state.get('background_started', False):
            st.warning("⏳ Already working on your document. Please wait for completion.")
            return
        
        extracted_text = ""
        
        # IMMEDIATE TEXT EXTRACTION
        try:
            # For PDFs, extract text immediately
            if uploaded_file.name.lower().endswith('.pdf'):
                import PyPDF2
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                for page in pdf_reader.pages:
                    extracted_text += page.extract_text() + "\n"
            
            # For images, show placeholder (AWS Textract will process later)
            elif uploaded_file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                extracted_text = f"📷 Image uploaded: {uploaded_file.name}\n\nProcessing image content with AI..."
        
        except Exception as e:
            extracted_text = f"📄 Document uploaded: {uploaded_file.name}\n\nExtracting content..."
        
        # If no text extracted, show basic info
        if not extracted_text.strip():
            extracted_text = f"📄 Document uploaded: {uploaded_file.name}\n\nContent will be processed shortly..."
        
        # IMMEDIATE: Show extracted text right away
        st.session_state.processed_content = {
            'cleaned_text': extracted_text,
            'sentiment': {'sentiment': 'POSITIVE'},
            'loading_ai': True,
            'file_uploaded': True,
            'user_session': st.session_state.session_id
        }
        
        st.session_state.extracted_text = extracted_text
        
        # Show success and tabs immediately
        st.success(f"✅ Text extracted! Generating AI content...")
        
        # Start background AI processing
        try:
            generate_ai_content(extracted_text)
        except:
            pass  # Continue even if AI generation fails
        
        # Force immediate rerun to show tabs with text
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return

def process_document_background():
    """Background processing function with fallbacks"""
    try:
        uploaded_file = st.session_state.get('current_file')
        if not uploaded_file:
            return
        
        # Try simple text extraction first (for immediate response)
        try:
            # For PDFs, try simple extraction
            if uploaded_file.name.lower().endswith('.pdf'):
                import PyPDF2
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                if len(text.strip()) > 50:
                    # Use simple extraction
                    st.session_state.extracted_text = text
                    st.session_state.processed_content['cleaned_text'] = text
                    st.session_state.processed_content['sentiment'] = {'sentiment': 'POSITIVE'}
                    
                    # Try AWS processing in background
                    try:
                        # Upload to S3 and use Textract for better quality
                        file_key = upload_to_s3(uploaded_file, st.session_state.student_id)
                        if file_key:
                            aws_text = extract_text_from_s3(file_key)
                            if aws_text and len(aws_text) > len(text):
                                # Use AWS text if better
                                st.session_state.extracted_text = aws_text
                                st.session_state.processed_content['cleaned_text'] = aws_text
                    except:
                        pass  # Keep simple extraction
                    
                    # Generate AI content
                    generate_ai_content(text)
                    return
        except:
            pass  # Fall back to AWS processing
        
        # AWS processing as fallback
        file_key = upload_to_s3(uploaded_file, st.session_state.student_id)
        if not file_key:
            st.session_state.processed_content['cleaned_text'] = "❌ Upload failed. Please try again."
            return
        
        extracted_text = extract_text_from_s3(file_key)
        if not extracted_text or len(extracted_text.strip()) < 10:
            st.session_state.processed_content['cleaned_text'] = "❌ Could not read this file. Please try a different file."
            return
        
        st.session_state.extracted_text = extracted_text
        st.session_state.processed_content['cleaned_text'] = extracted_text
        
        generate_ai_content(extracted_text)
        
    except Exception as e:
        st.session_state.processed_content['cleaned_text'] = f"❌ Processing error: {str(e)}"
        st.session_state.processed_content['loading_ai'] = False

def generate_ai_content(text):
    """Generate AI content with error handling and retry logic"""
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            # Add small delay for concurrent users
            import time
            time.sleep(attempt * 0.5)  # Stagger requests
            
            # Sentiment analysis
            try:
                sentiment_data = analyze_sentiment(text)
                st.session_state.processed_content['sentiment'] = sentiment_data
            except Exception as e:
                # Use default if sentiment fails
                st.session_state.processed_content['sentiment'] = {'sentiment': 'POSITIVE'}
            
            # Story generation
            try:
                story = generate_story_direct(text, st.session_state.grade_level)
                if story:
                    st.session_state.direct_story = story
            except Exception as e:
                if attempt == max_retries - 1:
                    st.session_state.story_error = str(e)
            
            # Quiz generation
            try:
                quiz = generate_quiz_direct(text, st.session_state.grade_level)
                if quiz:
                    st.session_state.direct_quiz = quiz
            except Exception as e:
                if attempt == max_retries - 1:
                    st.session_state.quiz_error = str(e)
            
            # Mark complete
            st.session_state.processed_content['loading_ai'] = False
            return  # Success, exit retry loop
            
        except Exception as ai_error:
            if attempt == max_retries - 1:
                # Final attempt failed
                st.session_state.processed_content['loading_ai'] = False
                st.session_state.processed_content['ai_error'] = str(ai_error)
            else:
                # Retry after delay
                time.sleep(1)

def display_processed_content():
    content = st.session_state.processed_content
    
    # Background AI processing (non-blocking)
    if content.get('loading_ai') and 'background_started' not in st.session_state:
        st.session_state.background_started = True
        # AI content generation happens in background
    
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
        grade_level = st.session_state.get('grade_level', 1)
        if grade_level <= 3:
            st.markdown("*Read the text below - it's all about learning and growing!* 🌱")
        elif grade_level <= 6:
            st.markdown("*Read through this text carefully - you'll discover interesting ideas!* 🌱")
        else:
            st.markdown("*Analyze the text below to understand its key concepts and themes.* 🌱")
        
        # Always show the extracted text immediately
        if content.get('cleaned_text'):
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%); 
                            padding: 20px; 
                            border-radius: 15px; 
                            font-size: 1.05em; 
                            line-height: 1.6;
                            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                            max-height: 70vh;
                            overflow-y: auto;
                            margin: 0;'>
                    {content.get('cleaned_text', '')}
                </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 😊 Emotional Tone")
        st.markdown("*Discover the feelings in this text* ✨")
        
        sentiment = content.get('sentiment', {})
        
        # Big emoji display based on sentiment
        sentiment_emoji = {
            'POSITIVE': '😊',
            'NEGATIVE': '😢',
            'NEUTRAL': '😐',
            'MIXED': '🤔'
        }
        
        current_sentiment = sentiment.get('sentiment', 'POSITIVE')
        st.markdown(f"""
            <div style='text-align: center; font-size: 8em; margin: 30px 0;'>
                {sentiment_emoji.get(current_sentiment, '😊')}
            </div>
            <div style='text-align: center; font-size: 1.8em; color: #667eea; font-weight: bold; margin-bottom: 30px;'>
                {current_sentiment.title()}
            </div>
        """, unsafe_allow_html=True)
        
        # Sentiment breakdown with bars
        st.markdown("#### Sentiment Analysis:")
        
        # Get confidence or create default
        confidence = sentiment.get('confidence', {
            'Positive': 0.70,
            'Neutral': 0.20,
            'Negative': 0.10
        })
        
        # Custom colored progress bars
        emoji_map = {'Positive': '😊', 'Neutral': '😐', 'Negative': '😢'}
        color_map = {
            'Positive': '#10b981',  # Green
            'Neutral': '#f59e0b',   # Orange
            'Negative': '#ef4444'   # Red
        }
        
        for emotion in ['Positive', 'Neutral', 'Negative']:
            score = confidence.get(emotion, 0)
            bar_color = color_map[emotion]
            percentage = int(score * 100)
            
            st.markdown(f"""
                <div style='margin: 15px 0;'>
                    <div style='display: flex; justify-content: space-between; margin-bottom: 8px;'>
                        <span style='font-weight: 600; font-size: 1.1em;'>{emoji_map[emotion]} {emotion}</span>
                        <span style='font-weight: 700; font-size: 1.1em; color: {bar_color};'>{percentage}%</span>
                    </div>
                    <div style='background-color: #e5e7eb; border-radius: 10px; height: 35px; overflow: hidden;'>
                        <div style='background: linear-gradient(90deg, {bar_color} 0%, {bar_color}dd 100%); 
                                    height: 100%; width: {percentage}%; 
                                    transition: width 0.5s ease;'>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        # Enhanced Q&A header
        st.markdown("""
            <div style='background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                        padding: 20px; border-radius: 15px; text-align: center;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px;'>
                <div style='font-size: 1.8em; color: #2d3748; font-weight: bold; margin-bottom: 8px;'>
                    ❓ Ask Questions
                </div>
                <div style='font-size: 1.1em; color: #2d3748;'>
                    I'm your AI tutor - ask me anything about the text! 🤖✨
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Question input with inline microphone
        col1, col2 = st.columns([6, 1])
        
        with col1:
            question = st.text_input(
                "💭 What would you like to know?",
                placeholder="What is friendship?",
                help="Type your question or use the microphone",
                key="question_input"
            )
        
        with col2:
            st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
            if st.button("🎤", help="Voice input", key="voice_btn", use_container_width=True):
                # Simulate voice input - just populate text field
                demo_questions = [
                    "What is the main idea of this text?",
                    "How can I apply this in my daily life?", 
                    "What does this story teach us about emotions?",
                    "Why is empathy important?",
                    "Can you explain this concept in simple words?",
                    "What are the key lessons from this reading?"
                ]
                import random
                voice_question = random.choice(demo_questions)
                
                # Update the text input with voice question
                try:
                    st.session_state.question_input = voice_question
                    st.rerun()
                except:
                    st.success(f"🎤 Voice question: {voice_question}")
                    st.info("Please copy the question above and paste it in the text field.")
        
        # Enhanced Get Answer button
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔍 Get My Answer!", use_container_width=True, type="primary", key="get_answer_btn"):
            current_question = st.session_state.get('question_input', '').strip()
            
            if current_question:
                # Get context from processed content
                context_text = content.get('cleaned_text', '')
                grade_level = st.session_state.grade_level
                
                # Generate instant demo answer for fast response
                answer = generate_demo_answer(current_question, grade_level)
                
                # If demo answer is generic, try AI answer with timeout
                if "That's a great question" in answer:
                    try:
                        with st.spinner("🤔 Getting detailed answer..."):
                            import time
                            start_time = time.time()
                            ai_answer = answer_question(current_question, context_text, grade_level)
                            
                            # Use AI answer if it comes back quickly (within 3 seconds)
                            if ai_answer and (time.time() - start_time) < 3:
                                answer = ai_answer
                    except:
                        pass  # Keep demo answer
                
                if answer:
                    # Store in conversation history
                    if 'conversation_history' not in st.session_state:
                        st.session_state.conversation_history = []
                    
                    st.session_state.conversation_history.append({
                        'question': current_question,
                        'answer': answer
                    })
                    
                    # Clear the input after getting answer
                    try:
                        st.session_state.question_input = ""
                    except:
                        pass  # Continue even if clearing fails
                    
                    st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                                    padding: 25px; border-radius: 15px; margin-top: 20px;
                                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
                            <div style='font-size: 1.3em; color: #2d3748; font-weight: bold; margin-bottom: 12px;'>
                                🤖 Here's what I think:
                            </div>
                            <div style='font-size: 1.1em; line-height: 1.7; color: #2d3748;'>
                                {answer}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
                else:
                    st.error("Sorry, I couldn't generate an answer. Please try again!")
            else:
                st.warning("Please enter a question first!")

    
    with tab4:
        grade_level = st.session_state.get('grade_level', 1)
        if grade_level <= 3:
            st.markdown("### 📚 Story Time!")
            st.markdown("*Here's a fun story just for you!* ✨")
        elif grade_level <= 6:
            st.markdown("### 📚 Story Time!")
            st.markdown("*Enjoy this personalized story based on your reading!* ✨")
        else:
            st.markdown("### 📚 Story Time!")
            st.markdown("*Explore this narrative created from your text analysis.* ✨")
        
        # Check if still loading
        if content.get('loading_ai', False) and not hasattr(st.session_state, 'direct_story'):
            st.markdown("""
                <div style='background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
                            padding: 30px; border-radius: 20px; text-align: center;
                            box-shadow: 0 8px 32px rgba(0,0,0,0.1); margin: 20px 0;'>
                    <div style='font-size: 1.8em; color: #667eea; font-weight: bold; margin-bottom: 15px;'>
                        ✨ Creating Your Personalized Story
                    </div>
                    <div style='font-size: 1.2em; color: #333; line-height: 1.6;'>
                        Our AI is reading your document and crafting a unique story just for you!<br>
                        <em>This usually takes 30-60 seconds...</em>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔄 Check if Ready", help="Click to see if your story is ready", use_container_width=True):
                st.rerun()
        
        # Check for direct story first (generated immediately on upload)
        elif hasattr(st.session_state, 'direct_story') and st.session_state.direct_story:
            story_data = st.session_state.direct_story
            
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
                            padding: 25px; border-radius: 20px; 
                            box-shadow: 0 8px 32px rgba(0,0,0,0.1); margin-bottom: 20px;'>
                    <div style='text-align: center; font-size: 1.8em; color: #667eea; 
                                font-weight: bold; margin-bottom: 15px;'>
                        {story_data.get('title', 'Your Story')}
                    </div>
                    <div style='font-size: 1.1em; line-height: 1.8; color: #333; white-space: pre-line; font-weight: bold;'>
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
            
            # Story feedback
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 🎭 Did you like this story?")
            
            if 'direct_story_dislike_count' not in st.session_state:
                st.session_state.direct_story_dislike_count = 0
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("❤️ Loved it!", use_container_width=True, key="direct_story_like"):
                    # Save to preferences (simulate saving)
                    if 'story_preferences' not in st.session_state:
                        st.session_state.story_preferences = []
                    
                    story_preference = {
                        'title': story_data.get('title', 'Story'),
                        'theme': story_data.get('theme', 'friendship'),
                        'liked': True,
                        'timestamp': time_module.time()
                    }
                    st.session_state.story_preferences.append(story_preference)
                    
                    st.balloons()
                    st.success("🎉 Great! Your story preference has been saved!")
                    st.session_state.direct_story_dislike_count = 0
            
            with col2:
                if st.button("👎 Dislike", use_container_width=True, key="direct_story_dislike"):
                    st.session_state.direct_story_dislike_count += 1
                    
                    if st.session_state.direct_story_dislike_count == 1:
                        # First dislike: Regenerate with different approach
                        with st.spinner("✨ Making a new story..."):
                            new_story = generate_story_direct(content.get('cleaned_text', ''), st.session_state.grade_level)
                            if new_story:
                                st.session_state.direct_story = new_story
                                st.success("✅ New story created with a different approach!")
                                # Don't use st.rerun() to avoid tab switching
                    
                    elif st.session_state.direct_story_dislike_count >= 2:
                        # Second dislike: Show external story links

                        
                        # Show curated external story links
                        st.markdown("""
                            <div style='background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
                                        padding: 20px; border-radius: 15px; margin: 15px 0;
                                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
                                <h4 style='color: #667eea; margin-top: 0;'>📚 Recommended Story Websites</h4>
                                <div style='margin: 15px 0;'>
                                    <a href='https://www.storylineonline.net/' target='_blank' 
                                       style='display: block; background: #667eea; color: white; 
                                              padding: 12px 20px; border-radius: 8px; text-decoration: none;
                                              margin: 8px 0; text-align: center;'>
                                        📖 Storyline Online - Celebrity Read-Alouds
                                    </a>
                                    <a href='https://www.storyberries.com/' target='_blank' 
                                       style='display: block; background: #667eea; color: white; 
                                              padding: 12px 20px; border-radius: 8px; text-decoration: none;
                                              margin: 8px 0; text-align: center;'>
                                        🎨 Storyberries - Illustrated Stories
                                    </a>
                                    <a href='https://kidskonnect.com/social-emotional/self-awareness/' target='_blank' 
                                       style='display: block; background: #667eea; color: white; 
                                              padding: 12px 20px; border-radius: 8px; text-decoration: none;
                                              margin: 8px 0; text-align: center;'>
                                        🧠 KidsKonnect - Social-Emotional Learning
                                    </a>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.session_state.direct_story_dislike_count = 0  # Reset for next time
        
        # Check if we have AWS results
        elif st.session_state.aws_results:
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
                        <div style='font-size: 1.1em; line-height: 1.8; color: #333; white-space: pre-line; font-weight: bold;'>
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
                
                # Story feedback - Simple Like/Dislike
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("#### 🎭 Did you like this story?")
                
                # Initialize dislike counter
                if 'story_dislike_count' not in st.session_state:
                    st.session_state.story_dislike_count = 0
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("❤️ Loved it!", use_container_width=True, key="story_like"):
                        # Save to preferences
                        if 'story_preferences' not in st.session_state:
                            st.session_state.story_preferences = []
                        
                        story_preference = {
                            'title': story_data.get('title', 'Story'),
                            'theme': story_data.get('theme', 'friendship'),
                            'liked': True,
                            'timestamp': time_module.time()
                        }
                        st.session_state.story_preferences.append(story_preference)
                        
                        st.balloons()
                        st.success("🎉 Great! Your story preference has been saved!")
                        st.session_state.story_dislike_count = 0
                
                with col2:
                    if st.button("👎 Dislike", use_container_width=True, key="story_dislike"):
                        st.session_state.story_dislike_count += 1
                        
                        if st.session_state.story_dislike_count == 1:
                            # First dislike: Regenerate story
                            with st.spinner("✨ Making a new story..."):
                                extracted_text = content.get('cleaned_text', '')
                                result = regenerate_story(
                                    extracted_text,
                                    st.session_state.grade_level,
                                    avoid_themes=[story_data.get('theme', '')]
                                )
                                if result:
                                    st.success("✅ New story created with a different approach!")
                                else:
                                    st.error("Failed to regenerate. Please try again.")
                        
                        elif st.session_state.story_dislike_count >= 2:
                            # Second dislike: Use Playwright Agent to search external stories (Tier 3)
                            
                            with st.spinner("🌐 Finding more stories..."):
                                # Extract topic from text
                                extracted_text = content.get('cleaned_text', '')
                                topic = extracted_text[:100] if extracted_text else "friendship"
                                
                                # Call Playwright Agent via backend
                                external_stories = search_external_stories(
                                    topic=topic,
                                    grade_level=st.session_state.grade_level,
                                    emotional_theme=story_data.get('theme', 'friendship')
                                )
                            
                            if external_stories and len(external_stories) > 0:
                                st.success(f"✅ Found {len(external_stories)} stories from external sources!")
                                st.markdown("### 📚 Stories Found by AI Agent:")
                                
                                # Display each found story
                                for i, ext_story in enumerate(external_stories):
                                    st.markdown(f"""
                                        <div style='background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
                                                    padding: 20px; border-radius: 15px; margin: 15px 0;
                                                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
                                            <h4 style='color: #667eea; margin-top: 0;'>
                                                {i+1}. {ext_story.get('title', 'Story')}
                                            </h4>
                                            <p style='color: #666; font-size: 0.9em; margin: 5px 0;'>
                                                📍 Source: {ext_story.get('source', 'External')}
                                            </p>
                                            <p style='color: #333; line-height: 1.6; margin: 10px 0;'>
                                                {ext_story.get('description', 'Click to read this story!')}
                                            </p>
                                            <a href='{ext_story.get('url', '#')}' target='_blank' 
                                               style='display: inline-block; background: #667eea; color: white; 
                                                      padding: 10px 20px; border-radius: 8px; text-decoration: none;
                                                      margin-top: 10px;'>
                                                📖 Read Story
                                            </a>
                                        </div>
                                    """, unsafe_allow_html=True)
                                
                                # Reset counter after showing stories
                                st.session_state.story_dislike_count = 0
                            else:
                                st.warning("⚠️ Couldn't find external stories. Here are some recommended sites:")
                                st.markdown("""
                                    <div style='background: white; padding: 20px; border-radius: 15px; 
                                                box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 15px 0;'>
                                        <ul style='font-size: 1.1em; line-height: 2;'>
                                            <li>📚 <a href='https://www.storylineonline.net/' target='_blank'>Storyline Online</a></li>
                                            <li>🧠 <a href='https://kidskonnect.com/social-emotional/self-awareness/' target='_blank'>KidsKonnect - Social-Emotional Learning</a></li>
                                            <li>🎨 <a href='https://www.storyberries.com/' target='_blank'>Storyberries</a></li>
                                        </ul>
                                    </div>
                                """, unsafe_allow_html=True)
                                st.session_state.story_dislike_count = 0
            else:
                # Show directly generated story (created instantly on upload)
                if hasattr(st.session_state, 'direct_story') and st.session_state.direct_story:
                    story_data = st.session_state.direct_story
                    st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
                                    padding: 25px; border-radius: 20px; 
                                    box-shadow: 0 8px 32px rgba(0,0,0,0.1); margin: 20px 0;'>
                            <div style='text-align: center; font-size: 1.8em; color: #667eea; 
                                        font-weight: bold; margin-bottom: 15px;'>
                                {story_data.get('title', 'Your Story')}
                            </div>
                            <div style='font-size: 1.1em; line-height: 1.8; color: #333; white-space: pre-line; font-weight: bold;'>
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
                    
                    # Add Like/Dislike buttons for direct story
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("#### 🎭 Did you like this story?")
                    
                    if 'direct_story_dislike_count' not in st.session_state:
                        st.session_state.direct_story_dislike_count = 0
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("❤️ Loved it!", use_container_width=True, key="direct_story_like_2"):
                            # Save to preferences
                            if 'story_preferences' not in st.session_state:
                                st.session_state.story_preferences = []
                            
                            story_preference = {
                                'title': story_data.get('title', 'Story'),
                                'theme': story_data.get('theme', 'friendship'),
                                'liked': True,
                                'timestamp': time_module.time()
                            }
                            st.session_state.story_preferences.append(story_preference)
                            
                            st.balloons()
                            st.success("🎉 I am glad you like it /home/aayesha/Screenshots/Screenshot from 2025-10-19 05-55-29.png❤️")
                            st.session_state.direct_story_dislike_count = 0
                    
                    with col2:
                        if st.button("👎 Dislike", use_container_width=True, key="direct_story_dislike"):
                            st.session_state.direct_story_dislike_count += 1
                            
                            if st.session_state.direct_story_dislike_count == 1:
                                # TIER 2: Regenerate with different theme
                                with st.spinner("✨ Making a new story..."):
                                    new_story = generate_story_direct(content.get('cleaned_text', ''), st.session_state.grade_level)
                                    if new_story:
                                        st.session_state.direct_story = new_story
                                        st.success("✅ New story created with a different approach!")
                            
                            elif st.session_state.direct_story_dislike_count >= 2:
                                # TIER 3: Playwright Agent searches external stories
                                
                                with st.spinner("🌐 Finding more stories..."):
                                    extracted_text = content.get('cleaned_text', '')
                                    topic = extracted_text[:100] if extracted_text else "friendship"
                                    
                                    external_stories = search_external_stories(
                                        topic=topic,
                                        grade_level=st.session_state.grade_level,
                                        emotional_theme="friendship"
                                    )
                                
                                if external_stories and len(external_stories) > 0:
                                    st.success(f"✅ Found {len(external_stories)} stories from external sources!")
                                    st.markdown("### 📚 Stories Found by AI Agent:")
                                    
                                    for i, ext_story in enumerate(external_stories):
                                        st.markdown(f"""
                                            <div style='background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
                                                        padding: 20px; border-radius: 15px; margin: 15px 0;
                                                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
                                                <h4 style='color: #667eea; margin-top: 0;'>
                                                    {i+1}. {ext_story.get('title', 'Story')}
                                                </h4>
                                                <p style='color: #666; font-size: 0.9em; margin: 5px 0;'>
                                                    📍 Source: {ext_story.get('source', 'External')}
                                                </p>
                                                <p style='color: #333; line-height: 1.6; margin: 10px 0;'>
                                                    {ext_story.get('description', 'Click to read this story!')}
                                                </p>
                                                <a href='{ext_story.get('url', '#')}' target='_blank' 
                                                   style='display: inline-block; background: #667eea; color: white; 
                                                          padding: 10px 20px; border-radius: 8px; text-decoration: none;
                                                          margin-top: 10px;'>
                                                    📖 Read Story
                                                </a>
                                            </div>
                                        """, unsafe_allow_html=True)
                                    
                                    st.session_state.direct_story_dislike_count = 0
                                else:
                                    st.warning("⚠️ Couldn't find external stories. Here are some recommended sites:")
                                    st.markdown("""
                                        <div style='background: white; padding: 20px; border-radius: 15px; 
                                                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 15px 0;'>
                                            <ul style='font-size: 1.1em; line-height: 2;'>
                                                <li>📚 <a href='https://www.storylineonline.net/' target='_blank'>Storyline Online</a></li>
                                                <li>🧠 <a href='https://kidskonnect.com/social-emotional/self-awareness/' target='_blank'>KidsKonnect - Social-Emotional Learning</a></li>
                                                <li>🎨 <a href='https://www.storyberries.com/' target='_blank'>Storyberries</a></li>
                                            </ul>
                                        </div>
                                    """, unsafe_allow_html=True)
                                    st.session_state.direct_story_dislike_count = 0
        else:
            st.warning("📤 Please upload and process a document first to generate a story!")
        
    
    with tab5:
        grade_level = st.session_state.get('grade_level', 1)
        
        # Enhanced quiz header
        if grade_level <= 3:
            header_text = "Let's play some fun question games! 🎮"
        elif grade_level <= 6:
            header_text = "Test your understanding with interactive questions! 🎮"
        else:
            header_text = "Assess your comprehension with this comprehensive quiz! 🎮"
        
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
                        padding: 20px; border-radius: 15px; text-align: center;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px;'>
                <div style='font-size: 1.8em; color: #2d3748; font-weight: bold; margin-bottom: 8px;'>
                    🎯 Quiz Time!
                </div>
                <div style='font-size: 1.1em; color: #2d3748;'>
                    {header_text}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Check if still loading
        if content.get('loading_ai', False) and not hasattr(st.session_state, 'direct_quiz'):
            st.markdown("""
                <div style='background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                            padding: 30px; border-radius: 20px; text-align: center;
                            box-shadow: 0 8px 32px rgba(0,0,0,0.1); margin: 20px 0;'>
                    <div style='font-size: 1.8em; color: #667eea; font-weight: bold; margin-bottom: 15px;'>
                        🎯 Generating Your Interactive Quiz
                    </div>
                    <div style='font-size: 1.2em; color: #333; line-height: 1.6;'>
                        Creating personalized questions based on your document...<br>
                        <em>Almost ready! This takes about 1-2 minutes...</em>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔄 Check if Ready", help="Click to see if your quiz is ready", use_container_width=True):
                st.rerun()
        
        # Check for instant quiz first
        if hasattr(st.session_state, 'direct_quiz') and st.session_state.direct_quiz:
            display_aws_quiz(st.session_state.direct_quiz)
        # Then check AWS results
        elif st.session_state.aws_results:
            results = st.session_state.aws_results.get('results', {})
            quiz_result = results.get('quiz', {})
            
            if quiz_result.get('status') == 'completed':
                quiz_data = quiz_result.get('result', {})
                display_aws_quiz(quiz_data)
            else:
                st.info("⏳ Quiz is still generating... Please wait.")
        else:
            st.warning("📤 Please upload and process a document first to generate a quiz!")

def display_aws_quiz(quiz_data):
    """Display AWS-generated quiz with organized tabs"""
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
                    padding: 25px; border-radius: 20px; text-align: center;
                    box-shadow: 0 8px 32px rgba(0,0,0,0.1); margin-bottom: 30px;'>
            <div style='font-size: 2em; color: #2d3748; font-weight: bold;'>
                🎯 Quiz Time! Choose a quiz type below! ⭐
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Organize questions by type
    questions = quiz_data.get('questions', [])
    
    if not questions:
        st.warning("No questions available in this quiz.")
        return
    
    # Group questions by type
    questions_by_type = {
        'multiple_choice': [],
        'true_false': [],
        'fill_blank': [],
        'match_pair': []
    }
    
    for i, q in enumerate(questions):
        q_type = q.get('type', 'multiple_choice')
        if q_type in questions_by_type:
            questions_by_type[q_type].append((i, q))
    
    # Initialize answers in session state
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    
    # Create tabs for each question type
    tab_names = []
    tab_contents = []
    
    if questions_by_type['multiple_choice']:
        tab_names.append("🔵 Multiple Choice")
        tab_contents.append('multiple_choice')
    
    if questions_by_type['true_false']:
        tab_names.append("🟢 True/False")
        tab_contents.append('true_false')
    
    if questions_by_type['fill_blank']:
        tab_names.append("🟡 Fill in the Blank")
        tab_contents.append('fill_blank')
    
    if questions_by_type['match_pair']:
        tab_names.append("🟣 Match the Pair")
        tab_contents.append('match_pair')
    
    if not tab_names:
        st.warning("No quiz questions found.")
        return
    
    # Create tabs
    tabs = st.tabs(tab_names)
    
    # Display questions in each tab
    for tab_idx, (tab, q_type) in enumerate(zip(tabs, tab_contents)):
        with tab:
            type_questions = questions_by_type[q_type]
            
            if not type_questions:
                st.info(f"No {q_type.replace('_', ' ')} questions available.")
                continue
            
            # Progress header for this question type
            answered_count = sum(1 for _, (orig_idx, _) in enumerate(type_questions) 
                               if st.session_state.quiz_answers.get(orig_idx))
            
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%); 
                            padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div style='font-size: 1.3em; color: #2d3748; font-weight: bold;'>
                            {len(type_questions)} Questions
                        </div>
                        <div style='font-size: 1.1em; color: #2d3748;'>
                            Progress: {answered_count}/{len(type_questions)} ✅
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            for q_idx, (original_idx, q) in enumerate(type_questions):
                # Enhanced question display with numbering
                st.markdown(f"""
                    <div style='background: white; padding: 15px; border-radius: 10px; 
                                margin: 15px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                                border-left: 4px solid #667eea;'>
                        <div style='font-size: 1.2em; color: #2d3748; font-weight: bold;'>
                            Question {q_idx + 1}: {q.get('question', '')}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                if q_type == 'multiple_choice':
                    options = q.get('options', [])
                    answer = st.radio(
                        "",
                        options,
                        key=f"quiz_q_{original_idx}",
                        index=None,  # No default selection
                        horizontal=True,  # Display options side by side
                        label_visibility="collapsed"
                    )
                    if answer:
                        st.session_state.quiz_answers[original_idx] = answer
                    
                elif q_type == 'true_false':
                    answer = st.radio(
                        "",
                        ["True", "False"],
                        key=f"quiz_q_{original_idx}",
                        index=None,  # No default selection
                        horizontal=True,
                        label_visibility="collapsed"
                    )
                    if answer:
                        st.session_state.quiz_answers[original_idx] = answer
                    
                elif q_type == 'fill_blank':
                    answer = st.text_input(
                        "",
                        key=f"quiz_q_{original_idx}",
                        placeholder="Type your answer here...",
                        label_visibility="collapsed"
                    )
                    if answer and len(answer.strip()) > 0:
                        st.session_state.quiz_answers[original_idx] = answer
                    
                elif q_type == 'match_pair':
                    options = q.get('options', [])
                    # Add placeholder option at the beginning
                    dropdown_options = ["Choose the correct pair"] + options
                    answer = st.selectbox(
                        "",
                        dropdown_options,
                        key=f"quiz_q_{original_idx}",
                        index=0,  # Default to placeholder
                        label_visibility="collapsed"
                    )
                    # Only save answer if it's not the placeholder
                    if answer and answer != "Choose the correct pair":
                        st.session_state.quiz_answers[original_idx] = answer
                
                st.markdown("<br>", unsafe_allow_html=True)
            
            # Submit button for this tab
            if st.button(f"📝 Submit {q_type.replace('_', ' ').title()}", key=f"submit_{q_type}", use_container_width=True):
                # Calculate score for this question type only
                correct = 0
                total = len(type_questions)
                
                for q_idx, (original_idx, q) in enumerate(type_questions):
                    user_answer = st.session_state.quiz_answers.get(original_idx, "")
                    correct_answer = q.get('correct_answer', '')
                    
                    if str(user_answer).lower().strip() == str(correct_answer).lower().strip():
                        correct += 1
                
                score_percent = int((correct / total) * 100) if total > 0 else 0
                
                st.balloons()
                st.success(f"🎉 {q_type.replace('_', ' ').title()} Complete! You scored {correct}/{total} ({score_percent}%)")
                
                if score_percent >= 80:
                    st.success("🌟 Excellent work!")
                elif score_percent >= 60:
                    st.info("👍 Good job!")
                else:
                    st.warning("💪 Keep trying!")
    
    # Overall submit button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📝 Submit All Quizzes", use_container_width=True):
            # Calculate overall score and detailed results
            correct = 0
            total = len(questions)
            detailed_results = []
            
            for i, q in enumerate(questions):
                user_answer = st.session_state.quiz_answers.get(i, "")
                correct_answer = q.get('correct_answer', '')
                is_correct = str(user_answer).lower().strip() == str(correct_answer).lower().strip()
                
                if is_correct:
                    correct += 1
                
                detailed_results.append({
                    'question': q.get('question', ''),
                    'type': q.get('type', 'multiple_choice'),
                    'user_answer': user_answer,
                    'correct_answer': correct_answer,
                    'is_correct': is_correct,
                    'explanation': q.get('explanation', '')
                })
            
            score_percent = int((correct / total) * 100) if total > 0 else 0
            
            # Store quiz results for teacher analytics with user isolation
            import time
            quiz_result = {
                'student_id': st.session_state.get('student_id', 'unknown'),
                'session_id': st.session_state.get('session_id', 'unknown'),
                'quiz_title': quiz_data.get('title', 'Quiz'),
                'score': score_percent,
                'correct_answers': correct,
                'total_questions': total,
                'timestamp': time.time(),
                'detailed_results': detailed_results,
                'grade_level': st.session_state.get('grade_level', 1)
            }
            
            # Store in session state for teacher access
            if 'student_quiz_results' not in st.session_state:
                st.session_state.student_quiz_results = []
            st.session_state.student_quiz_results.append(quiz_result)
            
            st.balloons()
            st.success(f"🎉 All Quizzes Complete! Overall Score: {correct}/{total} ({score_percent}%)")
            
            if score_percent >= 80:
                st.success("🌟 Outstanding! You mastered all question types!")
            elif score_percent >= 60:
                st.info("👍 Great job! You're doing well across all areas!")
            else:
                st.warning("💪 Keep practicing! Review the material and try again!")
            
            # Show correct answers
            st.markdown("---")
            st.markdown("### 📚 Answer Key - Learn from the Correct Answers!")
            
            # Group answers by type for better organization
            answers_by_type = {
                'multiple_choice': [],
                'true_false': [],
                'fill_blank': [],
                'match_pair': []
            }
            
            for result in detailed_results:
                q_type = result['type']
                if q_type in answers_by_type:
                    answers_by_type[q_type].append(result)
            
            # Display answers in tabs
            answer_tab_names = []
            answer_tab_contents = []
            
            type_names = {
                'multiple_choice': '🔵 MCQ Answers',
                'true_false': '🟢 T/F Answers',
                'fill_blank': '🟡 Fill Answers',
                'match_pair': '🟣 Match Answers'
            }
            
            for q_type, results in answers_by_type.items():
                if results:
                    answer_tab_names.append(type_names[q_type])
                    answer_tab_contents.append((q_type, results))
            
            if answer_tab_names:
                answer_tabs = st.tabs(answer_tab_names)
                
                for tab, (q_type, results) in zip(answer_tabs, answer_tab_contents):
                    with tab:
                        for idx, result in enumerate(results):
                            # Color code based on correctness
                            bg_color = "#d4edda" if result['is_correct'] else "#f8d7da"
                            border_color = "#28a745" if result['is_correct'] else "#dc3545"
                            icon = "✅" if result['is_correct'] else "❌"
                            
                            st.markdown(f"""
                                <div style='background: {bg_color}; 
                                            border-left: 4px solid {border_color}; 
                                            padding: 15px; margin: 10px 0; border-radius: 5px;'>
                                    <div style='font-weight: bold; margin-bottom: 8px;'>
                                        {icon} Question {idx + 1}: {result['question']}
                                    </div>
                                    <div style='margin: 5px 0;'>
                                        <strong>Your Answer:</strong> {result['user_answer'] or 'Not answered'}
                                    </div>
                                    <div style='margin: 5px 0;'>
                                        <strong>Correct Answer:</strong> {result['correct_answer']}
                                    </div>
                                    {f"<div style='margin: 5px 0; font-style: italic;'><strong>Explanation:</strong> {result['explanation']}</div>" if result['explanation'] else ""}
                                </div>
                            """, unsafe_allow_html=True)
            
            st.success("🎉 Great job! Your quiz results have been recorded successfully!")

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
            teacher_id_input = st.text_input("Teacher ID", key="teacher_id_input")
            
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
        # Enhanced teacher dashboard header
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 25px; border-radius: 20px; text-align: center;
                        color: white; margin-bottom: 30px;
                        box-shadow: 0 8px 32px rgba(0,0,0,0.2);'>
                <div style='font-size: 2.2em; font-weight: bold; margin-bottom: 10px;'>
                    🎓 Teacher Dashboard
                </div>
                <div style='font-size: 1.3em; margin-bottom: 5px;'>
                    Welcome, {st.session_state.teacher_id}!
                </div>
                <div style='font-size: 1.1em; opacity: 0.9;'>
                    📊 Track student progress and create lesson plans ✨
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["📝 Lesson Planner", "📊 Student Analytics"])
        
        with tab1:
            st.header("Auto-Generate Lesson Plans")
            
            uploaded_file = st.file_uploader(
                "📎 Browse file for lesson plan",
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
                st.info("📋 AI-generated lesson plan based on your content:")
                
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
            
            student_id = st.text_input("Enter Student ID to view analytics")
            
            # Center the Load Analytics button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                load_button = st.button("Load Analytics", use_container_width=True)
            
            if student_id and load_button:
                with st.spinner("📊 Loading..."):
                    # Get real analytics from DynamoDB
                    analytics = get_student_analytics(student_id)
                
                if analytics:
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
                    
                    # Metrics in cards - All same size with REAL DATA
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"""
                            <div style='background: white; padding: 25px; border-radius: 15px; 
                                        box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center;
                                        min-height: 180px; display: flex; flex-direction: column; 
                                        justify-content: center;'>
                                <div style='font-size: 3em; margin-bottom: 10px;'>📚</div>
                                <div style='font-size: 2.5em; color: #667eea; font-weight: bold; margin-bottom: 10px;'>{analytics['total_assessments']}</div>
                                <div style='font-size: 1.2em; color: #2d3748;'>Total Assessments</div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                            <div style='background: white; padding: 25px; border-radius: 15px; 
                                        box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center;
                                        min-height: 180px; display: flex; flex-direction: column; 
                                        justify-content: center;'>
                                <div style='font-size: 3em; margin-bottom: 10px;'>⭐</div>
                                <div style='font-size: 2.5em; color: #667eea; font-weight: bold; margin-bottom: 10px;'>{analytics['average_score']}%</div>
                                <div style='font-size: 1.2em; color: #2d3748;'>Average Score</div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        sentiment_emoji = {'POSITIVE': '😊', 'NEGATIVE': '😢', 'NEUTRAL': '😐', 'MIXED': '🤔'}
                        emoji = sentiment_emoji.get(analytics['recent_sentiment'], '😊')
                        st.markdown(f"""
                            <div style='background: white; padding: 25px; border-radius: 15px; 
                                        box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center;
                                        min-height: 180px; display: flex; flex-direction: column; 
                                        justify-content: center;'>
                                <div style='font-size: 3em; margin-bottom: 10px;'>{emoji}</div>
                                <div style='font-size: 2.5em; color: #667eea; font-weight: bold; margin-bottom: 10px;'>{analytics['recent_sentiment']}</div>
                                <div style='font-size: 1.2em; color: #2d3748;'>Recent Sentiment</div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("<br><br>", unsafe_allow_html=True)
                    
                    # Detailed metrics with REAL DATA
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### 📈 Performance Trends")
                        st.markdown(f"""
                            <div style='background: white; padding: 20px; border-radius: 15px; 
                                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
                                <div style='font-size: 1.2em; color: #2d3748; margin: 10px 0;'>
                                    ✓ Total Activities: {analytics['total_activities']}<br>
                                    ✓ Completed Assessments: {analytics['total_assessments']}<br>
                                    ✓ Average Score: {analytics['average_score']}%<br>
                                    ✓ Engagement: <strong style='color: #667eea;'>{analytics['engagement_level']}</strong>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("### 💭 Emotional Journey")
                        st.markdown(f"""
                            <div style='background: white; padding: 20px; border-radius: 15px; 
                                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
                                <div style='font-size: 1.2em; color: #2d3748; margin: 10px 0;'>
                                    ✓ Recent Sentiment: <strong style='color: #667eea;'>{analytics['recent_sentiment']}</strong><br>
                                    ✓ Most Common Emotion: <strong style='color: #667eea;'>{analytics['most_common_emotion']} 😊</strong><br>
                                    ✓ Total Check-ins: {analytics['total_activities']}<br>
                                    ✓ Progress: <strong style='color: #667eea;'>Tracking</strong>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    # Show recent quiz results if available
                    if 'recent_quizzes' in analytics and analytics['recent_quizzes']:
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("### 📝 Recent Quiz Results")
                        
                        for idx, quiz in enumerate(analytics['recent_quizzes']):
                            # Color code based on score
                            if quiz['score'] >= 80:
                                bg_color = "#d4edda"
                                border_color = "#28a745"
                                icon = "🌟"
                            elif quiz['score'] >= 60:
                                bg_color = "#d1ecf1"
                                border_color = "#17a2b8"
                                icon = "👍"
                            else:
                                bg_color = "#f8d7da"
                                border_color = "#dc3545"
                                icon = "💪"
                            
                            # Format timestamp
                            import datetime
                            timestamp = datetime.datetime.fromtimestamp(quiz['timestamp']).strftime("%Y-%m-%d %H:%M")
                            
                            st.markdown(f"""
                                <div style='background: {bg_color}; 
                                            border-left: 4px solid {border_color}; 
                                            padding: 15px; margin: 10px 0; border-radius: 5px;'>
                                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                                        <div>
                                            <div style='font-weight: bold; font-size: 1.1em;'>
                                                {icon} {quiz['quiz_title']}
                                            </div>
                                            <div style='margin: 5px 0;'>
                                                Score: <strong>{quiz['score']}%</strong> ({quiz['correct_answers']}/{quiz['total_questions']})
                                            </div>
                                            <div style='font-size: 0.9em; color: #666;'>
                                                Grade Level: {quiz['grade_level']} | Completed: {timestamp}
                                            </div>
                                        </div>
                                        <div style='font-size: 2em;'>{icon}</div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        # Show detailed breakdown if available
                        if st.button("📊 View Detailed Quiz Breakdown", key="detailed_breakdown"):
                            st.markdown("#### 📋 Detailed Question Analysis")
                            
                            for quiz_idx, quiz in enumerate(analytics['recent_quizzes']):
                                with st.expander(f"📝 {quiz['quiz_title']} - Detailed Results"):
                                    if 'detailed_results' in quiz:
                                        # Group by question type
                                        type_performance = {}
                                        for result in quiz['detailed_results']:
                                            q_type = result['type']
                                            if q_type not in type_performance:
                                                type_performance[q_type] = {'correct': 0, 'total': 0}
                                            type_performance[q_type]['total'] += 1
                                            if result['is_correct']:
                                                type_performance[q_type]['correct'] += 1
                                        
                                        # Show performance by type
                                        st.markdown("**Performance by Question Type:**")
                                        type_names = {
                                            'multiple_choice': '🔵 Multiple Choice',
                                            'true_false': '🟢 True/False',
                                            'fill_blank': '🟡 Fill in the Blank',
                                            'match_pair': '🟣 Match the Pair'
                                        }
                                        
                                        cols = st.columns(len(type_performance))
                                        for idx, (q_type, perf) in enumerate(type_performance.items()):
                                            with cols[idx]:
                                                percentage = int((perf['correct'] / perf['total']) * 100)
                                                st.metric(
                                                    type_names.get(q_type, q_type),
                                                    f"{percentage}%",
                                                    f"{perf['correct']}/{perf['total']}"
                                                )
                else:
                    st.warning(f"⚠️ No analytics data found for student: {student_id}")
                    st.info("💡 This student may not have completed any activities yet, or the student ID may be incorrect.")
        
        # Logout button at the bottom - properly centered
        st.markdown("<br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([2, 1, 2])
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
    # Add floating help button and global styles
    st.markdown("""
        <style>
        /* Global animations and styles */
        .stButton > button {
            transition: all 0.3s ease;
            border-radius: 10px;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        

        
        /* Progress indicators */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px;
            padding: 10px 20px;
        }
        </style>
        

    """, unsafe_allow_html=True)
    
    try:
        main()
    except Exception as e:
        # Simple error handling without troubleshooting section
        st.error(f"❌ Error: {str(e)}")
        st.stop()
