#!/bin/bash

echo "🗑️  SEL Platform Hackathon Cleanup Script"
echo "=========================================="
echo ""
echo "⚠️  WARNING: This will delete ALL AWS resources!"
echo "This includes:"
echo "  - CloudFormation stack"
echo "  - S3 buckets and all files"
echo "  - DynamoDB tables and all data"
echo "  - Lambda functions"
echo "  - CloudWatch logs"
echo "  - All other resources"
echo ""
read -p "Are you sure you want to continue? (type 'yes' to confirm): " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ Cleanup cancelled"
    exit 0
fi

echo ""
echo "🔍 Getting AWS account info..."
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION=$(aws configure get region)

echo "Account ID: $ACCOUNT_ID"
echo "Region: $REGION"
echo ""

# Get final cost before deletion
echo "💰 Checking final costs..."
aws ce get-cost-and-usage \
    --time-period Start=$(date -d "30 days ago" +%Y-%m-%d),End=$(date +%Y-%m-%d) \
    --granularity MONTHLY \
    --metrics BlendedCost \
    --output table

echo ""
read -p "Press Enter to start cleanup..."

# 1. Delete CloudFormation stack
echo ""
echo "1️⃣  Deleting CloudFormation stack..."
aws cloudformation delete-stack --stack-name sel-learning-platform
echo "   Waiting for stack deletion (this may take 5-10 minutes)..."
aws cloudformation wait stack-delete-complete --stack-name sel-learning-platform 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✅ Stack deleted successfully"
else
    echo "   ⚠️  Stack deletion in progress or already deleted"
fi

# 2. Delete S3 buckets
echo ""
echo "2️⃣  Deleting S3 buckets..."

UPLOAD_BUCKET="sel-platform-uploads-${ACCOUNT_ID}"
PROCESSED_BUCKET="sel-platform-processed-${ACCOUNT_ID}"

# Empty and delete upload bucket
if aws s3 ls "s3://${UPLOAD_BUCKET}" 2>/dev/null; then
    echo "   Emptying ${UPLOAD_BUCKET}..."
    aws s3 rm "s3://${UPLOAD_BUCKET}" --recursive
    echo "   Deleting ${UPLOAD_BUCKET}..."
    aws s3 rb "s3://${UPLOAD_BUCKET}"
    echo "   ✅ Upload bucket deleted"
else
    echo "   ℹ️  Upload bucket not found"
fi

# Empty and delete processed bucket
if aws s3 ls "s3://${PROCESSED_BUCKET}" 2>/dev/null; then
    echo "   Emptying ${PROCESSED_BUCKET}..."
    aws s3 rm "s3://${PROCESSED_BUCKET}" --recursive
    echo "   Deleting ${PROCESSED_BUCKET}..."
    aws s3 rb "s3://${PROCESSED_BUCKET}"
    echo "   ✅ Processed bucket deleted"
else
    echo "   ℹ️  Processed bucket not found"
fi

# 3. Delete DynamoDB tables
echo ""
echo "3️⃣  Deleting DynamoDB tables..."

# Delete memory table
if aws dynamodb describe-table --table-name sel-ltm-memory 2>/dev/null; then
    aws dynamodb delete-table --table-name sel-ltm-memory
    echo "   ✅ Memory table deleted"
else
    echo "   ℹ️  Memory table not found"
fi

# Delete analytics table
if aws dynamodb describe-table --table-name sel-ltm-memory-analytics 2>/dev/null; then
    aws dynamodb delete-table --table-name sel-ltm-memory-analytics
    echo "   ✅ Analytics table deleted"
else
    echo "   ℹ️  Analytics table not found"
fi

# 4. Delete CloudWatch log groups
echo ""
echo "4️⃣  Deleting CloudWatch log groups..."

LOG_GROUPS=$(aws logs describe-log-groups --query 'logGroups[?contains(logGroupName, `sel`)].logGroupName' --output text)

if [ -n "$LOG_GROUPS" ]; then
    for log_group in $LOG_GROUPS; do
        echo "   Deleting $log_group..."
        aws logs delete-log-group --log-group-name "$log_group"
    done
    echo "   ✅ Log groups deleted"
else
    echo "   ℹ️  No log groups found"
fi

# 5. Delete CloudWatch alarms
echo ""
echo "5️⃣  Deleting CloudWatch alarms..."

ALARMS=$(aws cloudwatch describe-alarms --query 'MetricAlarms[?contains(AlarmName, `SEL`)].AlarmName' --output text)

if [ -n "$ALARMS" ]; then
    aws cloudwatch delete-alarms --alarm-names $ALARMS
    echo "   ✅ Alarms deleted"
else
    echo "   ℹ️  No alarms found"
fi

# 6. Delete SNS topics
echo ""
echo "6️⃣  Deleting SNS topics..."

TOPICS=$(aws sns list-topics --query 'Topics[?contains(TopicArn, `sel`)].TopicArn' --output text)

if [ -n "$TOPICS" ]; then
    for topic in $TOPICS; do
        echo "   Deleting $topic..."
        aws sns delete-topic --topic-arn "$topic"
    done
    echo "   ✅ SNS topics deleted"
else
    echo "   ℹ️  No SNS topics found"
fi

# 7. Delete SQS queues
echo ""
echo "7️⃣  Deleting SQS queues..."

QUEUES=$(aws sqs list-queues --query 'QueueUrls[?contains(@, `sel`)]' --output text)

if [ -n "$QUEUES" ]; then
    for queue in $QUEUES; do
        echo "   Deleting $queue..."
        aws sqs delete-queue --queue-url "$queue"
    done
    echo "   ✅ SQS queues deleted"
else
    echo "   ℹ️  No SQS queues found"
fi

# 8. Verify cleanup
echo ""
echo "8️⃣  Verifying cleanup..."
echo ""

# Check S3
S3_COUNT=$(aws s3 ls | grep -c "sel-platform" || true)
echo "   S3 buckets remaining: $S3_COUNT"

# Check DynamoDB
DYNAMO_COUNT=$(aws dynamodb list-tables --query 'TableNames[?contains(@, `sel`)]' --output text | wc -w)
echo "   DynamoDB tables remaining: $DYNAMO_COUNT"

# Check Lambda
LAMBDA_COUNT=$(aws lambda list-functions --query 'Functions[?contains(FunctionName, `sel`)].FunctionName' --output text | wc -w)
echo "   Lambda functions remaining: $LAMBDA_COUNT"

# Check CloudWatch logs
LOG_COUNT=$(aws logs describe-log-groups --query 'logGroups[?contains(logGroupName, `sel`)].logGroupName' --output text | wc -w)
echo "   CloudWatch log groups remaining: $LOG_COUNT"

echo ""
if [ $S3_COUNT -eq 0 ] && [ $DYNAMO_COUNT -eq 0 ] && [ $LAMBDA_COUNT -eq 0 ] && [ $LOG_COUNT -eq 0 ]; then
    echo "✅ Cleanup complete! All resources deleted."
else
    echo "⚠️  Some resources may still exist. Please check AWS Console."
fi

# Final cost report
echo ""
echo "💰 Final Cost Report (Last 30 Days):"
echo "======================================"
aws ce get-cost-and-usage \
    --time-period Start=$(date -d "30 days ago" +%Y-%m-%d),End=$(date +%Y-%m-%d) \
    --granularity MONTHLY \
    --metrics BlendedCost \
    --group-by Type=SERVICE \
    --output table

echo ""
echo "🎉 Hackathon cleanup complete!"
echo ""
echo "📊 Summary:"
echo "  - All AWS resources deleted"
echo "  - Final costs calculated above"
echo "  - Project files preserved locally"
echo ""
echo "💡 Next steps:"
echo "  1. Review final AWS bill in 2-3 days"
echo "  2. Save project for portfolio"
echo "  3. Update resume/LinkedIn"
echo "  4. Share your success! 🏆"
echo ""
