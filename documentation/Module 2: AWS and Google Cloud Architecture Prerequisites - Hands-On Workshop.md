# MLOPS Model Migration Workshop – Week 2: AWS & Google Cloud Architecture Essentials - Hands-On Workshop

---

## Module Learning Objectives

By the end of this workshop, participants will be able to:

- Compare and contrast AWS and Google Cloud global infrastructure architectures
- Design topologies across both platforms
- Map AWS services to Google Cloud service equivalents for AI/ML pipeline workloads
- Implement basic IAM configurations for secure ML environments

---

## Prerequisites

- Completion of Module 1: Cost Management Foundation
- AWS Management Console access with infrastructure permissions
- Google Cloud Console access with project access rights

---

## Workshop Overview

This hands-on workshop builds upon the cost management foundation from Module 1 to establish the technical architecture knowledge required for successful AWS to Google Cloud ML migrations. Using **console interfaces** and **CloudShell**, participants will gain practical experience with infrastructure services, networking, and IAM configurations across both platforms.

---

## Module 1: AWS Global Infrastructure and Core Resources

### Lab 2.1: AWS Regions and Availability Zones Architecture Deep Dive

- **Duration:** 45 minutes
- **Objective:** Understand AWS global infrastructure and design for high availability

### Lab Prerequisites

- AWS Management Console access with infrastructure permissions
- AWS CloudShell access enabled
- Basic understanding of cloud concepts

---

## 🧪 Hands-On Lab

---

### Part 1: Region Explorer (15 minutes)

#### ✅ Step 1: Access AWS Management Console

```markdown
1. Open your web browser
2. Navigate to [https://console.aws.amazon.com](https://console.aws.amazon.com)
3. Sign in to your AWS account
4. Open CloudShell by clicking the terminal icon
5. Use the Search Bar to enter `EC2` and select the EC2 service

#### ✅ Step 2: List All Regions via CloudShell

aws ec2 describe-regions --output table

aws ec2 describe-regions --query 'Regions[*].[RegionName,OptInStatus]' --output table

aws ec2 describe-regions --query 'length(Regions)' --output text

#### Step 3: Explore Region Details via Console

1. Use the AWS Console Search Bar to enter `EC2`
2. Select the EC2 service
3. In the top-right corner, click the Region selector
4. Review available regions and note those labeled “Opt-in required”

#### Step 4: Analyze Availability Zones

1. Current region AZs
aws ec2 describe-availability-zones --output table

2. Specific region example
aws ec2 describe-availability-zones --region us-east-1 --output table

3. Count AZs per region
aws ec2 describe-regions --query 'Regions[*].RegionName' --output text | \
while read region; do
  count=$(aws ec2 describe-availability-zones --region $region \
  --query 'length(AvailabilityZones)' --output text 2>/dev/null || echo "0")
  echo "$region: $count AZs"
done
