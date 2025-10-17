import json
import boto3
import logging
import os
import re
import requests
import time
from typing import Dict, Any

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS clients
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
s3 = boto3.client('s3')

# Playwright Lambda Function URL
PLAYWRIGHT_FUNCTION_URL = "https://7ldyrls5ptaplhaqw6jrlzxsea0tqqsk.lambda-url.us-east-1.on.aws/"

MAX_REGENERATION_ATTEMPTS = 2  # first dislike = regeneration, second dislike = redirect

def split_title_and_content(story_content: str) -> tuple:
    lines = story_content.strip().split('\n')
    if len(lines) > 1:
        title = re.sub(r'[#*]', '', lines[0]).strip()
        content = '\n'.join(lines[1:]).strip()
        return title, content
    return "SEL Adventure Story", story_content

def clean_story_content(content: str) -> str:
    content = re.sub(r'#+\s*', '', content)
    content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)
    content = re.sub(r'__(.*?)__', r'\1', content)
    content = re.sub(r'\n\s*\n', '\n\n', content)
    return content.strip()

def call_playwright_function(story_theme: str, grade_level: str, attempt: int) -> Dict[str, Any]:
    """Call Playwright Lambda for live story scraping"""
    try:
        payload = {'story_theme': story_theme, 'grade_level': grade_level, 'attempt': attempt, 'timestamp': int(time.time())}
        response = requests.post(
            PLAYWRIGHT_FUNCTION_URL,
            json=payload,
            timeout=25,
            headers={'Content-Type': 'application/json', 'User-Agent': 'SEL-Story-Generator/1.0'}
        )
        if response.status_code == 200:
            return response.json()
        return {'success': False, 'error': f'HTTP {response.status_code}'}
    except Exception as e:
        logger.error(f"Playwright call error: {e}")
        return {'success': False, 'error': str(e)}

def lambda_handler(event, context):
    """Main Lambda handler"""
    try:
        body = json.loads(event.get('body', '{}')) if 'body' in event else event
        extracted_text = body.get('extracted_text', '')
        emotions_data = body.get('emotions', {})
        grade_level = body.get('grade_level', 'Grade 5')
        story_theme = body.get('story_theme', 'friendship')
        is_regeneration = body.get('regenerate', False)
        attempt_number = body.get('attempt', 1)

        # Get document name
        document_name = body.get('document_name') or body.get('fileName') or 'Document'
        base_name = os.path.splitext(document_name)[0] if document_name != 'Unknown' else 'Document'

        # Parse emotions
        emotions = {}
        if isinstance(emotions_data, str):
            emotions = json.loads(emotions_data)
        elif isinstance(emotions_data, list) and len(emotions_data) > 0:
            emotions = json.loads(emotions_data[0]) if isinstance(emotions_data[0], str) else emotions_data[0]
        elif isinstance(emotions_data, dict):
            emotions = emotions_data
        dominant_emotion = emotions.get('Sentiment', 'NEUTRAL')

        # IF second dislike → redirect to external story websites
        if is_regeneration and attempt_number > MAX_REGENERATION_ATTEMPTS:
            playwright_result = call_playwright_function(story_theme, grade_level, attempt_number)
            if playwright_result.get('success') and len(playwright_result.get('live_stories', [])) > 0:
                # Take first story URL for redirect
                first_story_site = playwright_result['live_stories'][0].get('url', 'https://www.readingrockets.org/books-and-authors/books/')
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({
                        'success': True,
                        'action': 'redirect',
                        'redirect_url': first_story_site,
                        'message': f"Redirecting to a curated {story_theme} story website..."
                    })
                }
            else:
                # fallback redirect
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({
                        'success': True,
                        'action': 'redirect',
                        'redirect_url': 'https://www.readingrockets.org/books-and-authors/books/',
                        'message': f"Redirecting to fallback story website..."
                    })
                }

        # --- Otherwise generate story via Bedrock ---
        meaningful_text = ""
        if extracted_text and len(extracted_text.strip()) > 10:
            words, unique, seen = extracted_text.split(), [], set()
            for w in words:
                if w.lower() not in seen and len(w) > 2:
                    unique.append(w)
                    seen.add(w.lower())
            meaningful_text = " ".join(unique[:20])

        variety_instructions = f"IMPORTANT: This is regeneration attempt #{attempt_number}." if is_regeneration else ""

        prompt = f"""{variety_instructions}
Create a simple, engaging {story_theme} story for {grade_level} children.
Child shared: "{meaningful_text}"
Child's emotion: {dominant_emotion}
Story theme: {story_theme}
Grade level: {grade_level}

Requirements:
1. Write EXACTLY 200-250 words
2. Use simple words appropriate for {grade_level}
3. Include 5-8 emojis 🌟
4. Focus on {story_theme} theme
5. Positive SEL message
6. Short sentences
7. Fun & relatable
8. Start with title
9. End lesson on NEW LINE: "The {story_theme.title()} Lesson:"
"""

        response = bedrock_client.invoke_model(
            modelId="arn:aws:bedrock:us-east-1:089580247707:inference-profile/global.anthropic.claude-sonnet-4-5-20250929-v1:0",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
            })
        )
        response_body = json.loads(response['body'].read())
        generated_story = response_body['content'][0]['text']
        story_title, story_body = split_title_and_content(generated_story)
        clean_content = clean_story_content(story_body)

        # Save to S3
        story_data = {
            'title': story_title,
            'content': clean_content,
            'grade_level': grade_level,
            'theme': story_theme,
            'regenerated': is_regeneration,
            'attempt': attempt_number
        }
        bucket_name = 'ai-sel-hackathon'
        s3_key = f"sel-output/stories/{base_name}_Story.json" if not is_regeneration else f"sel-output/stories/{base_name}_Story_v{attempt_number}.json"
        s3.put_object(Bucket=bucket_name, Key=s3_key, Body=json.dumps(story_data, indent=2), ContentType='application/json')

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'success': True,
                'action': 'show_story',
                'story': clean_content,
                'title': story_title,
                'theme': story_theme,
                'grade_level': grade_level,
                'attempt': attempt_number
            })
        }

    except Exception as e:
        logger.error(f"Error in Lambda: {e}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'success': False, 'error': str(e)})
        }

