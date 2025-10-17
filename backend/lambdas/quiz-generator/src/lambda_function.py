import boto3
import json
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# --- Dynamic Instruction Helper ---
def get_grade_specific_instructions(grade_level):
    """Adjusts vocabulary rules and fun instructions based on grade level."""
    if '1' in grade_level or '2' in grade_level or 'kinder' in grade_level.lower():
        # Low Grades: ULTRA-SIMPLIFIED, maximum fun/emoji requirement, ultra-short sentences.
        return {
            'vocab_rule': "**CRITICAL VOCABULARY RULE:** **DO NOT** use any word longer than two syllables! Use simple, familiar replacements like 'sun,' 'drink,' 'air,' and 'food.' Focus on single-word answers.",
            'fun_rule': "Include at least **TWO EMOJIS** 🥳 per field to make it colorful and attractive. Keep sentences to **4-6 words maximum**.",
            'temperature': 0.8
        }
    elif '6' in grade_level or '7' in grade_level or '8' in grade_level:
        # Middle Grades: Use correct scientific vocabulary, maintain short/fun style.
        return {
            'vocab_rule': "**CRITICAL VOCABULARY RULE:** **MUST** use correct scientific terms like 'photosynthesis,' 'carbon dioxide,' and 'chloroplasts' where appropriate.",
            'fun_rule': "Keep it short and fun! Use a **maximum of two EMOJIS** per field to maintain a cool, engaging style.",
            'temperature': 0.6
        }
    else:
        # Default/Higher Grades
        return {
            'vocab_rule': "Use appropriate scientific terminology.",
            'fun_rule': "Keep explanations extremely short and concise (1-2 sentences MAX). Emojis are optional but should be minimal.",
            'temperature': 0.5
        }


# Helper function for JSON structure examples
def get_quiz_specifications(quiz_type):
    """Provides the LLM with a JSON structure specification."""
    # Examples are now set to the ULTRA-SIMPLE level to bias the LLM for low grades
    specs = {
        'multiple_choice': '{"questions":[{"question":"Plants need the bright **___**. ☀️","options":["Moon","Star","Sun","Rock"],"correct":"Sun","explanation":"Plants love sun power! 🌼✨"}]}',
        'fill_blanks': '{"questions":[{"sentence":"Plants need **___** from the sky. 💧","answer":"water","explanation":"Water helps plants grow! 🌧️🌱"}]}',
        'true_false': '{"questions":[{"statement":"Plants sleep when it is light. 😴","answer":False,"explanation":"No! Plants work when sun is out! ☀️💚"}]}',
        'match': '{"questions":[{"left_items":["Sun","Leaf"],"right_items":["Warm","Green"],"correct_pairs":[["Sun","Warm"],["Leaf","Green"]],"explanation":"Pair happy words! 😊🎉"}]}'
    }
    return specs.get(quiz_type, '{}')

def lambda_handler(event, context):
    bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
    s3 = boto3.client('s3')

    try:
        logger.info(f"Received event: {json.dumps(event)[:200]}")  # Debug log
        extracted_text = event.get('extracted_text', '')
        quiz_type = event.get('quiz_type', 'true_false') 
        grade_level = event.get('grade_level', 'Grade 2') # Focus on low grade
        num_questions = event.get('num_questions', 5)
        emotions = event.get('emotions', {})
        quiz_json_str = ""

        if not extracted_text:
            logger.error(f"No extracted_text in event. Event keys: {list(event.keys())}")
            return {'statusCode': 400, 'body': json.dumps({'error': "No extracted_text provided.", 'message': 'Missing required input'})}

        # Get dynamic instructions based on grade level
        instructions = get_grade_specific_instructions(grade_level)
        logger.info(f"Generating {quiz_type} quiz for {grade_level}. Vocab rule: {instructions['vocab_rule'][:30]}...")

        # --- 1️⃣ Build prompt (Using dynamic rules) ---
        prompt = f"""
        Generate a super fun, easy, and interactive **{quiz_type}** quiz with **{num_questions}** questions for **{grade_level}** students.
        
        **Content:** {extracted_text}
        **Emotional Context:** {emotions}
        
        **Requirements:**
        1. Keep the language extremely short, playful, and simple.
        2. **{instructions['vocab_rule']}**
        3. **{instructions['fun_rule']}**
        4. The last question **MUST** be an SEL question about feelings or actions related to the content.
        5. Keep all 'explanation' fields extremely short and concise (**1 sentence MAXIMUM, 4-6 words**).
        6. **Crucially**, return the output as a valid **JSON object ONLY**.
        7. Use the following JSON structure template:
        {get_quiz_specifications(quiz_type)}
        """

        # --- 2️⃣ Call Claude ---
        model_arn = 'arn:aws:bedrock:us-east-1:089580247707:inference-profile/global.anthropic.claude-sonnet-4-5-20250929-v1:0'

        response = bedrock.invoke_model(
            modelId=model_arn,
            body=json.dumps({
                'anthropic_version': 'bedrock-2023-05-31',
                'max_tokens': 2000,
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': instructions['temperature']
            })
        )

        # --- 3️⃣ Safe parse response (StreamingBody fix) ---
        resp_body = response.get('body')
        if not resp_body: raise ValueError("Claude returned empty response body.")
        resp_body_bytes = resp_body.read()
        resp_body_str = resp_body_bytes.decode('utf-8')
        
        raw_text = json.loads(resp_body_str)
        quiz_json_str = raw_text.get('content', [{}])[0].get('text', '').strip().replace('```json', '').replace('```', '').strip()
        
        if not quiz_json_str: raise ValueError("Claude did not return a valid JSON string.")
        parsed_quiz = json.loads(quiz_json_str)

        # --- 4️⃣ Format frontend-ready quiz (standardized) ---
        formatted_quiz = {"quiz_type": quiz_type, "questions": []}
        questions_list = parsed_quiz.get("questions", [])
        
        for idx, q in enumerate(questions_list, start=1):
            question_data = {"id": idx, "question": "", "options": [], "correct": "", "explanation": ""}
            
            # Use original mapping logic
            if quiz_type == "multiple_choice":
                question_data.update({"question": q.get("question", ""), "options": q.get("options", []), "correct": q.get("correct", ""), "explanation": q.get("explanation", "")})
            elif quiz_type == "fill_blanks":
                question_data.update({"question": q.get("sentence", ""), "options": [], "correct": q.get("answer", ""), "explanation": q.get("explanation", "")})
            elif quiz_type == "true_false":
                question_data.update({"question": q.get("statement", ""), "options": ["True", "False"], "correct": str(q.get("answer", True)), "explanation": q.get("explanation", "")})
            elif quiz_type == "match":
                question_data.update({"question": f"Match the pairs (Set {idx})", "options": {"left_items": q.get("left_items", []), "right_items": q.get("right_items", [])}, "correct": q.get("correct_pairs", []), "explanation": q.get("explanation", "")})

            formatted_quiz["questions"].append(question_data)


        # --- 5️⃣ Save quiz to S3 ---
        import os
        S3_BUCKET_NAME = os.environ.get('PROCESSED_BUCKET', 'ai-sel-hackathon')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        s3_key = f"sel-output/quizzes/Quiz_{timestamp}_{quiz_type}_{grade_level}_ultra_simple.json"
        
        s3.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_key,
            Body=json.dumps(formatted_quiz, indent=2),
            ContentType='application/json'
        )

        logger.info(f"Quiz saved to S3: s3://{S3_BUCKET_NAME}/{s3_key}")

        # Update job status in DynamoDB if job_id provided
        job_id = event.get('job_id')
        if job_id:
            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('sel-job-status')
                table.update_item(
                    Key={'job_id': job_id},
                    UpdateExpression='SET quiz_status = :status, quiz_result = :result, quiz_s3_key = :s3key',
                    ExpressionAttributeValues={
                        ':status': 'completed',
                        ':result': {'quiz_type': quiz_type, 'num_questions': len(formatted_quiz['questions'])},
                        ':s3key': f's3://{S3_BUCKET_NAME}/{s3_key}'
                    }
                )
                logger.info(f"Updated job {job_id} status in DynamoDB")
            except Exception as e:
                logger.error(f"Failed to update DynamoDB: {str(e)}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'quiz': formatted_quiz,
                's3_location': s3_key,
                'quiz_type': quiz_type,
                'grade_level': grade_level,
                'message': 'Quiz generated successfully with ultra-simple logic.'
            })
        }

    except json.JSONDecodeError as e:
        logger.error(f"JSON Decoding Error: {e}. Raw response part: {quiz_json_str[:500] if 'quiz_json_str' in locals() else 'N/A'}")
        return {'statusCode': 500, 'body': json.dumps({'error': f"Failed to parse JSON from Claude: {str(e)}", 'message': 'Failed to generate quiz due to invalid LLM output format'})}
    except Exception as e:
        logger.error(f"Error generating quiz: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps({'error': str(e), 'message': 'Failed to generate quiz'})}