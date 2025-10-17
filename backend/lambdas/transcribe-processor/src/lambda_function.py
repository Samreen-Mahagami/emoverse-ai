import json
import boto3
import urllib.parse
from datetime import datetime
import uuid

# Initialize clients globally
s3_client = boto3.client('s3')
transcribe_client = boto3.client('transcribe')
bedrock_client = boto3.client('bedrock')

# Replace with your Claude Sonnet 4.5 model ARN
CLAUDE_MODEL_ARN = "arn:aws:bedrock:us-east-1:089580247707:inference-profile/global.anthropic.claude-sonnet-4-5-20250929-v1:0"

def lambda_handler(event, context):
    try:
        # --- Step 1: Get audio S3 details ---
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

        print(f"Processing audio file: {key} from bucket: {bucket}")

        # Check correct folder
        if not key.startswith('sel-input/audio_questions/'):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid S3 folder for audio'})
            }

        # --- Step 2: Determine media format ---
        file_extension = key.lower().split('.')[-1]
        audio_format_mapping = {
            'mp3': 'mp3',
            'wav': 'wav',
            'flac': 'flac',
            'm4a': 'mp4',
            'aac': 'mp4',
            'ogg': 'ogg'
        }
        if file_extension not in audio_format_mapping:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': f"Unsupported audio format: {file_extension}"})
            }
        media_format = audio_format_mapping[file_extension]

        # --- Step 3: Start Transcribe job ---
        timestamp = int(datetime.now().timestamp())
        job_name = f"audio-transcribe-{uuid.uuid4().hex[:8]}-{timestamp}"
        audio_uri = f"s3://{bucket}/{key}"
        transcript_key = key.replace('sel-input/audio_questions/', 'sel-input/audio_transcripts/').replace(f'.{file_extension}', '.json')

        transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': audio_uri},
            MediaFormat=media_format,
            LanguageCode='en-US',
            OutputBucketName=bucket,
            OutputKey=transcript_key
        )

        print(f"Started transcription job: {job_name} → {transcript_key}")

        # --- Step 4: Poll for transcription completion ---
        for _ in range(30):  # max 30 tries (~3 min if interval=6s)
            status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
            job_status = status['TranscriptionJob']['TranscriptionJobStatus']
            if job_status in ['COMPLETED', 'FAILED']:
                break
            print("Waiting for transcription to complete...")
            import time; time.sleep(6)

        if job_status != 'COMPLETED':
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Transcription job failed or timed out'})
            }

        # --- Step 5: Get transcribed question ---
        transcript_obj = s3_client.get_object(Bucket=bucket, Key=transcript_key)
        transcript_json = json.loads(transcript_obj['Body'].read())
        question_text = transcript_json.get('results', {}).get('transcripts', [{}])[0].get('transcript', '')

        if not question_text:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Transcription resulted in empty text'})
            }

        print(f"Transcribed question: {question_text}")

        # --- Step 6: Get corresponding PDF raw text ---
        # Assuming audio filename matches PDF filename
        pdf_filename = key.split('/')[-1].replace(f'.{file_extension}', '.json')
        pdf_key = f"sel-output/raw_text/{pdf_filename}"

        pdf_obj = s3_client.get_object(Bucket=bucket, Key=pdf_key)
        pdf_text = json.loads(pdf_obj['Body'].read()).get('text', '')

        if not pdf_text:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'PDF text is empty'})
            }

        print(f"Fetched PDF text: {pdf_key}")

        # --- Step 7: Call Claude Sonnet 4.5 ---
        prompt = f"Based on the following content from a PDF:\n{pdf_text}\n\nAnswer the user's question:\n{question_text}"

        response = bedrock_client.invoke_model(
            modelId=CLAUDE_MODEL_ARN,
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1000
            })
        )

        answer_text = json.loads(response['body'].read())['content']
        print(f"Claude answer: {answer_text[:100]}...")

        # --- Step 8: Save answer to S3 ---
        answer_key = f"sel-output/qa/{pdf_filename.replace('.json','')}_answer.json"
        s3_client.put_object(
            Bucket=bucket,
            Key=answer_key,
            Body=json.dumps({
                'question': question_text,
                'answer': answer_text,
                'pdf_key': pdf_key
            })
        )

        return {
            'statusCode': 200,
            'headers': {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            'body': json.dumps({
                'success': True,
                'answer': answer_text,
                'question': question_text,
                'pdf_key': pdf_key,
                's3_key': answer_key
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            'body': json.dumps({'success': False, 'error': str(e)})
        }
