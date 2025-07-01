# Week 1: Introduction and Foundation Setup - Hands-On Workshop

---

## 🚀 Migration Overview and Business Case

### Module Learning Objectives

By the end of this workshop, participants will be able to:

- Analyze current AWS costs and identify optimization opportunities using AWS Console
- Navigate Google Cloud Console billing and cost management tools effectively
- Build a compelling business case for SageMaker to Vertex AI migration
- Establish cost baselines and tracking mechanisms for migration success

### Prerequisites

- AWS Management Console access with billing permissions
- Google Cloud Console access with billing account access
- Basic AWS and Google Cloud knowledge
- Web browser (Chrome, Firefox, Safari, or Edge)

### Workshop Overview

This comprehensive workshop establishes the financial foundation for migrating AWS SageMaker workloads to Google Cloud Vertex AI. Participants will master cost management tools on both platforms using only web-based console interfaces and develop compelling business cases for migration decisions.

---

## 💰 Lab 1.1: AWS Cost Management Tools Exploration and Analysis

### Lab Information

- Duration: 4 hours
- Tools Required: AWS Management Console, web browser, spreadsheet application
- Difficulty: Intermediate

### Lab Objectives

- Master AWS Cost Explorer and AWS Budgets for SageMaker workloads
- Analyze current SageMaker spending patterns and trends
- Identify cost optimization opportunities in existing ML infrastructure
- Create detailed cost breakdown for migration planning

---

## Section 1: AWS Cost Explorer Deep Dive (60 minutes)

### Step 1.1: Access and Navigate AWS Cost Explorer (15 minutes)

#### 🎯 Goal

Set up and familiarize yourself with the AWS Cost Explorer interface.

#### Instructions

1. Open your web browser
2. Navigate to the AWS Cost Management Console
3. Sign in with your AWS credentials
4. In the left navigation pane, select **Cost Explorer**
5. Click **Launch Cost Explorer** if you’re a first-time user (may take up to 24 hours for data processing)

#### Initial Cost Explorer Setup

**Setup Checklist:**

- Once loaded, verify you can see the main dashboard
- Set time range to “Last 13 months” using the date picker in the top right
- Set granularity to “Monthly” from the dropdown menu
- Group by “Service” from the “Group by” dropdown
- Enable the **Forecast** toggle at the bottom of the chart

#### Interface Familiarization

- Explore the main dashboard chart area
- Review chart type options (bar, line, stacked) using the chart controls
- Examine the filters panel on the left side
- Test the new Cost Comparison feature by clicking **Compare** in the Report Parameters panel

💡 Pro Tip: Use preconfigured views like “Monthly costs by service” or “RI Utilization” to accelerate insights. Take screenshots of your initial dashboard view for comparison later in the workshop.

### Step 1.2: SageMaker Cost Analysis (25 minutes)

⚠️ Important: Focus specifically on SageMaker services to understand current ML spending patterns.

#### 1. Filter for SageMaker Services

1. In the Filters panel, click on **Service**
2. Type “SageMaker” to search
3. Select **Amazon SageMaker** from the results
4. Click **Apply filters**
5. Adjust time range to “Last 6 months”
6. Change granularity to “Daily”

#### 2. Analyze SageMaker Cost Components

1. Change “Group by” to **Usage Type**
2. Review the chart to identify top cost drivers
3. Click on chart segments to drill down
4. Use Cost Comparison to compare current vs. previous month
5. Document findings in a spreadsheet

#### 3. Create Cost Breakdown Analysis

Create a table in your spreadsheet with this structure:

| Component           | Monthly Cost | % of Total | Trend   | Instance Types/Notes       |
|---------------------|--------------|------------|---------|----------------------------|
| Training Instances  | $X,XXX       | XX%        | ↑/↓/→   | ml.p3.2xlarge, ml.g5.xlarge |
| Notebook Instances  | $XXX         | XX%        | ↑/↓/→   | Development environments   |
| Endpoints           | $X,XXX       | XX%        | ↑/↓/→   | Production model serving   |
| Storage (S3)        | $XXX         | XX%        | ↑/↓/→   | Training data, models      |
| Data Transfer       | $XXX         | XX%        | ↑/↓/→   | Inter-region, internet     |
| Other Services      | $XXX         | XX%        | ↑/↓/→   | Supporting AWS services    |

#### 4. Document Key Findings

Answer these questions based on your analysis:

- Which instance types consume the most budget?
- What time periods show highest usage patterns?
- Are there obvious idle periods or unused resources?
- What’s the ratio between training costs vs. inference costs?

### Step 1.3: Advanced Cost Analysis Techniques (20 minutes)

#### 1. Usage Pattern Analysis

- Change granularity to “Hourly” for the most recent week
- Identify peak usage times and patterns
- Look for consistent idle resource patterns
- Switch back to “Daily” view to document seasonal variations
- Test Amazon Q Developer queries (e.g., “Which region had the largest cost increase last month?”)

#### 2. Explore Additional Filters

Experiment with these filters:

- Region: Concentration of SageMaker usage by region
- Usage Type: Filter by instance type (e.g., ml.m5.large)
- Linked Account: Analyze usage across AWS Organization accounts

#### 3. Cost Anomaly Detection Review

Note: Cost Anomaly Detection is automatically configured for new accounts as of March 2025.

1. In the AWS Console search bar, type “Cost Anomaly Detection”
2. Navigate to the service’s overview dashboard
3. Review any existing anomalies
4. Check the AWS Services monitor that was auto-created
5. Review daily email alert subscriptions
6. Click individual anomalies to investigate
7. Document patterns for optimization

💡 Pro Tip: Look for consistent patterns of unused resources during off-hours or weekends—immediate optimization opportunities.

## Section 2: AWS Budgets and Alerts Configuration (45 minutes)

---

### Step 2.1: Create SageMaker-Specific Budget (20 minutes)

#### 1. Navigate to AWS Budgets

- In the AWS Console search bar, type “Budgets”
- Select “AWS Budgets” from the search results
- Click the **Create budget** button

#### 2. Configure Cost Budget

**Budget setup:**

- Under **Budget setup**, choose **Customize (advanced)**
- Budget type: **Cost budget**
- Budget name: `SageMaker-ML-Workloads-Monthly`
- Period: **Monthly**
- Budget renewal type: **Recurring budget**
- Start month: Current month

**Set budget amount:**

- Budgeting method: **Fixed**
- Enter amount: `$[Current monthly SageMaker spend + 20% buffer]`
- Advanced options: **Unblended costs**

**Budget scope (Filters):**

1. Click **Add filter**
2. Select **Service** from the dropdown
3. Choose **Amazon SageMaker**
4. Click **Add filter** again if needed for other services

#### 3. Configure Alert Thresholds

1. Click **Next** to proceed to alert configuration
2. Set up multiple alerts:

   - **Alert 1 – Early Warning**
     - Threshold: 75%
     - Type: **Forecasted**
     - Recipients: ML team leads’ emails

   - **Alert 2 – Critical Alert**
     - Click **Add an alert threshold**
     - Threshold: 90%
     - Type: **Actual**
     - Recipients: Additional stakeholders

   - **Alert 3 – Budget Exceeded**
     - Click **Add an alert threshold**
     - Threshold: 100%
     - Type: **Actual**
     - Recipients: Management escalation contacts

**Enhanced Alert Options (2025 Feature):**

- Check **AWS User Notifications**
- Configure AWS Chatbot alerts for Slack/Chime if available

3. Click **Next**, review configuration, then **Create budget**

---

### Step 2.2: Advanced Budget Configuration (25 minutes)

#### 1. Create Environment-Specific Budgets

**Development Environment Budget:**

- Return to the Budgets dashboard and click **Create budget**
- Select **Customize (advanced)** → **Cost budget**
- Budget name: `ML-Development-Environment`
- Period: **Monthly**
- Method: **Fixed**
- Amount: `$500`
- Filters:
  - Tags: `Environment:Development`
  - Service: Amazon SageMaker

**Production Environment Budget:**

- Click **Create budget** again
- Budget name: `ML-Production-Environment`
- Period: **Monthly**
- Method: **Fixed**
- Amount: `$5,000`
- Filters focused on production resources

#### 2. Budget Actions Configuration (2025 Feature)

1. In the budget creation wizard, scroll to **Actions**
2. Click **Add action**
3. Configure automated response:
   - Action type: Apply IAM policy or target EC2/RDS instances
   - Threshold: 90% actual spend
   - Execution: Require approval (recommended) or Automatic
4. Define policy or instance targeting criteria

#### 3. Budget Monitoring Setup

- Navigate to the main Budgets dashboard
- Review all created budgets in list view
- Click each budget name to verify settings
- Check the **Actions** column for status
- Test email delivery with a low threshold (e.g., 1%)
- Document the monitoring process

---

## Lab 1.1 Deliverables Checklist

- AWS cost analysis report with detailed SageMaker breakdown
- Configured AWS budgets with alert thresholds and actions
- Optimization recommendations document
- Ongoing monitoring process documentation
- Baseline cost data for GCP migration comparison

---

## ☁️ Lab 1.2: Google Cloud Console Cost Management and Billing Tools Deep Dive

---

### Lab Information

- Duration: 4 hours
- Tools Required: Google Cloud Console only, web browser, spreadsheet application
- Difficulty: Intermediate

### Lab Objectives

- Master Google Cloud billing and cost management tools using console interface only
- Understand GCP pricing models for Vertex AI and supporting services
- Implement cost controls and monitoring for GCP ML workloads through console
- Create comprehensive cost comparison framework between AWS and GCP

---

## Section 1: Google Cloud Billing Console Deep Dive (60 minutes)

### Step 1.1: Billing Account Setup and Navigation (20 minutes)

1. Open your web browser
2. Navigate to the Google Cloud Console
3. Sign in with your Google Cloud credentials
4. Click the billing menu icon (💳) in the top navigation bar
5. Select your billing account from the dropdown

#### Billing Account Configuration Review

- In the left sidebar, click **Account management**
- Verify permissions:
  - Click **Account permissions**
  - Confirm your billing role (Administrator, User, or Viewer)
  - Document your access level
- Review account hierarchy:
  - Note any linked projects
  - Understand billing account structure
- Check payment settings:
  - Click **Payment settings**
  - Review payment methods
  - Verify automatic payment and billing alerts

#### Initial Billing Dashboard Overview

- Click **Overview** in the left sidebar
- Review current month spending:
  - Note total month-to-date spend
  - Identify top spending services
  - Check spending trends chart
  - Use Gemini Cloud Assist for AI-powered cost insights (if available)
- Analyze service-level breakdown:
  - Review services cost chart
  - Click chart segments for details
- Check project-level allocation:
  - Review costs by project
  - Note any ML-related projects

---

### Step 1.2: Cloud Billing Reports Analysis (25 minutes)

1. In the left sidebar, navigate to **Cost management** → **Reports**
2. Familiarize yourself with the Reports interface

#### Configure Analysis View

- Set time range: **Last 6 months**
- Group by options:
  - Service (default)
  - Project
  - Project hierarchy (folder-level)
  - SKU for detailed analysis
- Apply filters:
  - Projects, Services, SKUs, Locations, Labels
  - Folders & Organizations for ancestry analysis

#### Analyze Current GCP Usage for ML Services

- Filter for AI/ML services:
  - Vertex AI
  - Compute Engine
  - Cloud Storage
  - Container Registry
- Document current baseline:
  - Create a baseline cost matrix
  - Note usage patterns for storage and compute

#### Enhanced Report Features (2025)

- Save custom view:
  - Click **Save as new**, name “ML Migration Baseline”
  - Set as regular monitoring view
- Export capabilities:
  - Click **Export** → **Download CSV**
  - Save for AWS comparison

---

### Step 1.3: Advanced Billing Analysis Features (15 minutes)

#### Custom Time Ranges and Detailed Views

- Experiment with date picker:
  - “Last 30 days” for recent patterns
  - “Last 12 months” for trends
- Change granularity:
  - Monthly ↔ Daily to observe usage variation

#### Enhanced Savings and Credits Analysis (2025)

- Navigate to **Savings** (formerly Discounts and credits)
- Review subcategories:
  - Committed use discounts
  - Sustained use discounts

#### Export and Save Capabilities

- Export data:
  - Click **Export** → **Download CSV**
- Create saved reports:
  - Click **Save as new**, name “ML Migration Baseline”
  - Set as regular monitoring view

---

### Step 1.4: GCP Cost Projection Matrix

Create this table in your spreadsheet for future ML workload planning:

| Service Category       | Current Monthly Cost | Projected ML Cost | Migration Notes                  |
|------------------------|----------------------|-------------------|----------------------------------|
| Vertex AI Training     | $0                   | $X,XXX            | Based on AWS SageMaker analysis  |
| Vertex AI Prediction   | $0                   | $XXX              | Endpoint hosting equivalent      |
| Compute Engine         | $XXX                 | $X,XXX            | Custom training VMs              |
| Cloud Storage          | $XXX                 | $XXX              | Data storage migration           |
| Networking             | $XXX                 | $XXX              | Data transfer and egress         |
| Other Services         | $XXX                 | $XXX              | Supporting infrastructure        |
