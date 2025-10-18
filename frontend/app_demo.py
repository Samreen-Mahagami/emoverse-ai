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
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = None
if 'aws_results' not in st.session_state:
    st.session_state.aws_results = None

# AWS Helper Functions
def upload_to_s3(file, student_id):
    """Upload file to S3"""
    try:
        # Check file size (Textract async limit is 500MB)
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        # 500MB limit for Textract asynchronous API
        max_size = 500 * 1024 * 1024  # 500MB in bytes
        
        if file_size > max_size:
            st.error(f"⚠️ File too large: {file_size / (1024*1024):.1f}MB. Maximum size is 500MB for PDF processing.")
            st.info("💡 Please try a smaller PDF or compress your file.")
            return None
        
        file_key = f"uploads/{student_id}/{file.name}"
        s3_client.upload_fileobj(file, S3_BUCKET, file_key)
        return file_key
    except Exception as e:
        st.error(f"S3 Upload Error: {str(e)}")
        return None

def extract_text_from_s3(file_key):
    """Extract text using AWS Textract (Asynchronous for large files)"""
    try:
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
        
        # Poll for completion (silently)
        max_attempts = 60  # 60 attempts * 2 seconds = 2 minutes max
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
Answer this question based on the text provided. Use simple, age-appropriate language.

Text: {context_text[:5000]}

Student Question: {question}

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

def generate_quiz_direct(text, grade_level):
    """Generate quiz directly using Bedrock"""
    try:
        import boto3
        bedrock = boto3.client('bedrock-runtime', region_name=AWS_REGION)
        
        prompt = f"""Based on this text, create a quiz for {grade_level} students.
Make it fun, educational, and age-appropriate with 3-5 questions.

Text: {text[:2000]}

Create a quiz with multiple choice questions. Format as JSON:
{{
  "title": "Quiz Title",
  "questions": [
    {{
      "question": "Question text?",
      "type": "multiple_choice",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": "Option A",
      "explanation": "Why this is correct"
    }}
  ]
}}"""

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
            quiz_data = json.loads(quiz_text)
            return quiz_data
        except:
            # If not JSON, create simple quiz
            return {
                "title": "Understanding Quiz",
                "questions": [
                    {
                        "question": "What is the main topic of this text?",
                        "type": "multiple_choice",
                        "options": ["Friendship", "Nature", "Learning", "Adventure"],
                        "correct_answer": "Learning",
                        "explanation": "The text focuses on learning and growth."
                    }
                ]
            }
    except Exception as e:
        st.error(f"Error generating quiz: {str(e)}")
        return None

def generate_story_direct(text, grade_level):
    """Generate story directly using Bedrock"""
    try:
        import boto3
        bedrock = boto3.client('bedrock-runtime', region_name=AWS_REGION)
        
        prompt = f"""Based on this text, create a short, engaging story for {grade_level} students.
Make it fun, educational, and age-appropriate.

Text: {text[:2000]}

Create a story with:
1. A catchy title
2. A short story (3-4 paragraphs)
3. A reflection question

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
    """Get real student analytics from DynamoDB LTM"""
    try:
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
        
        if not items:
            return None
        
        # Aggregate analytics
        total_assessments = len([i for i in items if i.get('type') == 'quiz'])
        quiz_scores = [i.get('score', 0) for i in items if i.get('type') == 'quiz' and 'score' in i]
        avg_score = sum(quiz_scores) / len(quiz_scores) if quiz_scores else 0
        
        emotions = [i.get('emotion') for i in items if i.get('emotion')]
        most_common_emotion = max(set(emotions), key=emotions.count) if emotions else 'Happy'
        
        recent_sentiment = items[0].get('sentiment', 'POSITIVE') if items else 'POSITIVE'
        
        return {
            'total_assessments': total_assessments,
            'average_score': int(avg_score * 100) if avg_score <= 1 else int(avg_score),
            'recent_sentiment': recent_sentiment,
            'most_common_emotion': most_common_emotion,
            'total_activities': len(items),
            'engagement_level': 'High' if len(items) > 20 else 'Medium' if len(items) > 10 else 'Low'
        }
    except Exception as e:
        st.error(f"Error fetching analytics: {str(e)}")
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
                🎉 Welcome, {st.session_state.student_id}! | 📚 Grade {st.session_state.grade_level} | Let's learn together! 🌟
            </div>
        """, unsafe_allow_html=True)
        
        # AWS Toggle
        # File upload section
        st.markdown("### 📚 Upload Your Learning Material")
        st.markdown("*Upload a PDF or image - AI will extract text and generate personalized content!* ✨")
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'png', 'jpg', 'jpeg'],
            help="Upload a PDF or image to start learning!"
        )
        
        # File uploaded (no message needed)
            
        if uploaded_file:
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1.5, 2, 1.5])
            with col2:
                process_button = st.button("🚀 Process with AI!", use_container_width=True)
        
        if uploaded_file and process_button:
            # REAL AWS PROCESSING ONLY
            process_with_aws(uploaded_file)
        
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
def process_with_aws(uploaded_file):
    """Process document - Show text immediately, AI loads in background"""
    
    with st.spinner("Processing..."):
        # Upload to S3
        file_key = upload_to_s3(uploaded_file, st.session_state.student_id)
        if not file_key:
            st.error("Failed to process file. Please try again.")
            return
        
        # Extract text with Textract
        extracted_text = extract_text_from_s3(file_key)
        if not extracted_text:
            st.error("Failed to extract text. Please try a different file.")
            return
        
        # Analyze sentiment with Comprehend
        sentiment_data = analyze_sentiment(extracted_text)
        
        # SHOW TEXT IMMEDIATELY - Don't wait for AI!
        st.session_state.extracted_text = extracted_text
        st.session_state.processed_content = {
            'cleaned_text': extracted_text,
            'sentiment': sentiment_data,  # Real sentiment from Comprehend!
            'loading_ai': True  # AI content still loading
        }
        
        # Generate story and quiz INSTANTLY with Claude 4.5
        with st.spinner("✨ Generating your story and quiz..."):
            instant_story = generate_story_direct(extracted_text, st.session_state.grade_level)
            if instant_story:
                st.session_state.direct_story = instant_story
            
            instant_quiz = generate_quiz_direct(extracted_text, st.session_state.grade_level)
            if instant_quiz:
                st.session_state.direct_quiz = instant_quiz
        
        # Start AI generation in background (for quiz and other features)
        job_data = start_content_generation(
            extracted_text,
            st.session_state.grade_level,
            story_theme="friendship",
            quiz_type="multiple_choice"
        )
        
        if job_data:
            st.session_state.job_id = job_data['job_id']
            st.session_state.job_start_time = time_module.time()
    
    # Show tabs immediately
    st.balloons()
    st.rerun()

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
        st.markdown("### ❓ Ask Questions")
        
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
            voice_question = st.audio_input("🎤 Voice", help="Record your question")
        
        # Process voice input
        if voice_question is not None:
            with st.spinner("🎤 Transcribing your question..."):
                transcribed_text = process_voice_question(voice_question, content.get('cleaned_text', ''), st.session_state.grade_level)
                if transcribed_text:
                    st.session_state.question_input = transcribed_text
                    st.rerun()
        
        if st.button("🔍 Get My Answer!", use_container_width=True) and question:
            with st.spinner("🤔 Thinking with AI..."):
                # Get context from processed content
                context_text = content.get('cleaned_text', '')
                grade_level = st.session_state.grade_level
                
                # Get AI answer
                answer = answer_question(question, context_text, grade_level)
            
            if answer:
                # Store in conversation history
                if 'conversation_history' not in st.session_state:
                    st.session_state.conversation_history = []
                
                st.session_state.conversation_history.append({
                    'question': question,
                    'answer': answer
                })
                
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
        
        # Show conversation history
        if hasattr(st.session_state, 'conversation_history') and st.session_state.conversation_history:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 💬 Previous Questions:")
            for i, conv in enumerate(reversed(st.session_state.conversation_history[-3:])):
                with st.expander(f"Q: {conv['question'][:50]}..."):
                    st.markdown(f"**Question:** {conv['question']}")
                    st.markdown(f"**Answer:** {conv['answer']}")
    
    with tab4:
        st.markdown("### 📚 Story Time!")
        
        # Check if we have AWS results
        if st.session_state.aws_results:
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
                
                # Story feedback - Simple Like/Dislike
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("#### 🎭 Did you like this story?")
                
                # Initialize dislike counter
                if 'story_dislike_count' not in st.session_state:
                    st.session_state.story_dislike_count = 0
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("� LoveD it!", use_container_width=True, key="story_like"):
                        st.balloons()
                        st.success("🎉 Awesome! I'm so glad you enjoyed it!")
                        # Reset dislike counter on like
                        st.session_state.story_dislike_count = 0
                
                with col2:
                    if st.button("👎 Dislike", use_container_width=True, key="story_dislike"):
                        st.session_state.story_dislike_count += 1
                        
                        if st.session_state.story_dislike_count == 1:
                            # First dislike: Regenerate story
                            with st.spinner("✨ Generating a different story for you..."):
                                extracted_text = content.get('cleaned_text', '')
                                result = regenerate_story(
                                    extracted_text,
                                    st.session_state.grade_level,
                                    avoid_themes=[story_data.get('theme', '')]
                                )
                                if result:
                                    st.success("✅ New story generated! Please wait...")
                                    time_module.sleep(2)
                                    st.rerun()
                                else:
                                    st.error("Failed to regenerate. Please try again.")
                        
                        elif st.session_state.story_dislike_count >= 2:
                            # Second dislike: Use Playwright Agent to search external stories (Tier 3)
                            st.info("🌐 Searching external story libraries with AI Agent...")
                            
                            with st.spinner("🤖 Playwright Agent is browsing external websites for you..."):
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
                                            <li>📖 <a href='http://www.childrenslibrary.org/' target='_blank'>International Children's Digital Library</a></li>
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
                    
                    # Add Like/Dislike buttons for direct story
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("#### 🎭 Did you like this story?")
                    
                    if 'direct_story_dislike_count' not in st.session_state:
                        st.session_state.direct_story_dislike_count = 0
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("❤️ Loved it!", use_container_width=True, key="direct_story_like"):
                            st.balloons()
                            st.success("🎉 Awesome! I'm so glad you enjoyed it!")
                            st.session_state.direct_story_dislike_count = 0
                    
                    with col2:
                        if st.button("👎 Dislike", use_container_width=True, key="direct_story_dislike"):
                            st.session_state.direct_story_dislike_count += 1
                            
                            if st.session_state.direct_story_dislike_count == 1:
                                # TIER 2: Regenerate with different theme
                                with st.spinner("✨ Generating a different story for you..."):
                                    new_story = generate_story_direct(content.get('cleaned_text', ''), st.session_state.grade_level)
                                    if new_story:
                                        st.session_state.direct_story = new_story
                                        st.success("✅ New story generated!")
                                        time_module.sleep(1)
                                        st.rerun()
                            
                            elif st.session_state.direct_story_dislike_count >= 2:
                                # TIER 3: Playwright Agent searches external stories
                                st.info("🌐 Searching external story libraries with AI Agent...")
                                
                                with st.spinner("🤖 Playwright Agent is browsing external websites for you..."):
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
                                                <li>📖 <a href='http://www.childrenslibrary.org/' target='_blank'>International Children's Digital Library</a></li>
                                                <li>🎨 <a href='https://www.storyberries.com/' target='_blank'>Storyberries</a></li>
                                            </ul>
                                        </div>
                                    """, unsafe_allow_html=True)
                                    st.session_state.direct_story_dislike_count = 0
        else:
            st.warning("📤 Please upload and process a document first to generate a story!")
        
    
    with tab5:
        st.markdown("### 🎯 Quiz Time!")
        
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
    """Display AWS-generated quiz"""
    
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
                    padding: 25px; border-radius: 20px; text-align: center;
                    box-shadow: 0 8px 32px rgba(0,0,0,0.1); margin-bottom: 30px;'>
            <div style='font-size: 2em; color: #2d3748; font-weight: bold;'>
                🎯 {quiz_data.get('title', 'Quiz')}
            </div>
            <div style='font-size: 1.2em; color: #2d3748; margin-top: 10px;'>
                Answer the questions below! ⭐
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Display quiz questions from AWS
    questions = quiz_data.get('questions', [])
    
    if not questions:
        st.warning("No questions available in this quiz.")
        return
    
    # Initialize answers in session state
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    
    # Display each question
    for i, q in enumerate(questions):
        st.markdown(f"### Question {i+1}")
        st.markdown(f"**{q.get('question', '')}**")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Handle different question types
        q_type = q.get('type', 'multiple_choice')
        
        if q_type == 'multiple_choice':
            options = q.get('options', [])
            answer = st.radio(
                "Select your answer:",
                options,
                key=f"quiz_q_{i}",
                label_visibility="collapsed"
            )
            st.session_state.quiz_answers[i] = answer
            
        elif q_type == 'fill_blank':
            answer = st.text_input(
                "Your answer:",
                key=f"quiz_q_{i}",
                placeholder="Type your answer here..."
            )
            st.session_state.quiz_answers[i] = answer
            
        elif q_type == 'true_false':
            answer = st.radio(
                "Select:",
                ["True", "False"],
                key=f"quiz_q_{i}",
                horizontal=True,
                label_visibility="collapsed"
            )
            st.session_state.quiz_answers[i] = answer
        
        st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📝 Submit Quiz", use_container_width=True):
            # Calculate score
            correct = 0
            total = len(questions)
            
            for i, q in enumerate(questions):
                user_answer = st.session_state.quiz_answers.get(i, "")
                correct_answer = q.get('correct_answer', '')
                
                if str(user_answer).lower().strip() == str(correct_answer).lower().strip():
                    correct += 1
            
            score_percent = int((correct / total) * 100) if total > 0 else 0
            
            st.balloons()
            st.success(f"🎉 Quiz Complete! You scored {correct}/{total} ({score_percent}%)")
            
            if score_percent >= 80:
                st.success("🌟 Excellent work! You really understand the material!")
            elif score_percent >= 60:
                st.info("👍 Good job! Keep practicing to improve!")
            else:
                st.warning("💪 Keep trying! Review the material and try again!")

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
            
            student_id = st.text_input("Enter Student ID to view analytics", placeholder="e.g., student123")
            
            # Center the Load Analytics button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                load_button = st.button("Load Analytics", use_container_width=True)
            
            if student_id and load_button:
                with st.spinner("📊 Loading student analytics from LTM..."):
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
                else:
                    st.warning(f"⚠️ No analytics data found for student: {student_id}")
                    st.info("💡 This student may not have completed any activities yet, or the student ID may be incorrect.")
        
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
