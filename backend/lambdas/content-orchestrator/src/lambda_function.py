import boto3
import json
import logging
import os
import uuid
from datetime import datetime, timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Orchestrate the generation of stories, quizzes, and lesson plans ASYNCHRONOUSLY
    Returns immediately with a job_id for status polling
    """
    
    lambda_client = boto3.client('lambda')
    dynamodb = boto3.resource('dynamodb')
    
    try:
        # Parse the event - handle both API Gateway and direct invocation
        if 'body' in event:
            # API Gateway event
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            # Direct Lambda invocation
            body = event
        
        logger.info(f"Parsed body: {json.dumps(body)[:200]}")
        
        # Extract common parameters
        extracted_text = body.get('extracted_text', '')
        grade_level = body.get('grade_level', 'Grade 5')
        emotions = body.get('emotions', {})
        
        # Content generation parameters
        story_theme = body.get('story_theme', 'friendship')
        quiz_type = body.get('quiz_type', 'multiple_choice')
        subject = body.get('subject', 'General')
        
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        logger.info(f"Created job {job_id} for {grade_level}, extracted_text length: {len(extracted_text)}")
        
        # Save initial job status to DynamoDB
        table = dynamodb.Table(os.environ.get('JOB_STATUS_TABLE', 'sel-job-status'))
        ttl = int((datetime.now() + timedelta(hours=24)).timestamp())
        
        table.put_item(Item={
            'job_id': job_id,
            'status': 'processing',
            'created_at': datetime.now().isoformat(),
            'ttl': ttl,
            'request': {
                'extracted_text': extracted_text[:100],  # Store first 100 chars
                'grade_level': grade_level,
                'story_theme': story_theme,
                'quiz_type': quiz_type
            },
            'story_status': 'pending',
            'quiz_status': 'pending',
            'lesson_status': 'pending'
        })
        
        logger.info(f"Job {job_id} saved to DynamoDB")
        
        # Prepare payloads for each Lambda function (include job_id)
        story_payload = {
            'extracted_text': extracted_text,
            'grade_level': grade_level,
            'story_theme': story_theme,
            'emotions': emotions,
            'job_id': job_id
        }
        
        quiz_payload = {
            'extracted_text': extracted_text,
            'grade_level': grade_level,
            'quiz_type': quiz_type,
            'num_questions': 5,
            'emotions': emotions,
            'job_id': job_id
        }
        
        lesson_payload = {
            'extracted_text': extracted_text,
            'grade_level': grade_level,
            'subject': subject,
            'lesson_duration': '45 minutes',
            'emotions': emotions,
            'job_id': job_id
        }
        
        # Function names from environment variables
        functions = {
            'story': os.environ.get('STORY_FUNCTION', 'sel-story-generator'),
            'quiz': os.environ.get('QUIZ_FUNCTION', 'sel-quiz-generator'), 
            'lesson': os.environ.get('LESSON_FUNCTION', 'SEL-lesson-planner')
        }
        
        payloads = {
            'story': story_payload,
            'quiz': quiz_payload,
            'lesson': lesson_payload
        }
        
        # Invoke all generators ASYNCHRONOUSLY (don't wait for response)
        for content_type, function_name in functions.items():
            try:
                logger.info(f"Invoking {content_type} generator asynchronously")
                lambda_client.invoke(
                    FunctionName=function_name,
                    InvocationType='Event',  # ASYNC - returns immediately!
                    Payload=json.dumps(payloads[content_type])
                )
                logger.info(f"{content_type} generator invoked successfully")
            except Exception as e:
                logger.error(f"Error invoking {content_type} generator: {str(e)}")
                # Update status in DynamoDB
                table.update_item(
                    Key={'job_id': job_id},
                    UpdateExpression=f'SET {content_type}_status = :status, {content_type}_error = :error',
                    ExpressionAttributeValues={
                        ':status': 'failed',
                        ':error': str(e)
                    }
                )
        
        # Return immediately with job ID (< 1 second response time!)
        return {
            'statusCode': 202,  # 202 Accepted = processing started
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'job_id': job_id,
                'status': 'processing',
                'message': 'Content generation started successfully',
                'poll_url': f'/status/{job_id}',
                'estimated_time': '30-60 seconds',
                'instructions': 'Poll the status endpoint to check progress'
            })
        }
        
    except Exception as e:
        logger.error(f"Orchestrator error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'message': 'Content generation orchestration failed'
            })
        }
