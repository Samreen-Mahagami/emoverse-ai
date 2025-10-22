# EmoVerse AI - Requirements Gathering Questionnaire
## AWS AI Agent Global Hackathon 2025

**Social-Emotional Learning Platform**

| Version | Author | Description | Date |
|---------|--------|-------------|------|
| 1.1 | Samreen Mahagami | Requirements Gathering | 17-09-2025 |

---

## 1. Project Overview and Goals

**1. What is the primary purpose of this AI solution?**  
Automating Social-Emotional Learning (SEL) lesson plans from documents/images to support mental health education for students

**2. What are the key objectives and expected outcomes?**  
Generate Quizzes, Adapt Scenarios, Fetch alternatives if disliked

**3. How does this project align with broader organizational or educational goals?**  
Improving SEL curriculum efficiency and providing accessible mental health learning support for students

**4. What problems does this solution aim to solve?**  
Manual content creation for SEL is time-consuming, and students need accessible mental health learning resources

**5. What is the desired timeline for development, testing, and deployment?**  
Completed: Full production platform with 5 student tabs, 2 teacher tabs deployed

**6. How could this problem be solved manually without AI, and why is AI preferred?**  
Manual: Teachers spend 2-3 hours creating each lesson plan  
AI Advantage: Instant personalization, 24/7 availability, scales to thousands of students

**7. What success metrics will define the project's effectiveness?**  
Accuracy of OCR extraction, user satisfaction with generated content

**8. What is the scope?**  
Full-scale production application currently deployed

**9. Are there any constraints on budget, resources, or technology stack?**  
Must use AWS services, Budget: Cost Optimized, Speed: Results as quickly as possible

**10. What inspired this project?**  
The need for accessible mental health learning resources and gaps in current SEL educational tools for students

---

## 2. Stakeholders and Users

**11. Who are the primary stakeholders?**  
Educators, School administrators, Developers, Students/Parents

**12. What are the roles, titles, and responsibilities of key users?**  
Teachers uploading PDFs, Admins Reviewing Outputs

**13. Who will be the end-users?**  
Grade 1-10 students learning about mental health and emotions through SEL content, teachers creating lesson plans

**14. What is the expected number of users and usage frequency?**  
Daily lesson planning for 100+ educators

**15. What levels of expertise do users have?**  
Tech-savvy vs. non-technical educators

**16. Are there accessibility needs?**  
Support for diverse languages, disabilities in SEL contexts

**17. How will stakeholders be involved in the requirements process?**  
Interviews, workshops

**18. What pain points do users currently face with SEL content?**  
Outdated materials, lack of customization, limited access to mental health learning resources

**19. Who will approve the final requirements and deliverables?**  
Project lead, educational advisors

**20. Are there external parties involved?**  
SEL experts, AWS consultants

---

## 3. Functional Requirements

**21. What core features are needed?**  
PDF upload and OCR scanning with Amazon Textract

**22. How should the system handle content extraction?**  
Text, images, tables from SEL PDFs

**23. What LLM tasks are required?**  
Summarize SEL themes related to mental health, Generate lesson plans, Create quizzes, Generate stories about emotions and coping strategies

**24. Describe the workflow for generating outputs?**  
Input PDF → OCR → LLM analysis → lesson plan/quiz output

**25. How should scenario adaptation work?**  
Change ocean pollution to friendship themes in SEL stories

**26. What triggers alternative content fetching?**  
User feedback like "not satisfied"

**27. Which external sources should be integrated for alternatives?**  
CASEL.org, Edutopia.org for SEL resources

**28. What output formats are needed?**  
Downloadable PDFs, interactive quizzes, web/app interfaces

**29. How should the system handle user interactions?**  
Confirmation for Image generation, Feedback Loops

**30. Are there customization options?**  
Grade level, SEL competency focus like self-awareness

**31. What integration points are required?**  
With AWS S3 for storage, API Gateway for access

**32. How should quizzes be structured?**  
Multiple-choice, Matching, with Answers and Scoring

**33. What error-handling features are needed?**  
Poor OCR fallback, LLM hallucination checks

**34. Should the system support multi-user collaboration?**  
Shared lesson plans

**35. How will the system evolve?**  
Adding new SEL topics or LLM models

---

## 4. Non-Functional Requirements

**36. What performance expectations exist?**  
OCR processing time under 10 seconds per page

**37. What scalability needs are there?**  
Handle 1,000 PDFs/day

**38. What reliability and uptime requirements?**  
99.9% availability

**39. What security measures are needed?**  
Data encryption, IAM roles for AWS access

**40. How should privacy be handled?**  
Anonymize SEL student data, comply with COPPA/FERPA

**41. What usability standards?**  
Intuitive UI for educators, mobile compatibility

**42. What maintainability requirements?**  
Easy to update LLM prompts or models in Bedrock

**43. Are there cost constraints?**  
Limits on Bedrock token usage or Textract pricing

**44. What logging and monitoring needs?**  
Track LLM outputs for bias

**45. How should the system handle edge cases?**  
Blurry PDFs, controversial SEL topics

---

## 5. Data and Content Handling

**46. What types of input data will be used?**  
SEL PDFs like "Grade.pdf"

**47. What data sources are available?**  
Internal PDFs, external websites for SEL alternatives

**48. How should data quality be ensured?**  
Validation after OCR extraction

**49. What data storage requirements?**  
S3 buckets for PDFs and outputs

**50. Are there data governance needs?**  
Retention policies for SEL content

**51. How will the system handle sensitive SEL topics?**  
Emotions like fear or anger

**52. What preprocessing steps for data?**  
Cleaning OCR text before LLM input

**53. Should the system support real-time data fetching?**  
Web scraping for updated SEL resources

**54. What data volume expectations?**  
PDFs with 10-50 pages each

**55. How to manage data biases?**  
Ensure diverse SEL examples in generated content

---

## 6. AI/LLM and OCR Specific Requirements

**56. Which AWS Bedrock models are going to be used?**  
Claude Sonnet 4.5 for creative SEL content generation

**57. What prompt engineering guidelines?**  
For lesson plans aligned with CASEL competencies

**58. How to evaluate LLM outputs?**  
Accuracy in naming emotions, relevance to SEL

**59. What OCR accuracy thresholds?**  
95% for text extraction from illustrated PDFs

**60. How to handle LLM limitations?**  
Guardrails for ethical SEL content, no harmful scenarios

**61. Should fine-tuning of models be supported?**  
Custom SEL datasets

**62. What testing for AI?**  
Unit tests for quizzes, human evaluation for lesson plans

**63. How to incorporate user feedback into AI improvements?**  
Retrain on disliked outputs

**64. What ethical AI considerations?**  
Bias in SEL emotion representations for diverse cultures

**65. How to optimize for cost and latency?**  
Bedrock's latency-optimized inference

---

## 7. Educational and SEL Specific Requirements

**66. How does the solution align with SEL frameworks?**  
CASEL's 5 competencies: self-awareness, etc.

**67. What pedagogical impact is expected?**  
Enhance emotional intelligence and mental health awareness through personalized stories, quizzes, and interactive learning

**68. How to ensure age-appropriateness?**  
Grade 1-10 SEL content with age-appropriate language for mental health topics and emotional learning

**69. What assessment tools for SEL outcomes?**  
Track student engagement with generated materials, quiz scores on emotional understanding, mental health learning progress

**70. How to promote empathy and responsibility?**  
In adapted scenarios like environmental themes

**71. Are there inclusivity requirements?**  
Diverse representations in SEL stories

**72. What training for users?**  
How educators use the tool for SEL classrooms

**73. How to measure educational effectiveness?**  
Pre/Post quizzes on emotion naming, understanding mental health concepts, and applying coping strategies

**74. Should the tool support SEL-specific features?**  
Emotion recognition through sentiment analysis, personalized stories about mental health topics, interactive quizzes on emotional learning

**75. What risks in SEL AI?**  
Oversimplifying complex emotions and mental health topics, ensuring age-appropriate content for sensitive subjects

---

## 8. Integration, Deployment, and Maintenance

**76. What existing systems to integrate with?**  
Learning management systems like Google Classroom

**77. What deployment environment?**  
AWS Lambda for serverless, Streamlit for frontend

**78. What APIs or tools are needed?**  
For web search in alternative fetching

**79. How to handle updates?**  
New AWS Bedrock models or SEL guidelines

**80. What support and maintenance plan?**  
Ongoing monitoring for AI drift

---

## 9. Risks, Compliance, and Feedback

**81. What potential risks?**  
Inaccurate LLM-generated SEL advice

**82. What compliance requirements?**  
GDPR for data, educational standards

**83. How to gather ongoing feedback?**  
User surveys post-deployment

**84. What contingency plans?**  
If Bedrock APIs change

**85. Are there ethical review processes?**  
For AI in education

---

## Current Features Implemented

**Platform Purpose:** Mental health learning platform for students through Social-Emotional Learning (SEL)

### For Students (5 Tabs):
1. **Read the Text** - AWS Textract extracts text from PDFs/images
2. **Feel the Emotions** - AWS Comprehend analyzes sentiment to help students understand emotional context
3. **Ask Questions** - AI-powered Q&A with Claude Sonnet 4.5 for mental health and emotional learning
4. **Stories** - Three-tier system generates personalized stories about emotions, coping strategies, and mental health topics (Bedrock → Regenerate → Playwright search)
5. **Quizzes** - 20 questions (MCQ, True/False, Fill-in-Blank, Match-Pair) on emotional understanding and mental health concepts

### For Teachers (2 Tabs):
1. **Lesson Planner** - Auto-generates 30-60 minute SEL lesson plans focused on mental health education
2. **Student Analytics** - Real-time performance tracking on emotional learning progress

### AWS Services Used:
- AWS Bedrock (Claude Sonnet 4.5)
- AWS Textract (OCR)
- AWS Comprehend (Sentiment Analysis)
- AWS Lambda (Serverless functions)
- Amazon S3 (Storage)
- Amazon DynamoDB (Long-term memory)
- CloudFormation/SAM (Infrastructure as Code)

---

**Document Version:** 1.1  
**Author:** Samreen Mahagami  
**Project:** EmoVerse AI - Your AI Universe of Emotional Learning  
**Hackathon:** AWS AI Agent Global Hackathon 2025
