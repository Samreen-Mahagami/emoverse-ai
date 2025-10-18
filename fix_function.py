#!/usr/bin/env python3
# Read the file
with open('frontend/app_demo.py', 'r') as f:
    lines = f.readlines()

# New function
new_function = '''def process_with_aws(uploaded_file):
    """Process document - Show text immediately, AI loads in background"""
    
    with st.spinner("Processing..."):
        # Upload to S3
        file_key = upload_to_s3(uploaded_file, st.session_state.student_id)
        if not file_key:
            st.error("Failed to process file. Please try again.")
            return
        
        # Extract text with Textract
        extracted_text = extract_text_from_s3(file_key)
        if not extracted_text:
            st.error("Failed to extract text. Please try a different file.")
            return
        
        # SHOW TEXT IMMEDIATELY - Don't wait for AI!
        st.session_state.extracted_text = extracted_text
        st.session_state.processed_content = {
            'cleaned_text': extracted_text,
            'sentiment': {'sentiment': 'POSITIVE'},
            'loading_ai': True  # AI content still loading
        }
        
        # Start AI generation in background
        job_data = start_content_generation(
            extracted_text,
            st.session_state.grade_level,
            story_theme="friendship",
            quiz_type="multiple_choice"
        )
        
        if job_data:
            st.session_state.job_id = job_data['job_id']
            st.session_state.job_start_time = time_module.time()
    
    # Show tabs immediately
    st.balloons()
    st.rerun()

'''

# Replace the function (lines 934-987)
new_lines = lines[:934] + [new_function] + lines[987:]

# Write back
with open('frontend/app_demo.py', 'w') as f:
    f.writelines(new_lines)

print("✅ Function replaced successfully!")
