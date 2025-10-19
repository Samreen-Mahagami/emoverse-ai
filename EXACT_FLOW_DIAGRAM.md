# EmoVerse AI - Exact System Flow Diagram
## Based on Actual Code Implementation

### 🔄 Complete User Journey Flow

```mermaid
flowchart TD
    %% Entry Point
    START([🌈 EmoVerse AI Launch]) --> INIT[init_session_state()]
    INIT --> MAIN[main() - User Type Selection]
    
    %% User Type Selection
    MAIN --> CHOICE{Choose User Type}
    CHOICE -->|👨‍🎓| STUDENT[Student Path]
    CHOICE -->|👩‍🏫| TEACHER[Teacher Path]
    
    %% Student Flow
    STUDENT --> LOGIN_CHECK{Student ID exists?}
    LOGIN_CHECK -->|No| STUDENT_LOGIN[Student Login Form]
    STUDENT_LOGIN --> ENTER_ID[Enter Student ID + Grade Level]
    ENTER_ID --> SET_SESSION[Set session_state.student_id & grade_level]
    SET_SESSION --> STUDENT_DASHBOARD
    
    LOGIN_CHECK -->|Yes| STUDENT_DASHBOARD[Student Dashboard]
    STUDENT_DASHBOARD --> FILE_UPLOAD[📎 File Upload Interface]
    
    %% File Processing Flow
    FILE_UPLOAD --> FILE_SELECTED{File Selected?}
    FILE_SELECTED -->|Yes| PROCESS_BTN[✨ Create Learning Content Button]
    PROCESS_BTN --> EXTRACT_IMMEDIATE[extract_text_immediately()]
    
    EXTRACT_IMMEDIATE --> PROCESSING_MSG[🔄 Show Processing Message]
    PROCESSING_MSG --> COMPLETE_EXTRACTION[complete_text_extraction()]
    
    %% Text Extraction Process
    COMPLETE_EXTRACTION --> FILE_TYPE{File Type?}
    FILE_TYPE -->|PDF| PDF_EXTRACT[PyPDF2 Text Extraction]
    FILE_TYPE -->|Image| AWS_TEXTRACT[AWS Textract OCR]
    
    PDF_EXTRACT --> TEXT_SUCCESS{Text Extracted?}
    AWS_TEXTRACT --> TEXT_SUCCESS
    TEXT_SUCCESS -->|Yes| STORE_TEXT[Store extracted_text in session]
    TEXT_SUCCESS -->|No| FALLBACK_TEXT[Generate fallback description]
    FALLBACK_TEXT --> STORE_TEXT
    
    %% AI Content Generation
    STORE_TEXT --> SET_PROCESSED[Set processed_content in session]
    SET_PROCESSED --> SHOW_TABS[Display 5 Tabs Interface]
    SET_PROCESSED --> BACKGROUND_AI[generate_ai_content() - Background]
    
    %% Background AI Processing
    BACKGROUND_AI --> SENTIMENT[analyze_sentiment() - AWS Comprehend]
    BACKGROUND_AI --> STORY_GEN[generate_story_direct() - Bedrock Claude]
    BACKGROUND_AI --> QUIZ_GEN[generate_quiz_direct() - Bedrock Claude]
    
    SENTIMENT --> SENTIMENT_STORE[Store sentiment in session]
    STORY_GEN --> STORY_STORE[Store direct_story in session]
    QUIZ_GEN --> QUIZ_STORE[Store direct_quiz in session]
    
    %% Tab Interface
    SHOW_TABS --> TAB1[📖 Read the Text]
    SHOW_TABS --> TAB2[😊 Feel the Emotions]
    SHOW_TABS --> TAB3[❓ Ask Questions]
    SHOW_TABS --> TAB4[📚 Stories]
    SHOW_TABS --> TAB5[🎯 Quizzes]
    
    %% Tab 1 - Text Display
    TAB1 --> DISPLAY_TEXT[Show extracted text with grade-appropriate messaging]
    
    %% Tab 2 - Emotions
    TAB2 --> EMOTION_CHECK{Sentiment Ready?}
    EMOTION_CHECK -->|Yes| SHOW_SENTIMENT[Display sentiment analysis with emojis & bars]
    EMOTION_CHECK -->|No| LOADING_SENTIMENT[Show loading message]
    
    %% Tab 3 - Q&A
    TAB3 --> QA_INTERFACE[Text Question Input]
    QA_INTERFACE --> QUESTION_ENTERED{Question Entered?}
    QUESTION_ENTERED -->|Yes| ANSWER_GEN[generate_demo_answer() or answer_question()]
    ANSWER_GEN --> SHOW_ANSWER[Display AI answer with styling]

    
    %% Tab 4 - Stories (Multi-Tier System)
    TAB4 --> STORY_CHECK{Story Ready?}
    STORY_CHECK -->|Yes| SHOW_STORY[Display story with title & reflection]
    STORY_CHECK -->|No| STORY_LOADING[Show story generation loading]
    
    SHOW_STORY --> STORY_FEEDBACK{User Feedback}
    STORY_FEEDBACK -->|❤️ Loved it| SAVE_PREFERENCE[Save story preference]
    STORY_FEEDBACK -->|👎 Dislike| DISLIKE_COUNT{Dislike Count}
    
    %% Multi-Tier Story System
    DISLIKE_COUNT -->|First Time| TIER2[Tier 2: regenerate_story()]
    DISLIKE_COUNT -->|Second Time| TIER3[Tier 3: search_external_stories()]
    TIER2 --> REGENERATE[Generate new story with different theme]
    TIER3 --> PLAYWRIGHT[Playwright Agent - External Search]
    PLAYWRIGHT --> EXTERNAL_LINKS[Show external story websites]
    
    %% Tab 5 - Quizzes
    TAB5 --> QUIZ_CHECK{Quiz Ready?}
    QUIZ_CHECK -->|Yes| QUIZ_TABS[Display quiz by type tabs]
    QUIZ_CHECK -->|No| QUIZ_LOADING[Show quiz generation loading]
    
    QUIZ_TABS --> MCQ_TAB[🔵 Multiple Choice]
    QUIZ_TABS --> TF_TAB[🟢 True/False]
    QUIZ_TABS --> FILL_TAB[🟡 Fill in Blank]
    QUIZ_TABS --> MATCH_TAB[🟣 Match the Pair]
    
    MCQ_TAB --> ANSWER_MCQ[Radio button selection]
    TF_TAB --> ANSWER_TF[True/False selection]
    FILL_TAB --> ANSWER_FILL[Text input]
    MATCH_TAB --> ANSWER_MATCH[Dropdown selection]
    
    ANSWER_MCQ --> SUBMIT_QUIZ[Submit Quiz Button]
    ANSWER_TF --> SUBMIT_QUIZ
    ANSWER_FILL --> SUBMIT_QUIZ
    ANSWER_MATCH --> SUBMIT_QUIZ
    
    SUBMIT_QUIZ --> CALCULATE_SCORE[Calculate score & detailed results]
    CALCULATE_SCORE --> STORE_RESULTS[Store in student_quiz_results]
    STORE_RESULTS --> SHOW_RESULTS[Display score with balloons & answer key]
    
    %% Teacher Flow
    TEACHER --> TEACHER_LOGIN{Teacher ID exists?}
    TEACHER_LOGIN -->|No| TEACHER_FORM[Teacher Login Form]
    TEACHER_FORM --> TEACHER_SET[Set teacher_id in session]
    TEACHER_SET --> TEACHER_DASHBOARD
    
    TEACHER_LOGIN -->|Yes| TEACHER_DASHBOARD[Teacher Dashboard]
    TEACHER_DASHBOARD --> TEACHER_TABS[Lesson Planner | Student Analytics]
    
    %% Teacher - Lesson Planner
    TEACHER_TABS --> LESSON_TAB[📝 Lesson Planner]
    LESSON_TAB --> LESSON_UPLOAD[Upload file for lesson plan]
    LESSON_UPLOAD --> LESSON_PARAMS[Select grade level & duration]
    LESSON_PARAMS --> GENERATE_LESSON[Generate Lesson Plan Button]
    GENERATE_LESSON --> LESSON_PLAN[display_lesson_plan() - Auto-generated]
    
    %% Teacher - Analytics
    TEACHER_TABS --> ANALYTICS_TAB[📊 Student Analytics]
    ANALYTICS_TAB --> STUDENT_ID_INPUT[Enter Student ID]
    STUDENT_ID_INPUT --> LOAD_ANALYTICS[get_student_analytics()]
    LOAD_ANALYTICS --> ANALYTICS_DATA{Data Found?}
    ANALYTICS_DATA -->|Yes| SHOW_ANALYTICS[Display metrics, progress, quiz results]
    ANALYTICS_DATA -->|No| NO_DATA[Show no data message]
    
    %% AWS Services Integration
    subgraph AWS_SERVICES[AWS Services]
        S3[(S3 Bucket<br/>sel-platform-uploads)]
        TEXTRACT_SVC[AWS Textract<br/>Document OCR]
        BEDROCK_SVC[AWS Bedrock<br/>Claude Sonnet 4.5]
        COMPREHEND_SVC[AWS Comprehend<br/>Sentiment Analysis]
        TEXT_PROC_SVC[Text Processing<br/>Q&A System]
        DYNAMO[(DynamoDB<br/>Analytics Storage)]
    end
    
    %% AWS Connections
    AWS_TEXTRACT --> TEXTRACT_SVC
    TEXTRACT_SVC --> S3
    STORY_GEN --> BEDROCK_SVC
    QUIZ_GEN --> BEDROCK_SVC
    SENTIMENT --> COMPREHEND_SVC
    ANSWER_GEN --> TEXT_PROC_SVC
    STORE_RESULTS --> DYNAMO
    LOAD_ANALYTICS --> DYNAMO
    
    %% External Services
    subgraph EXTERNAL[External Resources]
        STORYLINE[📚 Storyline Online]
        STORYBERRIES[🎨 Storyberries]
        KIDSKONNECT[🧠 KidsKonnect SEL]
    end
    
    PLAYWRIGHT --> STORYLINE
    PLAYWRIGHT --> STORYBERRIES
    PLAYWRIGHT --> KIDSKONNECT
    
    %% Styling
    classDef userFlow fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef processing fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef ai fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef storage fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef external fill:#f5f5f5,stroke:#424242,stroke-width:2px
    
    class START,MAIN,CHOICE,STUDENT,TEACHER userFlow
    class EXTRACT_IMMEDIATE,COMPLETE_EXTRACTION,BACKGROUND_AI processing
    class STORY_GEN,QUIZ_GEN,SENTIMENT,BEDROCK_SVC,COMPREHEND_SVC ai
    class S3,DYNAMO,STORE_RESULTS storage
    class STORYLINE,STORYBERRIES,KIDSKONNECT external
```

### 📊 Data Flow Summary

#### **1. User Authentication & Session Management**
```
User Launch → init_session_state() → User Type Selection → Login → Set Session Variables
```

#### **2. Document Processing Pipeline**
```
File Upload → extract_text_immediately() → complete_text_extraction() → 
PDF: PyPDF2 | Images: AWS Textract → Store in session_state.extracted_text
```

#### **3. AI Content Generation (Background)**
```
generate_ai_content() → Parallel Processing:
├── analyze_sentiment() → AWS Comprehend → session_state.sentiment
├── generate_story_direct() → AWS Bedrock → session_state.direct_story  
└── generate_quiz_direct() → AWS Bedrock → session_state.direct_quiz
```

#### **4. Multi-Tier Story System**
```
Tier 1: Direct Bedrock Generation (immediate)
Tier 2: regenerate_story() with different themes
Tier 3: search_external_stories() via Playwright Agent
```

#### **5. Interactive Learning Tabs**
```
📖 Text Display → Show extracted content with grade-appropriate messaging
😊 Emotions → Sentiment analysis with visual indicators
❓ Q&A → AI-powered question answering with text input
📚 Stories → Multi-tier story generation with feedback system
🎯 Quizzes → 4 question types with detailed scoring
```

#### **6. Teacher Analytics Pipeline**
```
Quiz Submission → Store in session_state.student_quiz_results → 
get_student_analytics() → Query DynamoDB + Session Data → Display Dashboard
```

### 🔧 Key Technical Implementation Details

- **Session Isolation**: Each user gets unique `session_id` for data separation
- **Error Handling**: Multiple fallback mechanisms for AI service failures  
- **Grade Adaptation**: Content automatically adjusts for K-10 levels
- **Real-time Processing**: Immediate text extraction with background AI generation
- **Multi-modal Input**: PDF (PyPDF2), Images (Textract), Text (Direct Input)
- **Scalable Architecture**: Stateless design with session-based data management

### 🎯 AWS Services Integration Points

| Service | Function | Integration Point |
|---------|----------|-------------------|
| **S3** | File Storage | `upload_to_s3()` |
| **Textract** | OCR Processing | `extract_text_from_s3()` |
| **Bedrock** | AI Generation | `generate_story_direct()`, `generate_quiz_direct()` |
| **Comprehend** | Sentiment Analysis | `analyze_sentiment()` |
| **Text Processing** | Q&A System | `answer_question()` |
| **DynamoDB** | Analytics Storage | `get_student_analytics()` |

This flow diagram represents the exact implementation as coded in your `app_demo.py` file, showing all the actual function calls, session state management, and AWS service integrations.