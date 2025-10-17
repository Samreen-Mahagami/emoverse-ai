import json
import boto3
import logging
from decimal import Decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    """
    Check the status of a content generation job
    """
    try:
        # Get job_id from path parameters
        job_id = event.get('pathParameters', {}).get('job_id')
        
        if not job_id:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Missing job_id parameter'})
            }
        
        logger.info(f"Checking status for job: {job_id}")
        
        # Query DynamoDB for job status
        table = dynamodb.Table('sel-job-status')
        response = table.get_item(Key={'job_id': job_id})
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Job not found'})
            }
        
        job = response['Item']
        
        # Check if all generators are complete
        story_status = job.get('story_status', 'pending')
        quiz_status = job.get('quiz_status', 'pending')
        lesson_status = job.get('lesson_status', 'pending')
        
        all_complete = (story_status == 'completed' and 
                       quiz_status == 'completed' and 
                       lesson_status == 'completed')
        
        # Update overall status if all complete
        if all_complete and job.get('status') != 'completed':
            from datetime import datetime
            table.update_item(
                Key={'job_id': job_id},
                UpdateExpression='SET #status = :status, completed_at = :completed',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={
                    ':status': 'completed',
                    ':completed': datetime.now().isoformat()
                }
            )
            job['status'] = 'completed'
            job['completed_at'] = datetime.now().isoformat()
        
        # Return job status
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'job_id': job_id,
                'status': job.get('status', 'unknown'),
                'created_at': job.get('created_at'),
                'completed_at': job.get('completed_at'),
                'progress': {
                    'story': story_status,
                    'quiz': quiz_status,
                    'lesson': lesson_status,
                    'completed': sum([s == 'completed' for s in [story_status, quiz_status, lesson_status]]),
                    'total': 3
                },
                'results': {
                    'story': job.get('story_result', {}),
                    'quiz': job.get('quiz_result', {}),
                    'lesson': job.get('lesson_result', {})
                },
                's3_files': [
                    job.get('story_s3_key'),
                    job.get('quiz_s3_key'),
                    job.get('lesson_s3_key')
                ],
                'error': job.get('error')
            }, cls=DecimalEncoder)
        }
        
    except Exception as e:
        logger.error(f"Error checking job status: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
