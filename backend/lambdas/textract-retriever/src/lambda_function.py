import json
import boto3
import os
import urllib.parse

# Initialize clients
textract_client = boto3.client('textract')
s3_client = boto3.client('s3')
sns_client = boto3.client('sns')

# Define the target S3 bucket and prefix
OUTPUT_BUCKET = 'ai-sel-hackathon'
OUTPUT_PREFIX = 'sel-output/raw_text/'

# SNS Topic ARN to trigger SEL-Text-Cleaner
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:089580247707:SEL-Text-Cleaner-Trigger' 

def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    Triggered by an SNS notification from Textract upon job completion.
    Retrieves Textract results, saves raw JSON to S3, and publishes SNS for cleaning.
    """
    print(f"Received SNS event: {json.dumps(event)}")
    
    # 1️⃣ Parse the SNS Message
    try:
        sns_message = event['Records'][0]['Sns']['Message']
        textract_data = json.loads(sns_message)

        job_id = textract_data['JobId']
        status = textract_data['Status']
        
        # Get the original document's S3 location
        document_location = textract_data['DocumentLocation']
        original_key = document_location['S3ObjectName']
        file_name = os.path.splitext(os.path.basename(original_key))[0]
        
        print(f"Processing Textract JobId: {job_id}, Status: {status} for file: {file_name}")

    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"Error parsing SNS message: {e}")
        return {'statusCode': 400, 'body': json.dumps({'error': 'Invalid SNS message format.'})}

    # 2️⃣ Check Job Status
    if status == 'SUCCEEDED':
        print(f"Job {job_id} succeeded. Retrieving results...")
        
        try:
            # 3️⃣ Retrieve Textract Results with Pagination
            pages = []
            response = textract_client.get_document_analysis(JobId=job_id)
            pages.append(response)
            
            while 'NextToken' in response:
                next_token = response['NextToken']
                print(f"Retrieving next page with NextToken: {next_token}")
                response = textract_client.get_document_analysis(JobId=job_id, NextToken=next_token)
                pages.append(response)

            # 4️⃣ Save Raw JSON to S3
            output_key = f'{OUTPUT_PREFIX}{file_name}-{job_id}.json'
            s3_client.put_object(
                Bucket=OUTPUT_BUCKET,
                Key=output_key,
                Body=json.dumps(pages),
                ContentType='application/json'
            )
            print(f"✅ Saved raw Textract JSON to s3://{OUTPUT_BUCKET}/{output_key}")

            # 5️⃣ Publish SNS to trigger SEL-Text-Cleaner
            sns_message_cleaner = {
                "bucket": OUTPUT_BUCKET,
                "key": output_key,
                "filename": file_name
            }
            sns_client.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=json.dumps(sns_message_cleaner)
            )
            print(f"✅ Published SNS message to trigger SEL-Text-Cleaner for {file_name}")

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': f'Textract job {job_id} results retrieved, saved to S3, and SNS triggered.'
                })
            }

        except Exception as e:
            print(f"Error retrieving or saving Textract results for JobId {job_id}: {e}")
            raise e 

    elif status == 'FAILED':
        error = textract_data.get('StatusMessage', 'Unknown error.')
        print(f"Job {job_id} failed. Error: {error}")
        
    return {
        'statusCode': 200,
        'body': json.dumps({'message': f'Textract job {job_id} completion notification handled.'})
    }
