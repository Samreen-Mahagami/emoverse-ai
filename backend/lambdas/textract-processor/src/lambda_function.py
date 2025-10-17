import os
import json
import boto3
from urllib.parse import unquote_plus

# Initialize the Textract client
textract_client = boto3.client('textract')

# Get configuration from environment variables (make sure these are set in the Lambda console)
# These were the ARNs you confirmed in the setup steps
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:089580247707:AmazonTextractJobCompletionTopic'
TEXTRACT_ROLE_ARN = 'arn:aws:iam::089580247707:role/TextractServiceRole-v1'

def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    Triggered by an S3 Put event for a document (PDF/Image).
    Starts the asynchronous Textract Document Analysis job.
    """
    print(f"Received event: {json.dumps(event)}")
    
    # 1. Extract S3 Bucket and Key from the event record
    try:
        # S3 events can contain multiple records, but usually only one for a single upload
        record = event['Records'][0]
        s3_info = record['s3']
        bucket_name = s3_info['bucket']['name']
        # The key might be URL-encoded, so we use unquote_plus
        document_key = unquote_plus(s3_info['object']['key'])

    except (KeyError, IndexError) as e:
        print(f"Error extracting S3 info from event: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid S3 event structure.'})
        }
    
    print(f"Processing document: s3://{bucket_name}/{document_key}")
    

    # 2. Start the Textract job
    try:
        response = textract_client.start_document_analysis(
            # The location of the document in S3
            DocumentLocation={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': document_key
                }
            },
            # Specify the features you want Textract to extract
            # Use ['TABLES', 'FORMS', 'QUERIES'] for comprehensive analysis
            FeatureTypes=['TABLES', 'FORMS'],
            
            # This is the critical part for the asynchronous pipeline
            NotificationChannel={
                'SNSTopicArn': SNS_TOPIC_ARN,
                'RoleArn': TEXTRACT_ROLE_ARN 
            },
            
            # Optional: Add a unique job tag or client token for tracking
            JobTag=document_key # Using the file key as a tag for easy lookup
        )

        job_id = response.get('JobId')
        print(f"Textract job successfully started for {document_key}. JobId: {job_id}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Textract job started successfully.',
                'JobId': job_id,
                'DocumentKey': document_key
            })
        }
        
    except Exception as e:
        print(f"Textract API Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Failed to start Textract job: {str(e)}"})
        }