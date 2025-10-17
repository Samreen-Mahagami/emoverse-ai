import json
import boto3
import logging
from datetime import datetime
from pathlib import Path

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
# NOTE: Ensure your Lambda execution role has permissions for Bedrock and S3
bedrock = boto3.client('bedrock-runtime')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    """
    Generates a tailored SEL Lesson Plan using Amazon Bedrock (Claude) and saves it to S3.
    """
    try:
        # --- 1. Extract and Validate Input Parameters ---
        logger.info(f"Received event: {json.dumps(event)[:200]}")  # Debug log
        extracted_text = event.get('extracted_text', '')
        emotions_data = event.get('emotions', {})
        grade_level = event.get('grade_level', 'Grade 5')
        lesson_topic = event.get('lesson_topic', 'emotional awareness')
        
        if not extracted_text:
            logger.error(f"No extracted_text in event. Event keys: {list(event.keys())}")
            return {'statusCode': 400, 'body': json.dumps({'error': "Missing required 'extracted_text' input."})}

        logger.info(f"Generating lesson for {grade_level}, topic: {lesson_topic}")
        
        # --- 2. Robust Emotion Data Handling ---
        emotions = {}
        dominant_emotion = 'NEUTRAL'
        try:
            # Handle string or list inputs from other services (e.g., Comprehend JSON output)
            if isinstance(emotions_data, str):
                emotions = json.loads(emotions_data)
            elif isinstance(emotions_data, list) and len(emotions_data) > 0:
                # Take the first element of the list
                first_item = emotions_data[0]
                emotions = json.loads(first_item) if isinstance(first_item, str) else first_item
            elif isinstance(emotions_data, dict):
                emotions = emotions_data
            
            # Safely extract the dominant sentiment for tailoring and naming
            dominant_emotion = emotions.get('Sentiment', 'NEUTRAL').upper()
            
        except (json.JSONDecodeError, TypeError, IndexError) as e:
            logger.warning(f"Could not fully parse emotions data: {e}. Defaulting to NEUTRAL.")
            
        # Create clear context for the LLM
        emotion_context = f"The student's current emotional state is {dominant_emotion}."

        # --- 3. Build Lesson Plan Prompt (Using your detailed structure) ---
        prompt = f"""
        Create a comprehensive, highly detailed SEL (Social-Emotional Learning) lesson plan for a teacher teaching {grade_level} students.
        
        Context for Lesson Tailoring:
        - Lesson Topic: {lesson_topic}
        - Student's Emotional State: {emotion_context}
        - Student Input/Trigger Context (Use this for realistic examples in activities): "{extracted_text[:300]}"
        
        CRITICAL REQUIREMENTS:
        1. The lesson MUST be specifically tailored to address the challenge or need suggested by the student's **Emotional State** and **Input**.
        2. Ensure the tone and vocabulary are perfectly age-appropriate for a {grade_level} classroom.
        3. Make the activities interactive, engaging, and low-prep for the teacher.
        
        Format the lesson STRICTLY as a comprehensive text block with the following sections, using bold headers and detailed instructions:
        
        **Lesson Title**
        **Grade Level & Duration**
        **SEL Competency** (e.g., Self-Awareness, Relationship Skills)
        **Learning Objectives** (3-4 specific, measurable outcomes)
        **Materials Needed** (List simple items like paper, markers, mirror)
        **Introduction/Hook (10 min)** (A fun, engaging opener related to the emotion)
        **Activity 1: Main Concept (15 min)** (Interactive exercise using the student's input context as an example)
        **Activity 2: Practice Strategy (15 min)** (Role-play, art, or writing activity)
        **Reflection Questions (5 min)** (3-4 closing questions)
        **Takeaway Strategy for Home/School** (1 actionable technique students can use immediately)
        **Wrap-up/Summary (5 min)**
        
        Lesson Plan:
        """
        
        # --- 4. Generate Lesson using Bedrock (Claude Sonnet 4.5) ---
        response = bedrock.invoke_model(
            modelId='arn:aws:bedrock:us-east-1:089580247707:inference-profile/global.anthropic.claude-sonnet-4-5-20250929-v1:0',
            body=json.dumps({
                'anthropic_version': 'bedrock-2023-05-31',
                'max_tokens': 2500,
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': 0.7 
            })
        )
        
        # Parse response
        response_body = json.loads(response['body'].read())
        lesson_content = response_body['content'][0]['text']
        
        # --- 5. Prepare and Save to S3 ---
        
        # Create a safe, clean base name for the S3 file
        clean_topic = lesson_topic.replace(' ', '_').replace('/', '-').lower()
        base_name = f"{grade_level.replace(' ', '')}_{clean_topic}_{dominant_emotion}"

        import os
        bucket_name = os.environ.get('PROCESSED_BUCKET', 'ai-sel-hackathon')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # Use the derived base_name and timestamp in the key
        file_key = f'sel-output/lesson_plans/{base_name}_{timestamp}_Lesson_plan.json'
        
        lesson_data = {
            'title': f'SEL Lesson: {lesson_topic.title()} ({dominant_emotion})',
            'content': lesson_content,
            'grade_level': grade_level,
            'topic': lesson_topic,
            'emotion_context': emotion_context,
            'generated_at': datetime.now().isoformat(),
            'student_input_preview': extracted_text[:200],
            'duration_note': '40-50 minutes (Adjust as needed)', 
            'model_used': 'claude-sonnet-4.5'
        }
        
        s3.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=json.dumps(lesson_data, indent=2),
            ContentType='application/json'
        )
        
        logger.info(f"Lesson saved to s3://{bucket_name}/{file_key}")
        
        # Update job status in DynamoDB if job_id provided
        job_id = event.get('job_id')
        if job_id:
            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('sel-job-status')
                table.update_item(
                    Key={'job_id': job_id},
                    UpdateExpression='SET lesson_status = :status, lesson_result = :result, lesson_s3_key = :s3key',
                    ExpressionAttributeValues={
                        ':status': 'completed',
                        ':result': {'title': lesson_data['title'], 'grade_level': grade_level},
                        ':s3key': f's3://{bucket_name}/{file_key}'
                    }
                )
                logger.info(f"Updated job {job_id} status in DynamoDB")
            except Exception as e:
                logger.error(f"Failed to update DynamoDB: {str(e)}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Lesson generated successfully and tailored to emotional context.',
                'file_location': f's3://{bucket_name}/{file_key}',
                'lesson_title': lesson_data['title']
            })
        }
        
    except Exception as e:
        logger.error(f"Error generating lesson: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'message': 'Failed to generate lesson plan.'
            })
        }