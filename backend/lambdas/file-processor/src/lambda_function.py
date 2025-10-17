import json
import boto3
from urllib.parse import unquote_plus

# Hardcoded ARNs
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:089580247707:AmazonTextractJobCompletionTopic'
TEXTRACT_ROLE_ARN = 'arn:aws:iam::089580247707:role/TextractServiceRole-v1'

def lambda_handler(event, context):
    # Initialize AWS Textract client
    textract = boto3.client('textract')
    
    # List to store the details of all jobs started in this batch
    job_details = []
    
    try:
        # Parse S3 event
        for record in event['Records']:
            bucket = record['s3']['bucket']['name']
            key = unquote_plus(record['s3']['object']['key'])
            
            print(f"Starting Textract analysis for file: {key} from bucket: {bucket}")
            
            # Start Textract document analysis (asynchronous)
            response = textract.start_document_analysis(
                DocumentLocation={
                    'S3Object': {
                        'Bucket': bucket,
                        'Name': key
                    }
                },
                FeatureTypes=['LAYOUT', 'TABLES', 'FORMS'],
                NotificationChannel={
                    'SNSTopicArn': SNS_TOPIC_ARN,
                    'RoleArn': TEXTRACT_ROLE_ARN
                }
            )
            
            job_id = response['JobId']
            print(f"Successfully started Textract job: {job_id}")
            
            job_details.append({
                'file_key': key,
                'jobId': job_id
            })

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Textract analysis successfully started for {len(job_details)} file(s).',
                'jobs': job_details
            })
        }
            
    except Exception as e:
        print(f"Error processing S3 event: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
