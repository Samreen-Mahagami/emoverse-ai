#!/bin/bash

echo "Extracting Lambda function zip files..."

# Create lambdas directory if it doesn't exist
mkdir -p backend/lambdas

# Function to extract and organize
extract_lambda() {
    local zip_file=$1
    local target_dir=$2
    
    if [ -f "$zip_file" ]; then
        echo "Extracting $zip_file to $target_dir..."
        mkdir -p "$target_dir"
        unzip -q "$zip_file" -d "$target_dir"
        echo "✓ Extracted $zip_file"
    else
        echo "⚠ Warning: $zip_file not found"
    fi
}

# Extract each Lambda function
extract_lambda "SEL-S3-Handler.zip" "backend/lambdas/s3-handler"
extract_lambda "SEL-Textract-Processor.zip" "backend/lambdas/textract-processor"
extract_lambda "SEL-Textract-Retriever.zip" "backend/lambdas/textract-retriever"
extract_lambda "SEL-Text-Cleaner.zip" "backend/lambdas/text-cleaner"
extract_lambda "SEL-Comprehend-Analyzer.zip" "backend/lambdas/comprehend-analyzer"
extract_lambda "sel-transcribe-processor.zip" "backend/lambdas/transcribe-processor"
extract_lambda "sel-story-generator.zip" "backend/lambdas/story-generator"
extract_lambda "sel_story_generator-v1.zip" "backend/lambdas/story-generator-v1"
extract_lambda "sel-quiz-generator.zip" "backend/lambdas/quiz-generator"
extract_lambda "SEL-lesson-planner.zip" "backend/lambdas/lesson-planner"
extract_lambda "SEL-content-orchestrator.zip" "backend/lambdas/content-orchestrator"
extract_lambda "SEL-File-Processor.zip" "backend/lambdas/file-processor"
extract_lambda "story-generator-playwright.zip" "backend/lambdas/story-generator-playwright"

echo ""
echo "Extraction complete!"
echo ""
echo "Lambda functions extracted to backend/lambdas/"
echo "You can now review and integrate them with the new architecture."
