"""
Long-Term Memory Manager for SEL Platform
Stores student preferences, story dislikes, and performance analytics
"""
import boto3
import json
from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel


class StudentPreference(BaseModel):
    student_id: str
    disliked_stories: List[str] = []
    preferred_topics: List[str] = []
    grade_level: int
    emotional_state_history: List[Dict] = []
    last_updated: str


class PerformanceRecord(BaseModel):
    student_id: str
    timestamp: str
    quiz_score: Optional[float] = None
    sentiment_score: Optional[float] = None
    engagement_level: Optional[str] = None
    content_id: str


class LTMManager:
    """Manages long-term memory using DynamoDB"""
    
    def __init__(self, table_name: str = "sel-ltm-memory"):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)
        self.analytics_table = self.dynamodb.Table(f"{table_name}-analytics")
    
    def get_student_preferences(self, student_id: str) -> StudentPreference:
        """Retrieve student preferences from LTM"""
        try:
            response = self.table.get_item(Key={'student_id': student_id})
            if 'Item' in response:
                return StudentPreference(**response['Item'])
            else:
                # Create new preference record
                return StudentPreference(
                    student_id=student_id,
                    grade_level=1,
                    last_updated=datetime.utcnow().isoformat()
                )
        except Exception as e:
            print(f"Error retrieving preferences: {e}")
            return StudentPreference(
                student_id=student_id,
                grade_level=1,
                last_updated=datetime.utcnow().isoformat()
            )
    
    def add_disliked_story(self, student_id: str, story_hash: str):
        """Record a story that the student disliked"""
        prefs = self.get_student_preferences(student_id)
        if story_hash not in prefs.disliked_stories:
            prefs.disliked_stories.append(story_hash)
            prefs.last_updated = datetime.utcnow().isoformat()
            self._save_preferences(prefs)
    
    def is_story_disliked(self, student_id: str, story_hash: str) -> bool:
        """Check if student has already disliked this story"""
        prefs = self.get_student_preferences(student_id)
        return story_hash in prefs.disliked_stories
    
    def update_emotional_state(self, student_id: str, sentiment_data: Dict):
        """Track emotional state over time"""
        prefs = self.get_student_preferences(student_id)
        emotional_record = {
            'timestamp': datetime.utcnow().isoformat(),
            'sentiment': sentiment_data.get('sentiment'),
            'emotions': sentiment_data.get('emotions', []),
            'confidence': sentiment_data.get('confidence')
        }
        prefs.emotional_state_history.append(emotional_record)
        
        # Keep only last 50 records
        if len(prefs.emotional_state_history) > 50:
            prefs.emotional_state_history = prefs.emotional_state_history[-50:]
        
        prefs.last_updated = datetime.utcnow().isoformat()
        self._save_preferences(prefs)
    
    def record_performance(self, record: PerformanceRecord):
        """Store performance data for teacher analytics"""
        try:
            self.analytics_table.put_item(
                Item={
                    'student_id': record.student_id,
                    'timestamp': record.timestamp,
                    'quiz_score': record.quiz_score,
                    'sentiment_score': record.sentiment_score,
                    'engagement_level': record.engagement_level,
                    'content_id': record.content_id
                }
            )
        except Exception as e:
            print(f"Error recording performance: {e}")
    
    def get_student_analytics(self, student_id: str, days: int = 30) -> List[Dict]:
        """Retrieve historical analytics for teacher dashboard"""
        try:
            from datetime import timedelta
            cutoff_date = (datetime.utcnow() - timedelta(days=days)).isoformat()
            
            response = self.analytics_table.query(
                KeyConditionExpression='student_id = :sid AND timestamp > :cutoff',
                ExpressionAttributeValues={
                    ':sid': student_id,
                    ':cutoff': cutoff_date
                }
            )
            return response.get('Items', [])
        except Exception as e:
            print(f"Error retrieving analytics: {e}")
            return []
    
    def _save_preferences(self, prefs: StudentPreference):
        """Save preferences to DynamoDB"""
        try:
            self.table.put_item(Item=prefs.dict())
        except Exception as e:
            print(f"Error saving preferences: {e}")
