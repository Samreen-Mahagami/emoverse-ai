# EmoVerse AI - Complete System Flow Diagram
## AWS AI Agent Global Hackathon - Exact Step-by-Step Implementation

### 🔄 **COMPLETE USER JOURNEY WITH ALL AWS SERVICES**

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    🌈 EmoVerse AI - Complete System Flow                                    │
│                              Social Emotional Learning Platform with AI Agents                              │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

STEP 1: APPLICATION LAUNCH & INFRASTRUCTURE
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              🏗️ AWS Infrastructure Layer                                │
│                                                                                         │
│  🔧 CloudFormation/CDK Deployment:                                                    │
│  ├─ VPC & Security Groups Configuration                                               │
│  ├─ IAM Roles & Policies Setup                                                        │
│  ├─ S3 Bucket: sel-platform-uploads-089580247707                                     │
│  ├─ DynamoDB Table: sel-ltm-memory-analytics                                         │
│  ├─ API Gateway: lckrtb0j9e.execute-api.us-east-1.amazonaws.com                     │
│  └─ Lambda Functions Deployment                                                       │
│                                                                                         │
│  🔐 Security Configuration:                                                            │
│  ├─ Amazon Cognito User Pools                                                         │
│  ├─ AWS IAM Service Roles                                                             │
│  └─ VPC Network Security                                                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                                      │
                                                      ▼
STEP 2: STREAMLIT APPLICATION STARTUP
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              🌈 Streamlit Frontend Launch                              │
│                                                                                         │
│  • st.set_page_config() - Configure app settings                                      │
│  • Initialize AWS clients: s3_client, textract_client                                 │
│  • Load custom CSS styling                                                            │
│  • Call main() function                                                               │
│  • Execute init_session_state() - Create unique session_id                           │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                                      │
                                                      ▼
STEP 3: USER AUTHENTICATION & TYPE SELECTION
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                            👨‍🎓👩‍🏫 User Interface & Authentication                        │
│                                                                                         │
│  User Opens Browser ──▶ EmoVerse AI Landing Page                                      │
│                                                                                         │
│  Choose User Type:                                                                     │
│  ├─ 👨‍🎓 Student Button ──▶ st.session_state.user_type = "student"                    │
│  └─ 👩‍🏫 Teacher Button ──▶ st.session_state.user_type = "teacher"                    │
│                                                                                         │
│  Student Path: Enter Student ID + Grade Level (K-10)                                  │
│  Teacher Path: Enter Teacher ID                                                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                                      │
                                                      ▼
STEP 4: STUDENT DOCUMENT UPLOAD INTERFACE
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              📤 File Upload Interface                                  │
│                                                                                         │
│  • st.file_uploader() - Accept PDF, PNG, JPG, JPEG (Max 500MB)                       │
│  • File size validation and user warnings                                             │
│  • Progress indicators for large files                                                │
│  • "✨ Create My Learning Content!" button                                            │
│                                                                                         │
│  File Size Handling:                                                                  │
│  ├─ 50MB+: "Processing ALL pages with batch optimization (~20-30 seconds)"           │
│  ├─ 25MB+: "Processing ALL pages efficiently (~15-25 seconds)"                       │
│  └─ <25MB: "Processing ALL pages for complete content (~10-15 seconds)"              │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                                      │
                                                      ▼
STEP 5: FILE PROCESSING INITIATION
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          🔄 extract_text_immediately() Function                        │
│                                                                                         │
│  • st.session_state.processing_file = True                                            │
│  • Display processing message with file size info                                     │
│  • st.rerun() to show immediate feedback                                              │
│  • Call complete_text_extraction(uploaded_file)                                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                                      │
                                                      ▼
STEP 6: AWS S3 UPLOAD & STORAGE
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                📦 Amazon S3 Storage                                    │
│                                                                                         │
│  Function: upload_to_s3(file, student_id)                                             │
│  • Bucket: sel-platform-uploads-089580247707                                          │
│  • Key Format: uploads/{student_id}/{session_id}_{timestamp}_{filename}               │
│  • File size validation (500MB limit for Textract)                                   │
│  • Retry logic (3 attempts) for reliable upload                                       │
│  • IAM permissions validation                                                         │
│                                                                                         │
│  Security Features:                                                                    │
│  ├─ Session-based file isolation                                                      │
│  ├─ Automatic lifecycle management                                                    │
│  └─ Secure access with IAM roles                                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                                      │
                                                      ▼
STEP 7: TEXT EXTRACTION PROCESSING
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                            📄 Text Extraction Engine                                   │
│                                                                                         │
│  PDF Processing (Priority Method):                                                     │
│  ├─ Primary: pdfplumber (faster extraction)                                           │
│  └─ Fallback: PyPDF2 (reliable backup)                                               │
│                                                                                         │
│  Image Processing:                                                                     │
│  └─ AWS Textract Asynchronous OCR                                                     │
│                                                                                         │
│  Children's Content Optimization:                                                      │
│  ├─ Process ALL pages (no page limits)                                               │
│  ├─ Maintain page numbering for navigation                                           │
│  ├─ Batch processing for large files (5-10 pages per batch)                          │
│  ├─ Real-time progress updates                                                       │
│  └─ Error resilience (skip problematic pages, continue processing)                   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                                      │
                                                      ▼
STEP 8: AWS TEXTRACT OCR (For Images)
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              📄 Amazon Textract Service                                │
│                                                                                         │
│  Function: extract_text_from_s3(file_key)                                             │
│  • start_document_text_detection() - Initiate async job                               │
│  • Job polling with progress indicators (max 30 attempts)                             │
│  • get_document_text_detection() - Retrieve results                                   │
│  • Extract text from all pages with pagination support                                │
│  • Handle SUCCEEDED/FAILED job statuses                                               │
│                                                                                         │
│  Output Processing:                                                                    │
│  ├─ Extract LINE blocks for readable text                                             │
│  ├─ Handle multi-page documents with NextToken                                        │
│  └─ Maintain document structure and formatting                                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                                      │
                                                      ▼
STEP 9: TEXT STORAGE & DISPLAY
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          🌈 Streamlit Text Display Interface                           │
│                                                                                         │
│  • Store extracted text in st.session_state.extracted_text                           │
│  • Create st.session_state.processed_content dictionary                               │
│  • st.session_state.processing_file = False                                          │
│  • Call display_processed_content() to show 5-tab interface                          │
│                                                                                         │
│  Tab 1: "📖 Read the Text"                                                           │
│  ├─ Display complete extracted content                                               │
│  ├─ Grade-appropriate messaging (K-10)                                               │
│  └─ Maintain page structure for children's books                                     │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                                      │
                                                      ▼
STEP 10: BACKGROUND AI PROCESSING INITIATION
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          🤖 generate_ai_content() Background Process                   │
│                                                                                         │
│  Parallel AI Processing (3 simultaneous operations):                                  │
│  ├─ Sentiment Analysis ──▶ analyze_sentiment()                                       │
│  ├─ Story Generation ──▶ generate_story_direct()                                     │
│  └─ Quiz Generation ──▶ generate_quiz_direct()                                       │
│                                                                                         │
│  Error Handling & Retry Logic:                                                        │
│  ├─ Max 3 retries per operation                                                      │
│  ├─ Staggered delays to prevent API throttling                                       │
│  └─ Graceful fallbacks for service failures                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                                      │
                                                      ▼
STEP 11: AWS COMPREHEND SENTIMENT ANALYSIS
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                            💭 Amazon Comprehend Service                                │
│                                                                                         │
│  Function: analyze_sentiment(text)                                                    │
│  • Input: First 5000 bytes of extracted text                                         │
│  • API Call: comprehend.detect_sentiment(Text=content, LanguageCode='en')            │
│  • Output: Sentiment + Confidence Scores                                             │
│    ├─ POSITIVE/NEGATIVE/NEUTRAL/MIXED                                                │
│    └─ Confidence percentages for each emotion                                        │
│                                                                                         │
│  Storage: st.session_state.processed_content['sentiment']                            │
│                                                                                         │
│  Display in Tab 2: "😊 Feel the Emotions"                                           │
│  ├─ Large emoji display based on dominant sentiment                                  │
│  ├─ Animated progress bars for each emotion type                                     │
│  └─ Color-coded confidence scores                                                    │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                                      │
                                                      ▼
STEP 12: AWS BEDROCK STORY GENERATION
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          🧠 Amazon Bedrock - Story Generation                          │
│                                                                                         │
│  Function: generate_story_direct(text, grade_level)                                   │
│  • Model: Claude Sonnet 4.5 (arn:aws:bedrock:us-east-1:089580247707:inference-profile)│
│  • Input: Extracted text + Grade level + Story requirements                          │
│  • Grade-adaptive prompting (K-10 vocabulary and themes)                             │
│  • Output: JSON with title, story, reflection_question                               │
│                                                                                         │
│  Multi-Tier Story System:                                                             │
│  ├─ Tier 1: Direct Bedrock generation (immediate)                                    │
│  ├─ Tier 2: Regeneration with different themes (on dislike)                          │
│  └─ Tier 3: External content discovery via Playwright Agent                          │
│                                                                                         │
│  Storage: st.session_state.direct_story                                              │
│                                                                                         │
│  AgentCore Integration:                                                                │
│  ├─ Long-term memory for user preferences                                            │
│  ├─ Session management and personalization                                           │
│  └─ Performance tracking and optimization                                             │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                                      │
                                                      ▼
STEP 13: AWS BEDROCK QUIZ GENERATION
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           🎯 Amazon Bedrock - Quiz Generation                          │
│                                                                                         │
│  Function: generate_quiz_direct(text, grade_level)                                    │
│  • Model: Claude Sonnet 4.5 (same inference profile)                                │
│  • Input: Extracted text + Grade level + Quiz specifications                         │
│  • Output: 20 questions total (5 each type):                                         │
│    ├─ 5 Multiple Choice Questions                                                     │
│    ├─ 5 True/False Questions                                                          │
│    ├─ 5 Fill in the Blank Questions                                                  │
│    └─ 5 Match the Pair Questions                                                     │
│                                                                                         │
│  Grade-Level Adaptation:                                                              │
│  ├─ K-3: Simple vocabulary, basic concepts                                           │
│  ├─ 4-6: Intermediate complexity, detailed explanations                              │
│  └─ 7-10: Advanced analysis, critical thinking                                       │
│                                                                                         │
│  Storage: st.session_state.direct_quiz                                               │
│  Fallback: create_content_specific_quiz() for service failures                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                                      │
                                                      ▼
STEP 14: VOICE INPUT PROCESSING (Optional User Action)
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          🎤 Voice Question Processing Pipeline                          │
│                                                                                         │
│  Tab 3: "❓ Ask Questions" Interface                                                  │
│  • Text input field for typed questions                                              │
│  • 🎤 Voice recording button                                                         │
│                                                                                         │
│  Voice Processing Flow:                                                                │
│  ├─ streamlit-audio-recorder component                                               │
│  ├─ Browser-based audio recording (WAV format)                                       │
│  ├─ Upload audio to S3 temporary storage                                             │
│  └─ AWS Transcribe speech-to-text conversion                                         │
│                                                                                         │
│  Function: transcribe_audio_aws(audio_bytes)                                          │
│  • Create unique transcription job                                                   │
│  • start_transcription_job() with S3 audio file                                     │
│  • Poll for completion with progress indicators                                      │
│  • Extract transcribed text and populate input field                                │
│                                                                                         │
│  Fallback: Demo voice questions for testing                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                                      │
                                                      ▼
STEP 15: AI-POWERED QUESTION ANSWERING
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        🧠 Content-Aware Question Answering                             │
│                                                                                         │
│  Question Processing Pipeline:                                                         │
│  ├─ Primary: answer_question() using Bedrock Claude                                  │
│  ├─ Secondary: generate_content_aware_answer() using document context                │
│  └─ Fallback: generate_demo_answer() with keyword matching                           │
│                                                                                         │
│  Function: answer_question(question, context_text, grade_level)                       │
│  • Model: Claude Sonnet 4.5                                                          │
│  • Input: User question + Document context + Grade level                             │
│  • Grade-appropriate response generation                                              │
│  • Context-aware answers using actual uploaded content                               │
│                                                                                         │
│  Enhanced Features:                                                                    │
│  ├─ Conversation history storage                                                     │
│  ├─ Real-time answer display with styling                                           │
│  └─ Balloons animation for successful answers                                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                                      │
                                                      ▼
STEP 16: INTERACTIVE STORY DISPLAY & FEEDBACK
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        📚 Multi-Tier Story System with AgentCore                       │
│                                                                                         │
│  Tab 4: "📚 Stories" Interface                                                        │
│  • Display generated story with title and reflection question                         │
│  • User feedback system: ❤️ Loved it! / 👎 Dislike                                  │
│                                                                                         │
│  Multi-Tier Response System:                                                          │
│                                                                                         │
│  TIER 1: Direct Bedrock Generation                                                    │
│  └─ Immediate story from generate_story_direct()                                      │
│                                                                                         │
│  TIER 2: Smart Regeneration (First Dislike)                                          │
│  ├─ Call generate_story_direct() with different parameters                           │
│  ├─ Avoid previous themes and approaches                                             │
│  └─ st.rerun() to refresh interface                                                  │
│                                                                                         │
│  TIER 3: External Content Discovery (Second Dislike)                                 │
│  ├─ Function: search_external_stories() via Playwright Agent                         │
│  ├─ Automated web scraping of educational story websites                             │
│  ├─ Target sites: storylineonline.net, storyberries.com, kidskonnect.com           │
│  └─ Display curated external story links                                             │
│                                                                                         │
│  AgentCore Memory:                                                                     │
│  ├─ Store user preferences in st.session_state.story_preferences                    │
│  ├─ Track dislike patterns for improvement                                           │
│  └─ Personalization for future content generation                                    │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                                      │
                                                      ▼
STEP 17: INTERACTIVE QUIZ SYSTEM
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          🎯 Comprehensive Quiz Interface                               │
│                                                                                         │
│  Tab 5: "🎯 Quizzes" - Organized by Question Type                                     │
│                                                                                         │
│  Quiz Tabs:                                                                           │
│  ├─ 🔵 Multiple Choice (5 questions with radio buttons)                              │
│  ├─ 🟢 True/False (5 questions with binary selection)                                │
│  ├─ 🟡 Fill in the Blank (5 questions with text input)                              │
│  └─ 🟣 Match the Pair (5 questions with dropdown selection)                          │
│                                                                                         │
│  Interactive Features:                                                                 │
│  ├─ Real-time progress tracking per question type                                    │
│  ├─ Individual tab submission buttons                                                │
│  ├─ Overall "Submit All Quizzes" button                                             │
│  └─ Immediate feedback with balloons animation                                       │
│                                                                                         │
│  Scoring System:                                                                       │
│  ├─ Calculate percentage scores per question type                                    │
│  ├─ Overall performance metrics                                                      │
│  ├─ Detailed answer key with explanations                                           │
│  └─ Color-coded results (green=correct, red=incorrect)                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                                      │
                                                      ▼
STEP 18: ANALYTICS & LONG-TERM MEMORY STORAGE
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        🗄️ DynamoDB Analytics & AgentCore LTM                           │
│                                                                                         │
│  Table: sel-ltm-memory-analytics                                                      │
│                                                                                         │
│  Quiz Results Storage:                                                                 │
│  ├─ Student ID, Session ID, Timestamp                                                │
│  ├─ Quiz title, Score percentage, Correct/Total answers                              │
│  ├─ Detailed question-by-question results                                           │
│  ├─ Grade level and difficulty metrics                                              │
│  └─ Emotional journey and sentiment tracking                                         │
│                                                                                         │
│  Session State Storage:                                                                │
│  ├─ st.session_state.student_quiz_results (immediate access)                        │
│  ├─ st.session_state.story_preferences (user feedback)                              │
│  └─ st.session_state.conversation_history (Q&A tracking)                            │
│                                                                                         │
│  AgentCore Long-Term Memory:                                                           │
│  ├─ User learning patterns and preferences                                           │
│  ├─ Performance trends over time                                                     │
│  ├─ Personalization data for future sessions                                        │
│  └─ Cross-session continuity and adaptation                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                                      │
                                                      ▼
STEP 19: TEACHER ANALYTICS DASHBOARD
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          👩‍🏫 Teacher Interface & Analytics                              │
│                                                                                         │
│  Function: get_student_analytics(student_id)                                          │
│  • Query DynamoDB for student performance data                                       │
│  • Combine with session state for real-time data                                     │
│  • Generate comprehensive analytics dashboard                                         │
│                                                                                         │
│  Analytics Metrics:                                                                    │
│  ├─ Total assessments completed                                                      │
│  ├─ Average quiz scores and performance trends                                       │
│  ├─ Recent sentiment analysis (emotional journey)                                    │
│  ├─ Most common emotions and engagement levels                                       │
│  ├─ Recent quiz results with detailed breakdowns                                     │
│  └─ Learning progress and improvement areas                                           │
│                                                                                         │
│  Lesson Plan Generation:                                                               │
│  ├─ Upload educational content                                                       │
│  ├─ Select grade level and duration                                                  │
│  ├─ Auto-generate structured lesson plans                                           │
│  ├─ Include SEL competencies and learning objectives                                 │
│  └─ Downloadable lesson plan documents                                               │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                                      │
                                                      ▼
STEP 20: MONITORING & OBSERVABILITY
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        📊 AgentCore Observability & Monitoring                         │
│                                                                                         │
│  CloudWatch Integration:                                                               │
│  ├─ Application logs and error tracking                                              │
│  ├─ Performance metrics and latency monitoring                                       │
│  ├─ AWS service usage and cost optimization                                          │
│  └─ User engagement and system health metrics                                        │
│                                                                                         │
│  AgentCore Observability:                                                             │
│  ├─ AI agent performance tracking                                                    │
│  ├─ Multi-tier system effectiveness metrics                                          │
│  ├─ User satisfaction and content quality scores                                     │
│  └─ Learning outcome improvements over time                                           │
│                                                                                         │
│  Real-time Monitoring:                                                                │
│  ├─ System performance and response times                                            │
│  ├─ Error rates and service availability                                             │
│  ├─ User activity patterns and peak usage                                            │
│  └─ Content generation success rates                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              🎯 COMPLETE AWS SERVICES INTEGRATION                       │
│                                                                                         │
│  Core Services:                                                                        │
│  ├─ 📦 S3: Document storage and temporary file management                             │
│  ├─ 📄 Textract: OCR processing for images and complex PDFs                          │
│  ├─ 🧠 Bedrock: AI content generation (Claude Sonnet 4.5)                           │
│  ├─ 💭 Comprehend: Sentiment analysis and emotional tone detection                   │
│  ├─ 🎤 Transcribe: Voice-to-text conversion for questions                            │
│  ├─ 🗄️ DynamoDB: Analytics storage and long-term memory                             │
│  ├─ 🚪 API Gateway: RESTful API endpoints                                            │
│  └─ ⚡ Lambda: Serverless orchestration functions                                     │
│                                                                                         │
│  AgentCore Services:                                                                   │
│  ├─ 🤖 AgentCore Runtime: Multi-tier intelligent content generation                  │
│  ├─ 🧠 AgentCore Memory: Session management and personalization                      │
│  ├─ 👁️ AgentCore Observability: Performance tracking and optimization               │
│  └─ 🌐 Playwright Agent: External content discovery and web automation               │
│                                                                                         │
│  Security & Infrastructure:                                                            │
│  ├─ 🔐 Cognito: User authentication and session management                           │
│  ├─ 🛡️ IAM: Fine-grained access control and service permissions                     │
│  ├─ 🔒 VPC: Network security and isolation                                           │
│  ├─ 🏗️ CloudFormation: Infrastructure as code deployment                            │
│  └─ 📊 CloudWatch: Monitoring, logging, and alerting                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 📊 **EXACT TECHNICAL IMPLEMENTATION DETAILS**

#### **Function Call Flow:**
```
main() → init_session_state() → student_interface() → 
extract_text_immediately() → complete_text_extraction() → 
generate_ai_content() → [analyze_sentiment(), generate_story_direct(), generate_quiz_direct()] → 
display_processed_content() → [Tab interfaces with real-time updates]
```

#### **AWS Service Integration Points:**
```
S3: upload_to_s3() → extract_text_from_s3()
Textract: start_document_text_detection() → get_document_text_detection()
Bedrock: invoke_model() with Claude Sonnet 4.5
Comprehend: detect_sentiment() with confidence scores
Transcribe: start_transcription_job() → get_transcription_job()
DynamoDB: Query/Put operations for analytics storage
```

#### **Session State Management:**
```
st.session_state.session_id (unique user identifier)
st.session_state.extracted_text (document content)
st.session_state.processed_content (AI processing results)
st.session_state.direct_story (generated stories)
st.session_state.direct_quiz (generated quizzes)
st.session_state.student_quiz_results (performance data)
```

#### **Multi-Tier AgentCore System:**
```
Tier 1: Direct Bedrock → Immediate content generation
Tier 2: Smart Regeneration → Alternative approaches on user feedback
Tier 3: Playwright Agent → External content discovery and web scraping
```

This comprehensive flow diagram shows every step, function call, AWS service integration, and data flow in your EmoVerse AI system, exactly as implemented in your code.