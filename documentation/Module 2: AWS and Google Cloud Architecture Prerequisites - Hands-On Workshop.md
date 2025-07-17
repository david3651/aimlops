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

---

# Lab 2.2: AWS Edge Locations and CloudFront Global Network Exploration

---

## Duration
**30 minutes**

## Objective
Implement global content delivery and edge computing strategies.

---

## Prerequisites

- AWS Management Console access with infrastructure permissions
- AWS CloudShell access enabled
- Basic understanding of CDN concepts

---

## Theory Review

- AWS operates **450+ Points of Presence (PoPs)** and **13 Regional Edge Caches (RECs)** worldwide
- **Points of Presence (PoPs):** Edge locations for content caching closest to users
- **Regional Edge Caches (RECs):** Mid-tier caches between PoPs and origin servers
- **CloudFront** for content delivery network services
- **AWS Global Accelerator** for application performance optimization
- **Lambda@Edge** and **CloudFront Functions** for serverless compute at edge locations

---

## 🧪 Hands-On Lab

### Part 1: CloudFront Distribution Setup (15 minutes)

#### ✅ Step 1: Create S3 Bucket for Origin

**Navigate to S3 service in AWS Console**

1. Go to **S3 > Buckets**
2. Click **Create bucket**

**Configure S3 bucket**

- Bucket name: `ml-content-origin-[random-number]`
- Region: Keep default
- Block all public access: **Uncheck** (for demo purposes)
- Click **Create bucket**

**Upload sample content via Console**

1. Click your bucket name
2. Click **Upload**
3. Upload a sample image or HTML file
4. Click **Upload**

---

#### 🌐 Step 2: Create CloudFront Distribution via Console

**Navigate to CloudFront service**

1. Go to **CloudFront > Distributions**
2. Click **Create Distribution**

**Configure Origin settings**

- Origin domain: Select your S3 bucket
- Name: Keep default
- Origin access: Origin access control settings (recommended)
- Create new OAC if prompted

**Configure Default cache behavior**

- Viewer protocol policy: Redirect HTTP to HTTPS
- Allowed HTTP methods: GET, HEAD
- Cache policy: Caching Optimized

**Configure Distribution settings**

- Price class: Use all edge locations
- Default root object: `index.html` (if uploaded)
- Click **Create Distribution**

---

#### 🔍 Step 3: Verify Distribution via CloudShell

**List CloudFront distributions**


aws cloudfront list-distributions --query 'DistributionList.Items[*].[Id,DomainName,Status]' --output table

---

# Lab 2.3: Google Cloud Regions and Zones Architecture Analysis

---

## Duration

**45 minutes**

## Objective

Understand GCP global infrastructure and design for high availability.

---

## Prerequisites

- Google Cloud Console access with project access rights
- Cloud Shell access enabled
- Basic understanding of cloud concepts

---

## ✅ Theory Review

- Google Cloud has **42+ regions** with **127+ zones** globally
- Each region is completely independent with multiple isolated zones
- Zones are connected by Google’s private high-speed network
- Most regions consist of **3+ zones** housed in **3+ physical data centers**, with exceptions (Stockholm, Mexico, Osaka, Montreal) that are expanding to meet this requirement

---

## 🧪 Hands-On Lab

### Part 1: Infrastructure Discovery (15 minutes)

#### ✅ Step 1: Access Google Cloud Console


1. Navigate to [https://console.cloud.google.com](https://console.cloud.google.com)
2. Select your project from the project dropdown
3. Open Cloud Shell by clicking the terminal icon in the top toolbar

Step 2: Explore Available Regions and Zones via Cloud Shell

# List all regions
gcloud compute regions list --format="table(name,status,zones.len():label=ZONES)"

# Get detailed region info
gcloud compute regions describe us-central1

# List all zones
gcloud compute zones list --format="table(name,region,status)"

# Filter zones by region
gcloud compute zones list --filter="region:us-central1" --format="table(name,status)"


🔍 Step 3: Analyze Regional Capacity via Console

1. Navigate to **Compute Engine > VM instances**
2. Click **Create Instance**
3. Use the Region dropdown to observe available regions
4. Select different regions and note the zone availability
5. Cancel instance creation (do not deploy)

Step 4: Check Service Availability by Region

# Check Vertex AI availability
gcloud ai models list --region=us-central1 2>/dev/null || echo "Vertex AI not available in this region"

# Check available machine types
gcloud compute machine-types list --zones=us-central1-a --filter="name:n1-standard"

### Part 2: Multi-Zone Deployment (20 minutes)

##### ✅ Step 5: Create a Multi-Zone Managed Instance Group

1. Navigate to **Compute Engine > Instance templates**
2. Click **Create instance template**
3. Name: `ml-workload-template`
4. Machine: e2-medium
5. Boot disk: Debian GNU/Linux 11
6. Click **Create**

##### Create managed instance group via Cloud Shell:

gcloud compute instance-groups managed create ml-instance-group \
  --template=ml-workload-template \
  --zones=us-central1-a,us-central1-b,us-central1-c \
  --target-distribution-shape=BALANCED \
  --size=3

##### Configure auto-scaling:

gcloud compute instance-groups managed set-autoscaling ml-instance-group \
  --region=us-central1 \
  --max-num-replicas=6 \
  --min-num-replicas=3 \
  --target-cpu-utilization=0.6

#### Step 6: Test Zone Distribution via Console

1. Navigate to **Compute Engine > Instance groups**
2. Click on `ml-instance-group`
3. Observe instance distribution across zones in the **Details** tab

#### Step 7: Configure Health Checks

gcloud compute health-checks create http ml-health-check \
  --port=80 \
  --request-path=/health \
  --check-interval=30s \
  --timeout=10s \
  --healthy-threshold=2 \
  --unhealthy-threshold=3

gcloud compute instance-groups managed update ml-instance-group \
  --region=us-central1 \
  --health-check=ml-health-check


### Part 3: Zone Failure Simulation (10 minutes)

#### ⚠️ Step 8: Simulate Zone Outage

##### View current instance distribution:


```python
gcloud compute instances list --filter="name:ml-instance-group*" --format="table(name,zone,status)"
```
##### Simulate zone failure via Console:

1. Navigate to **Compute Engine > VM instances**
2. Select instances in `us-central1-a`
3. Click **Delete** (simulate outage)

##### Monitor auto-healing:


```python
watch -n 10 'gcloud compute instance-groups managed describe ml-instance-group --region=us-central1 --format="value(status)"'
```


##### ✅ Step 9: Verify High Availability

##### Check instance redistribution:

```python
gcloud compute instances list --filter="name:ml-instance-group*" --format="table(name,zone,status)"
```

View instance group events via Console:


1. Navigate to **Compute Engine > Instance groups**
2. Click `ml-instance-group`
3. Go to the **Monitoring** tab for scaling events
Regional Resource Strategy Design
🌐 Step 10: Multi-Region Planning
Identify optimal ML regions:


gcloud compute accelerator-types list --format="table(name,zone)" | grep "nvidia-tesla"
Analyze regional pricing via Console:


1. Navigate to **Billing > Pricing**
2. Compare **Compute Engine pricing** across regions
3. Document cost differences
Plan DR regions with 3+ zones:


gcloud compute regions list --format="table(name,zones.len():label=ZONES)" --filter="zones.len()>=3"

📦 Deliverables

1. Zone Availability Matrix
Region names and zone counts

Service availability by region

Machine type availability

GPU/TPU availability

2. Multi-Zone Deployment Architecture
Instance group setup

Zone distribution strategy

Auto-scaling configuration

Health check implementation

Failure recovery behavior

3. Regional Deployment Strategy Document
Primary and secondary region selection

Disaster recovery planning

Cost optimization opportunities

Compliance and data residency considerations

🧹 Cleanup
Remove created resources via Cloud Shell:


# Delete managed instance group
gcloud compute instance-groups managed delete ml-instance-group --region=us-central1 --quiet

# Delete instance template
gcloud compute instance-templates delete ml-workload-template --quiet

# Delete health check
gcloud compute health-checks delete ml-health-check --quiet


✅ Accuracy Notes

CLI commands and infrastructure counts reflect GCP state as of 2025

All queries are beginner-friendly and verified for Cloud Shell

Console navigation is simplified and current

GCP has 42+ regions and 127+ zones

Cleanup commands use --quiet to suppress prompts

🧠 Key Learning Points

Regional Independence: Each GCP region has isolated failure domains

Zone Distribution: Spread workloads for availability

Auto-healing: Managed groups replace failed instances

Service Variations: Not all services available in all regions

Cost Considerations: Pricing varies across regions

Infrastructure Standards: Most regions host 3+ zones in 3+ physical data centers

---

# Lab 2.4: Google Cloud Edge Network and Cloud CDN Exploration

---

## Duration

**30 minutes**

## Objective

Implement global content delivery using Google's edge network.

---

## Prerequisites

- Google Cloud Console access with project access rights
- Cloud Shell access enabled
- Basic understanding of CDN concepts

---

## Theory Review

- Google Cloud operates **202+ network edge locations** across 200+ countries and territories
- **Cloud CDN:** 100+ cache locations for content delivery
- **Media CDN:** 3,000+ locations for video streaming and large file downloads
- Global load balancing with **Anycast IP addresses**
- Integration with Google’s private global network backbone


## 🧪 Hands-On Lab

### Part 1: Cloud Storage Setup for CDN Origin (10 minutes)

#### ✅ Step 1: Create Cloud Storage Bucket via Console

**Navigate to Cloud Storage:**

1. Go to **Cloud Storage > Buckets**
2. Click **Create bucket**

**Configure Storage Bucket:**

- Name: `ml-cdn-content-[random-number]`
- Location type: Multi-region
- Default storage class: Standard
- Access control: Fine-grained
- Click **Create**

**Upload Sample Content:**

1. Click your bucket name
2. Click **Upload files**
3. Upload an image, video, or HTML file
4. Click **Upload**

**Make Content Publicly Accessible:**

1. Select the uploaded file
2. Click **Permissions** tab
3. Click **Grant access**
4. New principals: `allUsers`
5. Role: `Storage Object Viewer`
6. Click **Save**


### Part 2: Cloud CDN Configuration (15 minutes)

#### 🌐 Step 2: Create HTTP Load Balancer with CDN via Console

**Navigate to Load Balancing:**

1. Go to **Network Services > Load balancing**
2. Click **Create load balancer**

**Choose Load Balancer Type:**

- Select **Global external Application Load Balancer**
- Click **Configure**

**Configure Backend (Enable Cloud CDN):**

- Name: `ml-cdn-backend`
- Backend type: Cloud Storage bucket
- Cloud Storage bucket: Select your bucket
- Enable **Cloud CDN**
- Cache mode: `CACHE_ALL_STATIC`
- Default TTL: `3600 seconds`

**Configure Frontend:**

- Name: `ml-cdn-frontend`
- Protocol: HTTP
- Port: 80
- IP Address: Create IP address (`ml-cdn-ip`)

**Review and Create:**

- Name: `ml-cdn-lb`
- Click **Create**


#### 🔍 Step 3: Verify CDN Configuration via Cloud Shell

**List Load Balancers:**

```python
gcloud compute url-maps list --format="table(name,defaultService)"

gcloud compute url-maps describe ml-cdn-lb --global

gcloud compute backend-services list --global --format="table(name,enableCDN,cdnPolicy.cacheMode)"

Part 3: CDN Performance Testing (5 minutes)
```

📊 Step 4: Test CDN Performance via Cloud Shell

Get Load Balancer IP:

```python

LB_IP=$(gcloud compute addresses describe ml-cdn-ip --global --format="value(address)")
echo "Load Balancer IP: $LB_IP"
```

Test CDN Cache Behavior:

# First request (cache miss)
```python
echo "First request (cache miss):"
curl -I http://$LB_IP/your-file.jpg | grep -E "(HTTP|Cache-Control|Age|X-Cache)"
```

# Second request (cache hit)
```python
echo "Second request (cache hit):"
curl -I http://$LB_IP/your-file.jpg | grep -E "(HTTP|Cache-Control|Age|X-Cache)"
```

Test Global Distribution:

```python
curl -o /dev/null -s -w "Total time: %{time_total}s\n" http://$LB_IP/your-file.jpg
```

🌍 Step 5: Configure Custom Domain and SSL via Console
1. **Reserve Global IP Address:**
   - Go to **VPC Network > IP addresses**
   - Click **Reserve external static address**
   - Name: `ml-cdn-ssl-ip`
   - Type: Global
   - Click **Reserve**

2. **Create SSL Certificate (Recommended: Google-managed):**
   - Go to **Network Security > SSL certificates**
   - Click **Create SSL certificate**
   - Name: `ml-cdn-ssl-cert`
   - Mode: Google-managed
   - Domains: Enter your domain name
   - Click **Create**
3. **Update Load Balancer for HTTPS:**
   - Go to **Network Services > Load balancing**
   - Click on `ml-cdn-lb`
   - Click **Edit**
   - Add new frontend:
     - Name: `ml-cdn-https-frontend`
     - Protocol: HTTPS
     - Port: 443
     - IP address: `ml-cdn-ssl-ip`
     - Certificate: `ml-cdn-ssl-cert`
   - Click **Update**
---
