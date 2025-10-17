#!/bin/bash

echo "Deploying SEL Learning Platform to AWS..."

# Build SAM application
echo "Building SAM application..."
cd infrastructure
sam build

# Deploy
echo "Deploying to AWS..."
sam deploy --guided

echo "Deployment complete!"
echo "Check AWS Console for API Gateway endpoint and resource ARNs"
