import json
import boto3
import urllib.parse
import re
from datetime import datetime

def clean_text_for_analysis(text_content):
    """Clean extracted text for better sentiment analysis"""
    
    # Remove Textract headers and artifacts
    text = re.sub(r'# Clean Text.*?-\s*', '', text_content)
    text = re.sub(r'ANALYZE.*?LAYOUT.*?-\s*', '', text)
    
    # Remove excessive whitespace and line breaks
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n+', '. ', text)
    
    # Remove special characters that might confuse analysis
    text = re.sub(r'[|]+', ' ', text)
    text = re.sub(r'[-]{2,}', ' ', text)
    
    return text.strip()

def analyze_sel_educational_content(text_content):
    """Analyze SEL educational content with detailed categorization"""
    
    text_lower = text_content.lower()
    
    # 🎯 SEL EDUCATIONAL CATEGORIES
    anxiety_keywords = ['anxiety', 'worry', 'fear', 'stress', 'nervous', 'scared', 'breathing', 'calm', 'relax']
    anger_keywords = ['anger', 'mad', 'frustrated', 'upset', 'tantrum', 'control', 'manage', 'regulate']
    sadness_keywords = ['sad', 'sadness', 'grief', 'loss', 'hurt', 'cry', 'comfort', 'support', 'heal']
    joy_keywords = ['happy', 'joy', 'excited', 'proud', 'celebrate', 'smile', 'laugh', 'gratitude']
    social_keywords = ['friendship', 'friends', 'social', 'sharing', 'caring', 'kindness', 'empathy']
    confidence_keywords = ['confidence', 'brave', 'strong', 'growth', 'believe', 'capable', 'resilient']
    mindfulness_keywords = ['mindfulness', 'awareness', 'present', 'focus', 'breathe', 'peaceful', 'quiet']
    story_keywords = ['story', 'tale', 'character', 'adventure', 'lesson', 'moral', 'journey']
    
    # Count occurrences
    anxiety_count = sum(1 for word in anxiety_keywords if word in text_lower)
    anger_count = sum(1 for word in anger_keywords if word in text_lower)
    sadness_count = sum(1 for word in sadness_keywords if word in text_lower)
    joy_count = sum(1 for word in joy_keywords if word in text_lower)
    social_count = sum(1 for word in social_keywords if word in text_lower)
    confidence_count = sum(1 for word in confidence_keywords if word in text_lower)
    mindfulness_count = sum(1 for word in mindfulness_keywords if word in text_lower)
    story_count = sum(1 for word in story_keywords if word in text_lower)
    
    # Determine primary SEL category
    categories = {
        'anxiety_management': anxiety_count,
        'anger_regulation': anger_count,
        'sadness_processing': sadness_count,
        'joy_exploration': joy_count,
        'social_skills': social_count,
        'confidence_building': confidence_count,
        'mindfulness': mindfulness_count,
        'educational_story': story_count
    }
    
    # Get top category
    primary_category = max(categories, key=categories.get) if max(categories.values()) > 0 else 'general_sel'
    
    # Generate key message with facial expressions
    messages = {
        'anxiety_management': "😰➡️😌 This content helps children manage anxiety, worries, and fears.",
        'anger_regulation': "😠➡️😊 This content teaches children anger management and self-regulation.",
        'sadness_processing': "😢➡️🤗 This content helps children process sadness and difficult emotions.",
        'joy_exploration': "😊✨ This content explores positive emotions and happiness with children.",
        'social_skills': "🤝😊 This content builds social skills, friendship, and empathy.",
        'confidence_building': "😔➡️😎 This content builds children's self-confidence and resilience.",
        'mindfulness': "😵‍💫➡️😇 This content teaches children mindfulness and calming techniques.",
        'educational_story': "📚😊 This story teaches children valuable social-emotional lessons.",
        'general_sel': "🌟😊 This content supports children's social-emotional development."
    }
    
    return {
        'category': primary_category,
        'message': messages[primary_category],
        'technique_count': sum(categories.values())
    }

def enhance_sel_sentiment(category, technique_count):
    """Simple sentiment enhancement for SEL content"""
    
    if category in ['joy_exploration', 'confidence_building', 'social_skills']:
        return 'POSITIVE', {'Positive': 0.7, 'Negative': 0.1, 'Neutral': 0.2, 'Mixed': 0.0}
    elif category in ['anxiety_management', 'anger_regulation']:
        if technique_count > 3:
            return 'POSITIVE', {'Positive': 0.6, 'Negative': 0.2, 'Neutral': 0.2, 'Mixed': 0.0}
        else:
            return 'MIXED', {'Positive': 0.4, 'Negative': 0.3, 'Neutral': 0.1, 'Mixed': 0.6}
    elif category == 'sadness_processing':
        return 'MIXED', {'Positive': 0.4, 'Negative': 0.3, 'Neutral': 0.1, 'Mixed': 0.6}
    elif category == 'mindfulness':
        return 'POSITIVE', {'Positive': 0.6, 'Negative': 0.1, 'Neutral': 0.3, 'Mixed': 0.0}
    else:  # general_sel, educational_story
        return 'NEUTRAL', {'Positive': 0.3, 'Negative': 0.1, 'Neutral': 0.6, 'Mixed': 0.0}

def generate_facial_emotions(category, sentiment):
    """Generate emotions with facial expressions for SEL content"""
    
    emotion_map = {
        'anxiety_management': ['Worried 😰', 'Calming 😌', 'Peaceful 😊'],
        'anger_regulation': ['Frustrated 😠', 'Controlled 😤', 'Happy 😊'],
        'sadness_processing': ['Sad 😢', 'Comforted 🤗', 'Hopeful 🙂'],
        'joy_exploration': ['Happy 😊', 'Excited 😃', 'Joyful 😄'],
        'social_skills': ['Friendly 😊', 'Caring 🥰', 'Kind 😇'],
        'confidence_building': ['Shy 😔', 'Brave 😤', 'Confident 😎'],
        'mindfulness': ['Confused 😵‍💫', 'Focused 🧘‍♀️', 'Peaceful 😇'],
        'educational_story': ['Curious 🤔', 'Engaged 😊', 'Thoughtful 😌'],
        'general_sel': ['Learning 🤓', 'Growing 😊', 'Understanding 😌']
    }
    
    emotions = emotion_map.get(category, ['Supportive 😊', 'Educational 🤓'])
    
    # Adjust based on sentiment
    if sentiment == 'POSITIVE':
        return emotions[-2:]  # Take the more positive emotions
    elif sentiment == 'NEGATIVE':
        return emotions[:2]   # Take the more challenging emotions
    elif sentiment == 'MIXED':
        return [emotions[0], emotions[-1]]  # Take first and last (journey)
    else:  # NEUTRAL
        return emotions[1:3] if len(emotions) > 2 else emotions  # Take middle emotions
    
def get_sentiment_face(sentiment):
    """Get facial expression for sentiment"""
    
    sentiment_faces = {
        'POSITIVE': '😊',
        'NEGATIVE': '😔', 
        'NEUTRAL': '😐',
        'MIXED': '😕'
    }
    
    return sentiment_faces.get(sentiment, '😐')

def lambda_handler(event, context):
    try:
        # Initialize AWS clients
        s3_client = boto3.client('s3')
        comprehend_client = boto3.client('comprehend')
        
        # Get bucket and object key from S3 event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
        
        print(f"Processing SEL content: {key}")
        
        # -----------------------------
        # Updated: Only process CLEAN files
        # -----------------------------
        if not key.startswith('sel-output/raw_text/') or not key.endswith('_clean.txt'):
            print(f"Skipping non-clean file: {key}")
            return {
                'statusCode': 200,
                'body': json.dumps({'message': f'Skipped non-clean file: {key}'})
            }
        
        # Read the text file
        response = s3_client.get_object(Bucket=bucket, Key=key)
        text_content = response['Body'].read().decode('utf-8')
        
        if len(text_content.strip()) < 10:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Text too short for analysis'})
            }
        
        # Clean and analyze text
        cleaned_text = clean_text_for_analysis(text_content)
        
        # Truncate for Comprehend
        text_bytes = cleaned_text.encode('utf-8')
        if len(text_bytes) > 4900:
            truncated_bytes = text_bytes[:4900]
            try:
                cleaned_text = truncated_bytes.decode('utf-8')
            except UnicodeDecodeError:
                cleaned_text = truncated_bytes[:4800].decode('utf-8', errors='ignore')
        
        # SEL Analysis
        sel_analysis = analyze_sel_educational_content(text_content)
        
        # Comprehend Analysis
        sentiment_response = comprehend_client.detect_sentiment(
            Text=cleaned_text,
            LanguageCode='en'
        )
        
        # Enhance sentiment for SEL
        enhanced_sentiment, enhanced_scores = enhance_sel_sentiment(
            sel_analysis['category'], 
            sel_analysis['technique_count']
        )
        
        # Generate emotions with facial expressions
        emotions = generate_facial_emotions(sel_analysis['category'], enhanced_sentiment)
        
        # Get sentiment emoji and face
        sentiment_emoji_map = {
            'POSITIVE': '🟩',
            'NEGATIVE': '🟥', 
            'NEUTRAL': '🟨',
            'MIXED': '🟧'
        }
        
        sentiment_face = get_sentiment_face(enhanced_sentiment)
        
        # Create simple, clean output with facial expressions
        results = {
            "OverallSentiment": enhanced_sentiment,
            "DetectedSentiment": f"{sentiment_emoji_map.get(enhanced_sentiment, '🟨')} {enhanced_sentiment.title()} ({max(enhanced_scores.values()):.2f}) {sentiment_face}",
            "DominantEmotions": "  ".join(emotions),
            "KeyMessage": sel_analysis['message'],
            "SELCategory": sel_analysis['category'].replace('_', ' ').title(),
            "EmotionalJourney": f"{emotions[0]} ➡️ {emotions[-1]}" if len(emotions) > 1 else emotions[0]
        }
        
        # Save results
        filename = key.split('/')[-1].replace('.txt', '').replace('_clean', '')
        output_key = f"sel-output/emotion_results/{filename}_analysis.json"
        
        s3_client.put_object(
            Bucket=bucket,
            Key=output_key,
            Body=json.dumps(results, indent=2, ensure_ascii=False),
            ContentType='application/json'
        )
        
        print(f"Analysis saved to: {output_key}")
        # 🚀 AUTO-TRIGGER ORCHESTRATOR
        try:
            # Read the clean text file for orchestrator
            clean_text_response = s3_client.get_object(Bucket=bucket, Key=key)
            clean_text = clean_text_response['Body'].read().decode('utf-8')
            
            # Prepare orchestrator payload
            orchestrator_payload = {
                "extracted_text": clean_text,
                "grade_level": "Grade 5",
                "story_theme": "adventure", 
                "quiz_type": "multiple_choice",
                "subject": "Science",
                "emotions": emotions,
                "filename": filename,
                "source": "document_upload"
            }
            
            # Trigger orchestrator
            lambda_client = boto3.client('lambda')
            response = lambda_client.invoke(
                FunctionName='SEL-content-orchestrator',
                InvocationType='Event',
                Payload=json.dumps(orchestrator_payload)
            )
            
            print(f"✅ Orchestrator triggered successfully for {filename}")
            
        except Exception as orchestrator_error:
            print(f"⚠️ Orchestrator trigger failed: {str(orchestrator_error)}")
            # Don't fail the main function if orchestrator fails
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'SEL analysis completed! 😊',
                'output_file': output_key,
                'category': sel_analysis['category'],
                'sentiment': enhanced_sentiment,
                'preview': results
            }, ensure_ascii=False)
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
