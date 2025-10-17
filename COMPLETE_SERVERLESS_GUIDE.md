# 🚀 Complete Serverless Deployment Guide

## Your Complete Production System

Following your WORKFLOW_DIAGRAM.md exactly, with:
- ✅ Your `app_demo.py` frontend (beautiful UI)
- ✅ Real AWS backend (already deployed)
- ✅ Real document processing (no demo)
- ✅ Serverless architecture

---

## 🏗️ Complete Architecture

```
User → CloudFront/ALB → Streamlit (ECS Fargate)
                              ↓
                         API Gateway
                              ↓
                    Content Orchestrator Lambda
                              ↓
              ┌───────────────┼───────────────┐
              ↓               ↓               ↓
      Story Generator   Quiz Generator  Lesson Planner
         (Lambda)          (Lambda)        (Lambda)
              ↓               ↓               ↓
           AWS Bedrock (Claude Sonnet 4.5)
              ↓               ↓               ↓
         DynamoDB + S3 (Results Storage)
              ↓               ↓               ↓
        Status Checker Lambda (Polling)
              ↓
         Frontend (Display Results)
```

---

## 🎯 Two Deployment Options

### Option 1: Streamlit Cloud + Lambda (Recommended)
- **Frontend:** Streamlit Cloud (FREE, optimized)
- **Backend:** Lambda (already deployed)
- **Cost:** ~$5-10/month
- **Setup:** 5 minutes
- **Best for:** Quick deployment, hackathons

### Option 2: ECS Fargate + Lambda (Full AWS)
- **Frontend:** ECS Fargate (serverless containers)
- **Backend:** Lambda (already deployed)
- **Cost:** ~$20-30/month
- **Setup:** 30 minutes
- **Best for:** Enterprise, full AWS control

---

## 🚀 Option 1: Quick Deploy (Recommended)

### Step 1: Ensure Backend is Deployed

```bash
# Check if backend exists
aws cloudformation describe-stacks --stack-name emoverse-ai-prod

# If not deployed, deploy it:
cd infrastructure
sam build
sam deploy
```

### Step 2: Deploy Frontend to Streamlit Cloud

```bash
# 1. Push to GitHub
git add .
git commit -m "Production ready - real AWS integration"
git push origin main

# 2. Go to: https://share.streamlit.io/
# 3. Click "New app"
# 4. Select:
#    - Repository: your-repo
#    - Branch: main
#    - Main file: frontend/app_demo.py
# 5. Click "Deploy"
```

### Step 3: Add AWS Credentials

In Streamlit Cloud dashboard → Settings → Secrets:

```toml
AWS_ACCESS_KEY_ID = "AKIARJW3GDKNVS4ZAKWQ4"
AWS_SECRET_ACCESS_KEY = "your-secret-key"
AWS_DEFAULT_REGION = "us-east-1"
```

### Step 4: Get Your Public URL

```
https://emoverse-ai.streamlit.app
```

**Done! Your app is live!** 🎉

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

## ✅ Verification

Test your deployment:

```bash
# Test backend API
curl https://lckrtb0j9e.execute-api.us-east-1.amazonaws.com/Prod/orchestrate \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"extracted_text":"test","grade_level":"Grade 5"}'

# Test frontend
curl http://your-url/
```

---

## 💰 Cost Breakdown

### Option 1: Streamlit Cloud
- Frontend: FREE
- Backend Lambda: ~$5-10/month
- **Total: ~$5-10/month**

### Option 2: ECS Fargate
- Frontend Fargate: ~$15-20/month
- Backend Lambda: ~$5-10/month
- **Total: ~$20-30/month**

---

## 🎉 You're Live!

Your complete serverless app is now:
- ✅ Processing real PDFs
- ✅ Using real AWS services
- ✅ Following WORKFLOW_DIAGRAM.md flow
- ✅ Fully serverless
- ✅ Production-ready

**Share your URL and start using it!** 🚀

---

## 📚 Files Created

- `frontend/Dockerfile` - Container definition
- `frontend/requirements.txt` - Python dependencies
- `infrastructure/ecs-frontend.yaml` - ECS infrastructure
- `deploy_serverless_complete.sh` - Deployment script
- `SERVERLESS_FRONTEND_DEPLOY.md` - Detailed guide

---

**Recommendation: Use Option 1 (Streamlit Cloud) for fastest deployment. Your backend is already serverless!** ✅
