# 🌈 EmoVerse AI

> *Your AI Universe of Emotional Learning*

**Empowering children's emotional intelligence through personalized AI-driven learning**

A comprehensive serverless platform that combines AWS AI services, Claude Sonnet 4.5, and AgentCore long-term memory to create adaptive Social-Emotional Learning experiences for students and teachers.

[![AWS](https://img.shields.io/badge/AWS-Serverless-orange)](https://aws.amazon.com/)
[![Bedrock](https://img.shields.io/badge/Bedrock-Claude%204.5-blue)](https://aws.amazon.com/bedrock/)
[![Python](https://img.shields.io/badge/Python-3.11+-green)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)](https://streamlit.io/)
[![Hackathon](https://img.shields.io/badge/AWS-AI%20Agent%20Hackathon-yellow)](https://aws.amazon.com/)

> 🚀 **Built for AWS AI Agent Global Hackathon**

**EmoVerse AI** - A comprehensive AI-powered Social-Emotional Learning platform that creates a universe of emotional intelligence for children and educators.

## 🌟 Key Features

### For Students
- 📄 **Smart Document Processing**: Upload PDFs/images, get clean extracted text
- 😊 **Emotion Analysis**: Real-time sentiment and emotion detection
- ❓ **Q&A**: Ask questions and get AI-powered answers
- 📚 **Adaptive Stories**: Grade-specific SEL stories that adapt to preferences
- 🔄 **Smart Fallback**: If you don't like a story, system regenerates or finds external stories
- 🧠 **Personalized Learning**: System remembers your preferences and adapts
- ✅ **Interactive Quizzes**: Auto-generated quizzes to reinforce learning

### For Teachers
- 📝 **Auto Lesson Plans**: Generate 30-60 minute structured lesson plans instantly
- 📊 **Student Analytics**: Track performance, emotional trends, and engagement

### System Intelligence
- 🧠 **Long-Term Memory**: Tracks student preferences, dislikes, and performance
- 🔄 **Three-Tier Story Generation**: Claude → Regenerate → External sources
- 🤖 **AgentCore Integration**: Playwright automation for external story discovery
- 📊 **Analytics Engine**: Rich insights for teachers and parents

## 🏗️ Architecture

```
Student Upload → Textract → Clean → Comprehend → Display
                                         ↓
                                    LTM Storage
                                         ↓
                Q&A ← Claude → Story Generation → Quiz
                                         ↓
                                If Disliked (1st)
                                         ↓
                                Claude Regenerates
                                         ↓
                                If Disliked (2nd)
                                         ↓
                            Playwright → External Stories
```

## 🚀 Quick Start

```bash
# 1. Setup environment
./scripts/setup.sh

# 2. Extract existing Lambda functions
./scripts/extract_lambdas.sh

# 3. Deploy to AWS
cd infrastructure
sam build && sam deploy --guided

# 4. Run frontend
streamlit run frontend/app.py
```

Visit `http://localhost:8501` to access the platform!

## 📋 Prerequisites

- AWS Account with Bedrock access (Claude Sonnet 4.5)
- AWS CLI configured
- SAM CLI installed
- Python 3.11+
- Playwright installed

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [EmoVerse-AI_Architecture_Diagram.png](https://github.com/Samreen-Mahagami/emoverse-ai/blob/426cc20871608bc2a3850661387f1a311e86364d/EmoVerse-AI_Architecture_Diagram.png) | Detailed system architecture |
| [COMPLETE_SYSTEM_FLOW.md](COMPLETE_SYSTEM_FLOW.md) | Complete workflows and system flow |
| [COMPLETE_SERVERLESS_GUIDE.md](COMPLETE_SERVERLESS_GUIDE.md) | Deployment guide with cost breakdown |
| [PROJECT_DESCRIPTION.md](PROJECT_DESCRIPTION.md) | Complete feature documentation |
| [HACKATHON_SUBMISSION.md](HACKATHON_SUBMISSION.md) | Hackathon submission details |

## 🛠️ Technology Stack

**AWS Services**: Lambda, S3, Textract, Comprehend, Bedrock, DynamoDB, API Gateway

**AI/ML**: Claude Sonnet 4.5 (via Bedrock), Playwright for web automation

**Frontend**: Streamlit with Python

**Infrastructure**: AWS SAM (Serverless Application Model)

## 📊 Project Structure

```
sel-platform/
├── backend/
│   ├── agentcore/              # AgentCore components
│   │   ├── memory/             # Long-term memory (LTM)
│   │   └── playwright_agent/   # Web automation
│   ├── shared/                 # Shared utilities
│   │   ├── bedrock_client.py   # Claude interface
│   │   └── orchestrator.py     # Workflow coordinator
│   └── lambdas/                # Lambda functions (extracted from zips)
├── frontend/
│   └── app_demo.py                  # Streamlit interface
├── infrastructure/
│   └── template.yaml           # SAM template
├── scripts/                    # Utility scripts
└── tests/                      # Integration tests
```

## 🎯 How It Works

### Student Workflow

1. **Upload**: Student uploads a PDF or image
2. **Process**: Textract extracts text, Comprehend analyzes emotions
3. **Display**: Clean text and sentiment shown to student
4. **Interact**: Student asks questions, Claude answers
5. **Story**: Student requests a story based on content
   - **Like it?** → Saved to preferences
   - **Dislike?** → Claude regenerates with different approach
   - **Still dislike?** → Playwright finds external stories
6. **Quiz**: Auto-generated quiz to test understanding
7. **Track**: All interactions stored in LTM for personalization

### Teacher Workflow

1. **Upload**: Teacher uploads content
2. **Generate**: System creates 30-60 min lesson plan
   - Warm-up activities
   - Main learning activities
   - Extension exercises
   - Assessment methods
3. **Analytics**: View student performance and emotional trends

## 💡 Key Innovation: Long-Term Memory (LTM)

The LTM system is the brain of the platform:

- **Remembers** student preferences and dislikes
- **Tracks** emotional states over time
- **Records** quiz performance and engagement
- **Provides** rich analytics for teachers
- **Enables** truly personalized learning

Stored in DynamoDB for fast, scalable access.

## 🔄 Three-Tier Story Generation

1. **Tier 1**: Claude generates story based on content
2. **Tier 2**: If disliked, Claude regenerates avoiding previous themes
3. **Tier 3**: If still disliked, Playwright searches external story websites

This ensures every student gets a story they enjoy!

## 💰 Cost Estimate

For 100 active students (5 sessions/month each):

- Lambda: ~$50/month
- Bedrock (Claude): ~$200/month
- Textract: ~$150/month
- Other AWS services: ~$105/month

**Total: ~$505/month** or **~$5/student/month**

## 🔐 Security & Privacy

- ✅ All data encrypted at rest (S3, DynamoDB)
- ✅ IAM roles with least privilege
- ✅ No storage of sensitive PII
- ✅ Age-appropriate content filtering
- ✅ Secure API endpoints

## 🧪 Testing

```bash
# Run integration tests
python tests/test_integration.py

# Test individual components
python -c "from backend.agentcore.memory.ltm_manager import LTMManager; ltm = LTMManager(); print(ltm.get_student_preferences('test'))"
```

## 📈 Monitoring

```bash
# View Lambda logs
sam logs -n StoryGeneratorFunction --tail

# CloudWatch logs
aws logs tail /aws/lambda/sel-story-generator --follow
```


## 📞 Project Links

    GitHub Repository: https://github.com/Samreen-Mahagami/emoverse-ai
    
    Video Demo: https://www.youtube.com/watch?v=wttBJOijmTs
    


## 🤝 Contributing

The project is for children's education. Contributions welcome!

## 📄 License

MIT License - See LICENSE file for details


---

**Made with ❤️ for children's emotional well-being**
