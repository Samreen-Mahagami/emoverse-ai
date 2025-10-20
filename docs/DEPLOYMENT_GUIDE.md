# 🌈 EmoVerse AI - Complete Serverless Deployment Guide

## Mental Health & Social-Emotional Learning Platform

**Built for AWS AI Agent Global Hackathon**

A complete serverless platform supporting children's and teens' mental health through personalized AI-driven emotional learning.

### ✨ Platform Features:
- ✅ Beautiful Streamlit UI with colorful, child-friendly design
- ✅ Real AWS backend with serverless architecture
- ✅ Mental health focused SEL content for K-10 students
- ✅ Three-tier AI agent system with AgentCore
- ✅ Sentiment & emotion analysis with AWS Comprehend
- ✅ Interactive quizzes and personalized stories
- ✅ Teacher portal with lesson plans and analytics

---

## 🏗️ Complete Architecture

```
Student/Teacher → Streamlit Frontend (app_demo.py)
                              ↓
                    ┌─────────┴─────────┐
                    ↓                   ↓
              Student Flow          Teacher Flow
                    ↓                   ↓
        1. Login + Grade Select    1. Login
        2. Upload PDF              2. Upload Content
        3. Click "Create Content"  3. Generate Lesson Plan
                    ↓                   ↓
              ┌─────┴─────┐            ↓
              ↓           ↓            ↓
         S3 Upload   Textract OCR  DynamoDB Query
              ↓           ↓            ↓
         pdfplumber  Text Extract  Analytics Data
              ↓           ↓            ↓
        ┌─────┴───────────┴────┐     ↓
        ↓                      ↓     ↓
   AWS Comprehend        AWS Bedrock (Claude Sonnet 4.5)
   (Sentiment)           (Stories, Quizzes, Q&A, Lessons)
        ↓                      ↓     ↓
        └──────────┬───────────┘     ↓
                   ↓                 ↓
            5 Student Tabs      2 Teacher Tabs
            ↓                        ↓
    1. Read the Text          1. Lesson Planner
    2. Feel the Emotions      2. Student Analytics
    3. Ask Questions
    4. Stories (3-Tier System)
    5. Quizzes (4 Types)
                   ↓
         DynamoDB (Long-Term Memory)
         - Student preferences
         - Quiz results
         - Analytics data
                   ↓
         Playwright Agent (Tier 3)
         - External story search
         - Storyline Online
         - Storyberries
         - Kids Konnect
```

---

## 🎯 Two Deployment Options

### Option 1: Streamlit Cloud (Recommended for Hackathon)
- **Frontend:** Streamlit Cloud (FREE, optimized)
- **Backend:** AWS Services (S3, Textract, Comprehend, Bedrock, DynamoDB)
- **Cost:** ~$5/student/month
- **Setup:** 5 minutes
- **Best for:** Quick deployment, demos, hackathons

### Option 2: ECS Fargate (Full AWS Production)
- **Frontend:** ECS Fargate (serverless containers)
- **Backend:** AWS Services (complete serverless stack)
- **Cost:** ~$20-30/month base + usage
- **Setup:** 30 minutes
- **Best for:** Enterprise, full AWS control, scalability

---

## 🚀 Option 1: Quick Deploy (Recommended)

### Step 1: Verify AWS Services

```bash
# Check S3 bucket
aws s3 ls s3://sel-platform-uploads-089580247707

# Check DynamoDB table
aws dynamodb describe-table --table-name sel-ltm-memory-analytics

# Check API Gateway (if using Lambda functions)
aws apigateway get-rest-apis
```

### Step 2: Prepare Repository

```bash
# 1. Ensure all files are ready
git add .
git commit -m "EmoVerse AI - Mental Health SEL Platform for AWS Hackathon"
git push origin main

# 2. Verify frontend/app_demo.py has correct AWS configuration:
# - AWS_REGION = "us-east-1"
# - S3_BUCKET = "sel-platform-uploads-089580247707"
# - API_BASE (if using API Gateway)
```

### Step 3: Deploy to Streamlit Cloud

```bash
# 1. Go to: https://share.streamlit.io/
# 2. Sign in with GitHub
# 3. Click "New app"
# 4. Configure:
#    - Repository: your-github-username/emoverse-ai
#    - Branch: main
#    - Main file path: frontend/app_demo.py
# 5. Click "Deploy"
```

### Step 4: Configure AWS Credentials

In Streamlit Cloud dashboard → Settings → Secrets:

```toml
# Add these secrets (DO NOT commit to GitHub)
AWS_ACCESS_KEY_ID = "YOUR_AWS_ACCESS_KEY"
AWS_SECRET_ACCESS_KEY = "YOUR_AWS_SECRET_KEY"
AWS_DEFAULT_REGION = "us-east-1"
S3_BUCKET = "sel-platform-uploads-089580247707"
```

### Step 5: Access the Live App

```
https://your-app-name.streamlit.app
```

**The platform is now live and ready for students and teachers!** 🎉

---

## 🏗️ Option 2: Full AWS Serverless (ECS Fargate)

### Prerequisites

- Docker installed
- AWS CLI configured
- Your backend already deployed

### Step 1: Build and Push Docker Image

```bash
# Run the deployment script
./deploy_serverless_complete.sh
```

This will:
1. Create ECR repository
2. Build Docker image
3. Push to ECR
4. Verify backend deployment

### Step 2: Create ECS Infrastructure

Create `infrastructure/ecs-frontend.yaml`:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: EmoVerse AI - Frontend on ECS Fargate

Parameters:
  ImageUri:
    Type: String
    Description: ECR image URI
    Default: 089580247707.dkr.ecr.us-east-1.amazonaws.com/emoverse-streamlit:latest

Resources:
  # VPC
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true

  # Public Subnets
  PublicSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.1.0/24
      AvailabilityZone: !Select [0, !GetAZs '']
      MapPublicIpOnLaunch: true

  PublicSubnet2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.2.0/24
      AvailabilityZone: !Select [1, !GetAZs '']
      MapPublicIpOnLaunch: true

  # Internet Gateway
  InternetGateway:
    Type: AWS::EC2::InternetGateway

  AttachGateway:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref VPC
      InternetGatewayId: !Ref InternetGateway

  # Route Table
  PublicRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC

  PublicRoute:
    Type: AWS::EC2::Route
    DependsOn: AttachGateway
    Properties:
      RouteTableId: !Ref PublicRouteTable
      DestinationCidrBlock: 0.0.0.0/0
      GatewayId: !Ref InternetGateway

  SubnetRouteTableAssociation1:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PublicSubnet1
      RouteTableId: !Ref PublicRouteTable

  SubnetRouteTableAssociation2:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PublicSubnet2
      RouteTableId: !Ref PublicRouteTable

  # Security Groups
  ALBSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: ALB Security Group
      VpcId: !Ref VPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0

  StreamlitSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Streamlit Container Security Group
      VpcId: !Ref VPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 8501
          ToPort: 8501
          SourceSecurityGroupId: !Ref ALBSecurityGroup

  # Application Load Balancer
  StreamlitALB:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Name: emoverse-streamlit-alb
      Subnets:
        - !Ref PublicSubnet1
        - !Ref PublicSubnet2
      SecurityGroups:
        - !Ref ALBSecurityGroup

  StreamlitTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: emoverse-streamlit-tg
      Port: 8501
      Protocol: HTTP
      VpcId: !Ref VPC
      TargetType: ip
      HealthCheckPath: /_stcore/health
      HealthCheckIntervalSeconds: 30
      HealthCheckTimeoutSeconds: 5
      HealthyThresholdCount: 2
      UnhealthyThresholdCount: 3

  StreamlitListener:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      LoadBalancerArn: !Ref StreamlitALB
      Port: 80
      Protocol: HTTP
      DefaultActions:
        - Type: forward
          TargetGroupArn: !Ref StreamlitTargetGroup

  # ECS Cluster
  StreamlitCluster:
    Type: AWS::ECS::Cluster
    Properties:
      ClusterName: emoverse-streamlit-cluster

  # CloudWatch Log Group
  StreamlitLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: /ecs/emoverse-streamlit
      RetentionInDays: 7

  # ECS Task Execution Role
  TaskExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Statement:
          - Effect: Allow
            Principal:
              Service: ecs-tasks.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

  # ECS Task Role
  TaskRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Statement:
          - Effect: Allow
            Principal:
              Service: ecs-tasks.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: StreamlitTaskPolicy
          PolicyDocument:
            Statement:
              - Effect: Allow
                Action:
                  - s3:*
                  - textract:*
                  - bedrock:*
                  - dynamodb:*
                Resource: '*'

  # ECS Task Definition
  StreamlitTaskDefinition:
    Type: AWS::ECS::TaskDefinition
    Properties:
      Family: emoverse-streamlit
      NetworkMode: awsvpc
      RequiresCompatibilities:
        - FARGATE
      Cpu: 512
      Memory: 1024
      ExecutionRoleArn: !GetAtt TaskExecutionRole.Arn
      TaskRoleArn: !GetAtt TaskRole.Arn
      ContainerDefinitions:
        - Name: streamlit-app
          Image: !Ref ImageUri
          PortMappings:
            - ContainerPort: 8501
          Environment:
            - Name: API_BASE
              Value: https://lckrtb0j9e.execute-api.us-east-1.amazonaws.com/Prod
            - Name: AWS_DEFAULT_REGION
              Value: us-east-1
          LogConfiguration:
            LogDriver: awslogs
            Options:
              awslogs-group: !Ref StreamlitLogGroup
              awslogs-region: !Ref AWS::Region
              awslogs-stream-prefix: streamlit

  # ECS Service
  StreamlitService:
    Type: AWS::ECS::Service
    DependsOn: StreamlitListener
    Properties:
      ServiceName: emoverse-streamlit-service
      Cluster: !Ref StreamlitCluster
      TaskDefinition: !Ref StreamlitTaskDefinition
      DesiredCount: 1
      LaunchType: FARGATE
      NetworkConfiguration:
        AwsvpcConfiguration:
          Subnets:
            - !Ref PublicSubnet1
            - !Ref PublicSubnet2
          SecurityGroups:
            - !Ref StreamlitSecurityGroup
          AssignPublicIp: ENABLED
      LoadBalancers:
        - ContainerName: streamlit-app
          ContainerPort: 8501
          TargetGroupArn: !Ref StreamlitTargetGroup

Outputs:
  LoadBalancerURL:
    Description: URL of the load balancer
    Value: !Sub http://${StreamlitALB.DNSName}
```

### Step 3: Deploy ECS Stack

```bash
aws cloudformation create-stack \
  --stack-name emoverse-frontend \
  --template-body file://infrastructure/ecs-frontend.yaml \
  --capabilities CAPABILITY_IAM \
  --parameters ParameterKey=ImageUri,ParameterValue=089580247707.dkr.ecr.us-east-1.amazonaws.com/emoverse-streamlit:latest
```

### Step 4: Get Your URL

```bash
aws cloudformation describe-stacks \
  --stack-name emoverse-frontend \
  --query 'Stacks[0].Outputs[?OutputKey==`LoadBalancerURL`].OutputValue' \
  --output text
```

Your app will be at: `http://your-alb-url.amazonaws.com`

---

## ✅ Verification & Testing

### Test the Complete Student Flow:

1. **Login & Upload**
   - Open the app
   - Click "Student" button
   - Enter Student ID and select Grade (K-10)
   - Upload a PDF document
   - Click "Create My Learning Content"

2. **Verify All 5 Tabs:**
   - ✅ **Tab 1: Read the Text** - Extracted content displays
   - ✅ **Tab 2: Feel the Emotions** - Sentiment analysis shows
   - ✅ **Tab 3: Ask Questions** - AI tutor responds
   - ✅ **Tab 4: Stories** - Three-tier system works (Claude → Regenerate → Playwright)
   - ✅ **Tab 5: Quizzes** - 20 questions across 4 types

3. **Test Teacher Portal:**
   - Click "Teacher" button
   - Enter Teacher ID
   - Click "Start Teaching"
   - Upload content and generate lesson plan
   - Check student analytics

### Test AWS Services:

```bash
# Test S3 upload
aws s3 ls s3://sel-platform-uploads-089580247707/uploads/

# Test DynamoDB
aws dynamodb scan --table-name sel-ltm-memory-analytics --limit 5

# Test Textract (if using images)
aws textract start-document-text-detection \
  --document-location '{"S3Object":{"Bucket":"sel-platform-uploads-089580247707","Name":"test.pdf"}}'
```

---

## 💰 Cost Breakdown (50 Students, 1 Month)

### Assumptions:
- **50 students** using the platform
- **1 month** duration
- Each student: 5 sessions/month
- Average: 2 PDFs per session (10 pages each)
- 5 questions per session
- 2 stories + 1 quiz per session

### Option 1: Streamlit Cloud (Recommended)

| Service | Usage | Cost |
|---------|-------|------|
| **Streamlit Cloud** | Frontend hosting | **FREE** |
| **S3 Storage** | 500 PDFs (~5GB) | $0.12 |
| **Textract** | 5,000 pages | $7.50 |
| **Comprehend** | 250 sentiment analyses | $0.03 |
| **Bedrock (Claude Sonnet 4.5)** | ~2M tokens | $6.00 |
| **DynamoDB** | 250 writes, 500 reads | $0.50 |
| **Data Transfer** | Minimal | $0.50 |
| **Total for 50 students/month** | | **~$14.65** |
| **Per student/month** | | **~$0.29** |

### Option 2: ECS Fargate (Full AWS)

| Service | Usage | Cost |
|---------|-------|------|
| **ECS Fargate** | 1 task, 24/7 | $15.00 |
| **Application Load Balancer** | 1 ALB | $16.20 |
| **AWS Services** | Same as above | $14.65 |
| **Total for 50 students/month** | | **~$45.85** |
| **Per student/month** | | **~$0.92** |

### Cost Breakdown Details:

**S3 Storage:**
- 500 PDFs × 10MB average = 5GB
- $0.023 per GB = $0.12/month

**Textract:**
- 50 students × 5 sessions × 2 PDFs × 10 pages = 5,000 pages
- $1.50 per 1,000 pages = $7.50/month

**Comprehend:**
- 50 students × 5 sessions = 250 sentiment analyses
- $0.0001 per unit = $0.03/month

**Bedrock (Claude Sonnet 4.5):**
- Input: ~1.5M tokens (stories, quizzes, Q&A)
- Output: ~500K tokens
- $3 per 1M input tokens + $15 per 1M output tokens
- ~$6.00/month

**DynamoDB:**
- 250 write requests + 500 read requests
- On-demand pricing: $0.50/month

### Scaling Estimates:

| Students | Monthly Cost (Streamlit) | Per Student |
|----------|-------------------------|-------------|
| 50 | $14.65 | $0.29 |
| 100 | $29.30 | $0.29 |
| 500 | $146.50 | $0.29 |
| 1,000 | $293.00 | $0.29 |

### Cost Optimization:
- ✅ Use Streamlit Cloud (FREE frontend)
- ✅ Enable S3 lifecycle policies (archive after 30 days)
- ✅ Use DynamoDB on-demand pricing
- ✅ Monitor Bedrock token usage with CloudWatch
- ✅ Set billing alarms at $20, $50, $100 thresholds

---

## 🎉 Platform is Live!

### EmoVerse AI Capabilities:
- ✅ Supporting Social-Emotional Learning for Grades 1-10
- ✅ Processing PDF documents with AWS Textract and pdfplumber
- ✅ Analyzing text sentiment with AWS Comprehend
- ✅ Generating educational content with Claude Sonnet 4.5
- ✅ Three-tier AI agent system with AgentCore Long-Term Memory
- ✅ Tracking student progress and quiz results in DynamoDB
- ✅ Providing teacher tools: lesson plans and analytics
- ✅ Fully serverless AWS architecture
- ✅ Scalable from 50 to 1,000+ students

**Ready for classroom deployment and educational use!** 🚀

---

## 📚 Project Structure

```
emoverse-ai/
├── frontend/
│   ├── app_demo.py              # Main Streamlit application
│   ├── requirements.txt         # Python dependencies
│   └── Dockerfile              # Container definition (for ECS)
├── backend/
│   ├── agentcore/
│   │   ├── memory/             # Long-term memory (DynamoDB)
│   │   └── playwright_agent/   # External story search
│   └── shared/
│       ├── bedrock_client.py   # Claude Sonnet 4.5 integration
│       └── orchestrator.py     # Workflow coordinator
├── infrastructure/
│   ├── template.yaml           # SAM/CloudFormation template
│   └── ecs-frontend.yaml       # ECS Fargate configuration
├── docs/
│   ├── COMPLETE_SYSTEM_FLOW.md # Complete system documentation
│   ├── ARCHITECTURE.md         # Architecture overview
│   └── COMPLETE_SERVERLESS_GUIDE.md # This file
└── README.md                   # Project overview
```

---

## 🌟 Key Features Implemented

### Student Features (Grades 1-10):
1. ✅ **Document Upload** - PDF/Image processing with S3 + Textract
2. ✅ **Text Extraction** - pdfplumber + PyPDF2 fallback (processes all pages)
3. ✅ **Emotion Analysis** - AWS Comprehend sentiment detection (POSITIVE, NEGATIVE, NEUTRAL, MIXED)
4. ✅ **AI Tutor** - Context-aware Q&A with Claude Sonnet 4.5 (grade-appropriate responses)
5. ✅ **Three-Tier Stories** - Claude → Regenerate → Playwright external search
6. ✅ **Interactive Quizzes** - 20 questions across 4 types (MCQ, True/False, Fill-in-Blank, Match-Pair)
7. ✅ **Long-Term Memory** - DynamoDB tracks preferences and learning patterns

### Teacher Features:
1. ✅ **Lesson Plan Generator** - 30-60 minute SEL lessons with structured activities
2. ✅ **Student Analytics** - Performance tracking and progress monitoring
3. ✅ **Real-time Dashboard** - Quiz results, scores, and engagement metrics

### AWS Services Used:
- ✅ **S3** - Document storage
- ✅ **Textract** - OCR for images
- ✅ **Comprehend** - Sentiment/emotion analysis
- ✅ **Bedrock** - Claude Sonnet 4.5 AI generation
- ✅ **DynamoDB** - Long-term memory and analytics
- ✅ **Lambda** - Serverless compute (optional)
- ✅ **API Gateway** - REST endpoints (optional)

### Development Tools:
- ✅ **Amazon Q Developer** - AWS integration guidance
- ✅ **Kiro AI IDE** - Accelerated development

---

## 🏆 Built for AWS AI Agent Global Hackathon

**Mission:** Supporting children's and teens' mental health through personalized, AI-driven Social-Emotional Learning.

**Innovation:** Three-tier AI agent system with AgentCore Long-Term Memory ensures every child gets content they love.

**Impact:** Helping children build emotional resilience, understand their feelings, and develop healthy coping strategies.

---

## 📞 Support & Resources

- **Documentation:** See `docs/` folder for complete guides
- **Architecture:** Review `ARCHITECTURE.md` for system design
- **System Flow:** Check `COMPLETE_SYSTEM_FLOW.md` for detailed workflows
- **AWS Console:** Monitor services in AWS Management Console
- **CloudWatch:** View logs and metrics for debugging

---

**Recommendation: Use Option 1 (Streamlit Cloud) for fastest deployment and hackathon demos!** ✅

**EmoVerse AI - Your AI Universe of Emotional Learning** 🌈💚
