import json
import boto3
import urllib.parse

def lambda_handler(event, context):
    """
    Handles S3 events and validates files
    Invokes Textract processor directly
    """
    
    print("🚀 SEL-S3-Handler started")
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'], encoding='utf-8')
        
        print(f"📁 New file uploaded: {key}")
        
        # Validate file type
        file_extension = key.lower().split('.')[-1]
        
        if file_extension in ['pdf', 'png', 'jpg', 'jpeg', 'tiff']:
            print(f"✅ Valid file type: {file_extension}")
            
            # Get file size
            s3 = boto3.client('s3')
            try:
                response = s3.head_object(Bucket=bucket, Key=key)
                file_size = response['ContentLength']
                file_size_mb = round(file_size / (1024 * 1024), 2)
                
                print(f"📊 File size: {file_size_mb} MB")
                
                # Prepare data for Textract processor
                payload = {
                    'bucket': bucket,
                    'key': key,
                    'file_size': file_size,
                    'file_extension': file_extension
                }
                
                # Invoke Textract processor
                lambda_client = boto3.client('lambda')
                response = lambda_client.invoke(
                    FunctionName='SEL-Textract-Processor',  # We'll create this next
                    InvocationType='Event',  # Asynchronous
                    Payload=json.dumps(payload)
                )
                
                print(f"🚀 Sent to Textract processor: {key}")
                
            except Exception as e:
                print(f"❌ Error processing {key}: {str(e)}")
                
        else:
            print(f"❌ Unsupported file type: {file_extension}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('S3 files processed successfully')
    }

