"""
Content Orchestrator - Coordinates the entire SEL platform workflow
"""
import boto3
import hashlib
from typing import Dict, Optional
from .bedrock_client import BedrockClient
from backend.agentcore.memory.ltm_manager import LTMManager, PerformanceRecord
from backend.agentcore.playwright_agent.story_browser import StoryBrowserAgent


class ContentOrchestrator:
    """Orchestrates the complete student and teacher workflows"""
    
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.textract = boto3.client('textract')
        self.comprehend = boto3.client('comprehend')
        self.transcribe = boto3.client('transcribe')
        self.sns = boto3.client('sns')
        self.sqs = boto3.client('sqs')
        
        self.bedrock_client = BedrockClient()
        self.ltm_manager = LTMManager()
        self.story_browser = StoryBrowserAgent()
    
    def process_student_upload(
        self, 
        file_path: str, 
        student_id: str,
        grade_level: int,
        bucket: str
    ) -> Dict:
        """Complete student workflow from upload to story generation"""
        
        result = {
            'student_id': student_id,
            'status': 'processing',
            'steps': {}
        }
        
        # Step 1: Upload to S3
        s3_key = f"uploads/{student_id}/{file_path.split('/')[-1]}"
        result['steps']['upload'] = {'s3_key': s3_key}
        
        # Step 2: Extract text with Textract
        extracted_text = self._extract_text(bucket, s3_key)
        result['steps']['extraction'] = {'text_length': len(extracted_text)}
        
        # Step 3: Clean text
        cleaned_text = self._clean_text(extracted_text)
        result['steps']['cleaning'] = {'cleaned_length': len(cleaned_text)}
        
        # Step 4: Analyze emotions with Comprehend
        sentiment_data = self._analyze_sentiment(cleaned_text)
        result['steps']['sentiment'] = sentiment_data
        
        # Update LTM with emotional state
        self.ltm_manager.update_emotional_state(student_id, sentiment_data)
        
        # Step 5: Display clean text (returned to frontend)
        result['cleaned_text'] = cleaned_text
        result['sentiment'] = sentiment_data
        
        result['status'] = 'ready_for_interaction'
        return result
    
    def handle_qa_interaction(
        self,
        question: str,
        context_text: str,
        student_id: str,
        audio_file: Optional[str] = None,
        conversation_history: Optional[list] = None
    ) -> Dict:
        """Handle Q&A - voice or text input"""
        
        # If audio provided, transcribe it first
        if audio_file:
            question = self._transcribe_audio(audio_file)
        
        # Get answer from Claude
        answer = self.bedrock_client.answer_question(
            question=question,
            context_text=context_text,
            conversation_history=conversation_history
        )
        
        return {
            'question': question,
            'answer': answer,
            'timestamp': self._get_timestamp()
        }
    
    def generate_story_with_fallback(
        self,
        extracted_text: str,
        student_id: str,
        grade_level: int,
        emotional_theme: Optional[str] = None,
        regenerate_count: int = 0
    ) -> Dict:
        """Generate story with fallback to external sources"""
        
        # Get student preferences from LTM
        prefs = self.ltm_manager.get_student_preferences(student_id)
        
        # First attempt: Generate with Claude
        if regenerate_count == 0:
            story_data = self.bedrock_client.generate_story(
                extracted_text=extracted_text,
                grade_level=grade_level,
                emotional_theme=emotional_theme
            )
            story_hash = self._hash_story(story_data.get('story', ''))
            
            return {
                'source': 'claude',
                'story': story_data,
                'story_hash': story_hash,
                'regenerate_count': 0
            }
        
        # Second attempt: Regenerate with Claude (avoid disliked themes)
        elif regenerate_count == 1:
            # Get themes from previously disliked stories
            avoid_themes = self._extract_themes_from_history(prefs.disliked_stories)
            
            story_data = self.bedrock_client.generate_story(
                extracted_text=extracted_text,
                grade_level=grade_level,
                emotional_theme=emotional_theme,
                avoid_themes=avoid_themes
            )
            story_hash = self._hash_story(story_data.get('story', ''))
            
            return {
                'source': 'claude_regenerated',
                'story': story_data,
                'story_hash': story_hash,
                'regenerate_count': 1
            }
        
        # Third attempt: Use Playwright to browse external sites
        else:
            external_stories = self.story_browser.search_external_stories(
                topic=self._extract_topic(extracted_text),
                grade_level=grade_level,
                emotional_theme=emotional_theme
            )
            
            return {
                'source': 'external',
                'stories': external_stories,
                'regenerate_count': regenerate_count
            }
    
    def handle_story_feedback(
        self,
        student_id: str,
        story_hash: str,
        liked: bool
    ):
        """Record student feedback on story"""
        if not liked:
            self.ltm_manager.add_disliked_story(student_id, story_hash)
    
    def generate_quiz(
        self,
        content: str,
        student_id: str,
        grade_level: int
    ) -> Dict:
        """Generate quiz and track performance"""
        quiz = self.bedrock_client.generate_quiz(
            story_or_text=content,
            grade_level=grade_level
        )
        
        quiz['student_id'] = student_id
        quiz['quiz_id'] = self._generate_id()
        
        return quiz
    
    def record_quiz_results(
        self,
        student_id: str,
        quiz_id: str,
        score: float,
        content_id: str
    ):
        """Record quiz results for analytics"""
        record = PerformanceRecord(
            student_id=student_id,
            timestamp=self._get_timestamp(),
            quiz_score=score,
            content_id=content_id
        )
        self.ltm_manager.record_performance(record)
    
    def generate_teacher_lesson_plan(
        self,
        extracted_text: str,
        grade_level: int,
        duration_minutes: int = 45
    ) -> Dict:
        """Generate lesson plan for teachers"""
        lesson_plan = self.bedrock_client.generate_lesson_plan(
            extracted_text=extracted_text,
            grade_level=grade_level,
            duration_minutes=duration_minutes
        )
        
        return lesson_plan
    
    def get_teacher_analytics(
        self,
        student_id: str,
        days: int = 30
    ) -> Dict:
        """Get student analytics for teacher dashboard"""
        analytics = self.ltm_manager.get_student_analytics(student_id, days)
        prefs = self.ltm_manager.get_student_preferences(student_id)
        
        return {
            'student_id': student_id,
            'performance_history': analytics,
            'emotional_trends': prefs.emotional_state_history,
            'preferences': {
                'grade_level': prefs.grade_level,
                'preferred_topics': prefs.preferred_topics
            }
        }
    
    # Helper methods
    
    def _extract_text(self, bucket: str, key: str) -> str:
        """Extract text using Textract"""
        response = self.textract.start_document_text_detection(
            DocumentLocation={'S3Object': {'Bucket': bucket, 'Name': key}}
        )
        job_id = response['JobId']
        
        # Poll for completion (simplified - use SNS/SQS in production)
        import time
        while True:
            result = self.textract.get_document_text_detection(JobId=job_id)
            status = result['JobStatus']
            if status in ['SUCCEEDED', 'FAILED']:
                break
            time.sleep(2)
        
        if status == 'SUCCEEDED':
            text = ' '.join([block['Text'] for block in result['Blocks'] if block['BlockType'] == 'LINE'])
            return text
        return ""
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        import re
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text
    
    def _analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment with Comprehend"""
        if len(text) > 5000:
            text = text[:5000]
        
        sentiment_response = self.comprehend.detect_sentiment(
            Text=text,
            LanguageCode='en'
        )
        
        return {
            'sentiment': sentiment_response['Sentiment'],
            'confidence': sentiment_response['SentimentScore'],
            'timestamp': self._get_timestamp()
        }
    
    def _transcribe_audio(self, audio_file: str) -> str:
        """Transcribe audio using AWS Transcribe"""
        # Simplified - implement full transcription logic
        return "Transcribed question text"
    
    def _hash_story(self, story: str) -> str:
        """Generate hash for story deduplication"""
        return hashlib.md5(story.encode()).hexdigest()
    
    def _extract_topic(self, text: str) -> str:
        """Extract main topic from text"""
        # Simplified - could use NLP for better extraction
        words = text.split()[:50]
        return ' '.join(words)
    
    def _extract_themes_from_history(self, disliked_hashes: list) -> list:
        """Extract themes from disliked stories"""
        # Simplified - would query stored stories
        return []
    
    def _generate_id(self) -> str:
        """Generate unique ID"""
        import uuid
        return str(uuid.uuid4())
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.utcnow().isoformat()
