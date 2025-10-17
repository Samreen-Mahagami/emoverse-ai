#!/bin/bash

echo "Setting up SEL Learning Platform..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo "Installing Playwright browsers..."
playwright install chromium

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please update .env with your AWS credentials and configuration"
fi

# Create DynamoDB tables locally (for development)
echo "Setting up local DynamoDB tables..."
aws dynamodb create-table \
    --table-name sel-ltm-memory \
    --attribute-definitions AttributeName=student_id,AttributeType=S \
    --key-schema AttributeName=student_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --endpoint-url http://localhost:8000 2>/dev/null || echo "Table may already exist"

aws dynamodb create-table \
    --table-name sel-ltm-memory-analytics \
    --attribute-definitions \
        AttributeName=student_id,AttributeType=S \
        AttributeName=timestamp,AttributeType=S \
    --key-schema \
        AttributeName=student_id,KeyType=HASH \
        AttributeName=timestamp,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST \
    --endpoint-url http://localhost:8000 2>/dev/null || echo "Analytics table may already exist"

echo "Setup complete!"
echo "To deploy to AWS, run: sam build && sam deploy --guided"
echo "To run locally, run: streamlit run frontend/app.py"
