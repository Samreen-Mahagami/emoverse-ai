import boto3
import json
import re
from datetime import datetime

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    Lambda to clean text extracted by Textract.
    Triggered via SNS message from SEL-Textract-Retriever.
    """
    print(f"Received event: {json.dumps(event)}")

    # 1️⃣ Parse SNS message
    try:
        message = event['Records'][0]['Sns']['Message']
        msg_data = json.loads(message)
        bucket_name = msg_data['bucket']
        json_key = msg_data['key']
        filename = msg_data['filename']
        print(f"Fetching Textract JSON from s3://{bucket_name}/{json_key}")
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"Error parsing SNS message: {e}")
        return {'statusCode': 400, 'body': json.dumps({'error': 'Invalid SNS message format.'})}

    # 2️⃣ Read Textract JSON from S3
    try:
        obj = s3_client.get_object(Bucket=bucket_name, Key=json_key)
        textract_pages = json.loads(obj['Body'].read())
        
        # Extract text from Textract JSON
        raw_text = extract_text_from_textract(textract_pages)
        if not raw_text:
            raw_text = ""
        print(f"Extracted text length: {len(raw_text)} characters")
    except Exception as e:
        print(f"Error reading Textract JSON from S3: {e}")
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

    # 3️⃣ Clean the text
    clean_text_content = clean_text(raw_text)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 4️⃣ Save cleaned text
    clean_key = f'sel-output/raw_text/{filename}_clean.txt'
    s3_client.put_object(
        Bucket=bucket_name,
        Key=clean_key,
        Body=f"# Extracted Text - {timestamp}\n\n{clean_text_content}",
        ContentType='text/plain'
    )

    # 5️⃣ Save frontend JSON
    frontend_data = {
        "filename": filename,
        "timestamp": timestamp,
        "extracted_text": clean_text_content,
        "word_count": len(clean_text_content.split()),
        "line_count": len(clean_text_content.splitlines()),
        "processing_status": "cleaned"
    }
    frontend_key = f'sel-output/raw_text/{filename}_frontend.json'
    s3_client.put_object(
        Bucket=bucket_name,
        Key=frontend_key,
        Body=json.dumps(frontend_data, indent=2),
        ContentType='application/json'
    )

    print(f"✅ Cleaned text saved for {filename}")

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Text cleaned and saved successfully.',
            's3_clean_text_path': f"s3://{bucket_name}/{clean_key}",
            's3_frontend_json_path': f"s3://{bucket_name}/{frontend_key}",
            'preview': clean_text_content[:500]
        })
    }

# ===============================================
# Extract text from Textract JSON
# ===============================================
def extract_text_from_textract(pages):
    """
    Loops through Textract JSON pages and extracts text from BLOCKS.
    """
    all_text = []
    for page in pages:
        for block in page.get('Blocks', []):
            if block.get('BlockType') == 'LINE' and 'Text' in block:
                all_text.append(block['Text'])
    return "\n".join(all_text)

# ===============================================
# Cleaning function
# ===============================================
def clean_text(text):
    # Remove unwanted characters
    text = re.sub(r'[^A-Za-z0-9\s.,;:!?\'\"#()\[\]{}-]', ' ', text)
    
    # Normalize spacing
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Fix common OCR issues
    text = re.sub(r'\bﬁ\b', 'fi', text)
    text = re.sub(r'\bﬂ\b', 'fl', text)
    text = re.sub(r'—', '-', text)
    
    # Smart Educational Grouping
    text = re.sub(r"(?i)(#?\s*['\"]?[a-z]\s*sound\s*story['\"]?)", r"\n\n📘 \1\n", text)
    text = re.sub(r"(?i)(note\s+for\s+the\s+teacher\s*:?)", r"\n\n🧑‍🏫 \1 ", text)
    text = re.sub(r"(?i)(encircle|colour|match|tick|find)", r"\n🎯 \1", text)
    text = re.sub(r"(?i)(identify|join|name all the pictures|encourage)", r"\n✏️ \1", text)
    
    # Bullet numbering
    text = re.sub(r"(\d+\.)", r"\n🔹 \1", text)
    
    return text.strip()
