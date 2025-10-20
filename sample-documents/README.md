# Sample Documents for Testing EmoVerse AI

This directory contains sample PDF storybooks and educational materials for testing the EmoVerse AI platform.

## 📚 Purpose

These documents are provided to:
- **Test the platform** without needing to find your own materials
- **Demonstrate features** during the video demo
- **Show judges** how the system processes real content
- **Provide examples** of appropriate SEL content for different grade levels

## 📖 Document Types

### Children's Storybooks (PDF)
- Stories with emotional themes (friendship, kindness, courage, etc.)
- Age-appropriate content for grades K-10
- Suitable for testing sentiment analysis and story generation

### Educational Materials
- SEL worksheets
- Emotional intelligence activities
- Social skills content

## 🎯 How to Use These Documents

### For Students:
1. Login to EmoVerse AI as a student
2. Select your grade level (1-10)
3. Upload one of these PDF files
4. Click "Create My Learning Content"
5. Explore all 5 tabs:
   - Read the Text
   - Feel the Emotions
   - Ask Questions
   - Stories
   - Quizzes

### For Teachers:
1. Login as a teacher
2. Upload one of these documents
3. Generate a lesson plan
4. View the structured SEL lesson

## 📝 Testing Scenarios

### Test Emotion Analysis:
- Upload a story with clear emotional themes
- Check "Feel the Emotions" tab for sentiment analysis
- Verify AWS Comprehend correctly identifies emotions

### Test Three-Tier Story System:
1. Upload a document
2. Generate a story (Tier 1)
3. Click "Dislike" to trigger regeneration (Tier 2)
4. Click "Dislike" again to trigger Playwright search (Tier 3)

### Test Quiz Generation:
- Upload any document
- Go to "Quizzes" tab
- Verify 20 questions across 4 types are generated
- Check that questions are based on actual content

### Test Lesson Plan Generation:
- Login as teacher
- Upload a document
- Select grade level and duration
- Verify complete lesson plan is generated

## 🔒 Copyright Notice

**Important:** These sample documents are provided for testing purposes only. 

- If you're using copyrighted materials, ensure you have permission
- For the hackathon demo, use public domain or Creative Commons licensed content
- Recommended sources:
  - **Project Gutenberg** (gutenberg.org) - Public domain books
  - **Storyline Online** (storylineonline.net) - Free educational stories
  - **International Children's Digital Library** (childrenslibrary.org)
  - **Creative Commons** (creativecommons.org) - CC-licensed content

## 📥 Adding Your Own Documents

To add more test documents:

```bash
# Copy your PDF files to this directory
cp /path/to/your/story.pdf sample-documents/

# Add to git
git add sample-documents/story.pdf

# Commit
git commit -m "Add sample document: story.pdf"

# Push to GitHub
git push origin main
```

## 🎬 For Video Demo

When recording your 3-minute demo video:
1. Use 1-2 sample documents from this folder
2. Show the complete student workflow
3. Demonstrate the three-tier story system
4. Show teacher lesson plan generation
5. Display student analytics

## 📊 Recommended Test Documents

### For Grades K-3:
- Simple stories with clear emotions
- 5-10 pages
- Large text, simple vocabulary

### For Grades 4-6:
- Intermediate complexity stories
- 10-20 pages
- More nuanced emotional themes

### For Grades 7-10:
- Complex narratives
- 20+ pages
- Advanced emotional intelligence concepts

## ⚠️ File Size Limits

- **Maximum file size:** 500MB (AWS Textract limit)
- **Recommended size:** Under 50MB for faster processing
- **Processing time:** ~30 seconds for typical documents

## 🚀 Quick Test

```bash
# Navigate to the app
streamlit run frontend/app_demo.py

# Upload a sample document from this folder
# Follow the on-screen instructions
```

---

**Note:** This directory is for demonstration purposes. In production, students and teachers would upload their own educational materials.

**EmoVerse AI - Your AI Universe of Emotional Learning** 💚🌈
