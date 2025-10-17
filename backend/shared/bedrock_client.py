"""
Bedrock Claude Sonnet 4.5 Client for SEL Platform
Handles story generation, quiz creation, Q&A, and lesson planning
"""
import boto3
import json
from typing import Dict, List, Optional
from datetime import datetime


class BedrockClient:
    """Client for AWS Bedrock Claude Sonnet 4.5"""
    
    def __init__(self, model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0"):
        self.bedrock = boto3.client('bedrock-runtime')
        self.model_id = model_id
    
    def generate_story(
        self, 
        extracted_text: str, 
        grade_level: int,
        emotional_theme: Optional[str] = None,
        avoid_themes: Optional[List[str]] = None
    ) -> Dict:
        """Generate grade-appropriate SEL story based on extracted text"""
        
        prompt = f"""You are an expert SEL (Social-Emotional Learning) story writer for children.

Based on the following text, create an engaging story appropriate for grade {grade_level} students that teaches emotional intelligence and social skills.

Extracted Text:
{extracted_text[:2000]}

Requirements:
- Grade level: {grade_level}
- Emotional theme: {emotional_theme or 'general emotional awareness'}
- Story length: 300-500 words for grades 1-3, 500-800 words for grades 4-6
- Include relatable characters facing emotional challenges
- Show healthy coping strategies and problem-solving
- End with a positive resolution and reflection question
{f"- Avoid these themes: {', '.join(avoid_themes)}" if avoid_themes else ""}

Generate the story in JSON format:
{{
    "title": "Story Title",
    "story": "Full story text...",
    "grade_level": {grade_level},
    "emotional_themes": ["theme1", "theme2"],
    "reflection_question": "Question for students to think about",
    "key_vocabulary": ["word1", "word2"]
}}"""

        response = self._invoke_claude(prompt)
        return self._parse_json_response(response)
    
    def generate_quiz(
        self, 
        story_or_text: str, 
        grade_level: int,
        num_questions: int = 5
    ) -> Dict:
        """Generate SEL-focused quiz based on story or extracted text"""
        
        prompt = f"""Create a {num_questions}-question quiz for grade {grade_level} students based on this content.

Content:
{story_or_text[:2000]}

Requirements:
- Focus on emotional understanding and social awareness
- Mix of multiple choice and short answer questions
- Age-appropriate language for grade {grade_level}
- Include questions about character emotions, motivations, and problem-solving

Generate in JSON format:
{{
    "quiz_title": "Quiz Title",
    "questions": [
        {{
            "question": "Question text",
            "type": "multiple_choice" or "short_answer",
            "options": ["A", "B", "C", "D"],  // only for multiple choice
            "correct_answer": "Answer",
            "explanation": "Why this is correct"
        }}
    ]
}}"""

        response = self._invoke_claude(prompt)
        return self._parse_json_response(response)
    
    def answer_question(
        self, 
        question: str, 
        context_text: str,
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """Answer student questions based on displayed text"""
        
        history_context = ""
        if conversation_history:
            history_context = "\n\nPrevious conversation:\n"
            for msg in conversation_history[-5:]:  # Last 5 messages
                history_context += f"{msg['role']}: {msg['content']}\n"
        
        prompt = f"""You are a helpful SEL learning assistant. Answer the student's question based on the provided text.

Text Context:
{context_text[:3000]}
{history_context}

Student Question: {question}

Provide a clear, age-appropriate answer that helps the student understand the content and its emotional/social aspects."""

        return self._invoke_claude(prompt)
    
    def generate_lesson_plan(
        self, 
        extracted_text: str,
        grade_level: int,
        duration_minutes: int = 45
    ) -> Dict:
        """Generate 30-45 minute lesson plan for teachers"""
        
        prompt = f"""Create a {duration_minutes}-minute SEL lesson plan for grade {grade_level} based on this content.

Content:
{extracted_text[:2000]}

Structure the lesson plan with these phases:
1. Warm-up (5-10 minutes) - Engagement activity
2. Main Activity (15-20 minutes) - Core learning experience
3. Extension (10-15 minutes) - Deeper exploration or application
4. Assessment (5-10 minutes) - Check for understanding

Generate in JSON format:
{{
    "lesson_title": "Title",
    "grade_level": {grade_level},
    "duration_minutes": {duration_minutes},
    "learning_objectives": ["objective1", "objective2"],
    "sel_competencies": ["self-awareness", "social awareness", etc.],
    "materials_needed": ["material1", "material2"],
    "phases": {{
        "warmup": {{
            "duration_minutes": 10,
            "activities": ["activity description"],
            "teacher_notes": "Notes for teacher"
        }},
        "main_activity": {{
            "duration_minutes": 20,
            "activities": ["activity description"],
            "discussion_questions": ["question1", "question2"],
            "teacher_notes": "Notes"
        }},
        "extension": {{
            "duration_minutes": 10,
            "activities": ["activity description"],
            "differentiation": "How to adapt for different learners",
            "teacher_notes": "Notes"
        }},
        "assessment": {{
            "duration_minutes": 5,
            "methods": ["assessment method"],
            "success_criteria": ["criteria1", "criteria2"],
            "teacher_notes": "Notes"
        }}
    }},
    "reflection_prompts": ["prompt1", "prompt2"],
    "home_connection": "How families can support learning at home"
}}"""

        response = self._invoke_claude(prompt)
        return self._parse_json_response(response)
    
    def _invoke_claude(self, prompt: str, max_tokens: int = 4096) -> str:
        """Invoke Claude via Bedrock"""
        try:
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7
            })
            
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=body
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
        
        except Exception as e:
            print(f"Error invoking Bedrock: {e}")
            raise
    
    def _parse_json_response(self, response: str) -> Dict:
        """Parse JSON from Claude response"""
        try:
            # Try to find JSON in response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
            return json.loads(response)
        except json.JSONDecodeError:
            print(f"Failed to parse JSON response: {response}")
            return {"error": "Failed to parse response", "raw_response": response}
