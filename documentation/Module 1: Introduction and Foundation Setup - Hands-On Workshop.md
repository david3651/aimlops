# Module 1: Introduction and Foundation Setup - Hands-On Workshop

## 🚀 Migration Overview and Business Case

### **Module Learning Objectives**
By the end of this workshop, participants will be able to:
- Analyze current AWS costs and identify optimization opportunities using AWS Console
- Navigate Google Cloud Console billing and cost management tools effectively
- Build a compelling business case for SageMaker to Vertex AI migration
- Establish cost baselines and tracking mechanisms for migration success

### **Prerequisites**
- AWS Management Console access with billing permissions
- Google Cloud Console access with billing account access
- Basic AWS and Google Cloud knowledge
- Web browser (Chrome, Firefox, Safari, or Edge)

### **Workshop Overview**
This comprehensive workshop establishes the financial foundation for migrating AWS SageMaker workloads to Google Cloud Vertex AI. Participants will master cost management tools on both platforms using only web-based console interfaces and develop compelling business cases for migration decisions.

---

## 💰 Lab 1.1: AWS Cost Management Tools Exploration and Analysis

### **Lab Information**
- **Duration:** 4 hours
- **Tools Required:** AWS Management Console, web browser, spreadsheet application
- **Difficulty:** Intermediate

### **Lab Objectives**
- Master AWS Cost Explorer and AWS Budgets for SageMaker workloads
- Analyze current SageMaker spending patterns and trends
- Identify cost optimization opportunities in existing ML infrastructure
- Create detailed cost breakdown for migration planning

---

## Section 1: AWS Cost Explorer Deep Dive (60 minutes)

### Step 1.1: Access and Navigate AWS Cost Explorer (15 minutes)

#### **🎯 Goal:** Set up and familiarize yourself with AWS Cost Explorer interface

**1. Log into AWS Management Console**
1. Open your web browser
2. Navigate to: [AWS Management Console](https://console.aws.amazon.com)
3. Sign in with your AWS credentials
4. In the search bar at the top, type "Cost Explorer" and select it from the results
5. Alternatively, navigate to: **Services** → **AWS Cost Management** → **Cost Explorer**

**2. Initial Cost Explorer Setup**

**Setup Checklist:**
- [ ] Click "Launch Cost Explorer" if first-time user (may take up to 24 hours for data processing)
- [ ] Once loaded, verify you can see the main dashboard
- [ ] Set time range to "Last 12 months" using the date picker in the top right
- [ ] Set granularity to "Monthly" from the dropdown menu
- [ ] Group by "Service" from the "Group by" dropdown

**3. Interface Familiarization**
- Explore the main dashboard chart area
- Review chart type options (bar, line, stacked) using the chart controls
- Examine the filters panel on the left side
- Check the forecast feature toggle at the bottom of the chart

> **💡 Pro Tip:** Take screenshots of your initial dashboard view for comparison later in the workshop.

### Step 1.2: SageMaker Cost Analysis (25 minutes)

#### **⚠️ Important:** Focus specifically on SageMaker services to understand current ML spending patterns

**1. Filter for SageMaker Services**
1. In the left panel under "Filters", click on "Service"
2. In the Service filter dropdown, type "SageMaker" to search
3. Select "Amazon SageMaker" from the filtered results
4. Click "Apply filters"
5. Adjust time range to "Last 6 months" using the date picker
6. Change granularity to "Daily" to see more detailed patterns

**2. Analyze SageMaker Cost Components**
1. Change the "Group by" setting to "Usage Type"
2. Review the resulting chart to identify top cost drivers
3. Click on individual chart segments to drill down into details
4. Document findings in a spreadsheet table

**3. Create Cost Breakdown Analysis**

Create a table in your spreadsheet with the following structure:

| Component | Monthly Cost | % of Total | Trend | Instance Types/Notes |
|-----------|--------------|------------|-------|---------------------|
| Training Instances | $X,XXX | XX% | ↑/↓/→ | ml.p3.2xlarge, ml.m5.large |
| Notebook Instances | $XXX | XX% | ↑/↓/→ | Development environments |
| Endpoints | $X,XXX | XX% | ↑/↓/→ | Production model serving |
| Storage (S3) | $XXX | XX% | ↑/↓/→ | Training data, models |
| Data Transfer | $XXX | XX% | ↑/↓/→ | Inter-region, internet |
| Other Services | $XXX | XX% | ↑/↓/→ | Supporting AWS services |

**4. Document Key Findings**
Answer these questions based on your analysis:
- Which instance types consume the most budget?
- What time periods show highest usage patterns?
- Are there obvious idle periods or unused resources?
- What's the ratio between training costs vs. inference costs?

### Step 1.3: Advanced Cost Analysis Techniques (20 minutes)

**1. Usage Pattern Analysis**

**Analysis Tasks:**
- [ ] Change granularity to "Hourly" for the most recent week
- [ ] Identify peak usage times and patterns in the hourly view
- [ ] Look for consistent idle resource patterns
- [ ] Switch back to "Daily" view and document any seasonal variations

**2. Explore Additional Filters**
1. In the Filters panel, experiment with additional filters:
  - **Region**: Check if SageMaker usage is concentrated in specific regions
  - **Usage Type**: Filter to specific instance types (e.g., ml.m5.large)
  - **Linked Account**: If using AWS Organizations, analyze by account

**3. Cost Anomaly Detection**
1. In the AWS Console search bar, type "Cost Anomaly Detection"
2. Navigate to the Cost Anomaly Detection service
3. Review the overview dashboard for any existing anomalies
4. Click on individual anomalies to understand unusual spending patterns
5. Document any patterns that could be optimized

> **💡 Pro Tip:** Look for consistent patterns of unused resources during off-hours or weekends - these represent immediate optimization opportunities.

---

## Section 2: AWS Budgets and Alerts Configuration (45 minutes)

### Step 2.1: Create SageMaker-Specific Budget (20 minutes)

**1. Navigate to AWS Budgets**
1. In the AWS Console search bar, type "Budgets"
2. Select "AWS Budgets" from the search results
3. Click "Create budget" button

**2. Configure Cost Budget**
1. **Budget setup**:
  - Budget type: Select "Cost budget"
  - Budget name: Enter "SageMaker-ML-Workloads-Monthly"
  - Period: Select "Monthly"
  - Start month: Choose current month

2. **Set budget amount**:
  - Budget method: Select "Fixed"
  - Enter amount: $[Current monthly SageMaker spend + 20% buffer]

3. **Budget scope (Filters)**:
  - Click "Add filter"
  - Select "Service" from dropdown
  - Choose "Amazon SageMaker"
  - Click "Add filter" again if needed for additional services

**3. Configure Alert Thresholds**
1. Click "Next" to proceed to alert configuration
2. Set up multiple alerts:

  **Alert 1 - Early Warning:**
  - Alert threshold: 75%
  - Threshold type: "Forecasted"
  - Email recipients: Enter ML team leads' email addresses

  **Alert 2 - Critical Alert:**
  - Click "Add an alert threshold"
  - Alert threshold: 90%
  - Threshold type: "Actual"
  - Email recipients: Add additional stakeholders

  **Alert 3 - Budget Exceeded:**
  - Click "Add an alert threshold"
  - Alert threshold: 100%
  - Threshold type: "Actual"
  - Email recipients: Include management escalation contacts

4. Click "Next" and review your budget configuration
5. Click "Create budget" to finalize

### Step 2.2: Advanced Budget Configuration (25 minutes)

**1. Create Environment-Specific Budgets**

**Development Environment Budget:**
1. Return to the Budgets dashboard and click "Create budget"
2. Configuration:
  - Budget name: "ML-Development-Environment"
  - Amount: $500/month
  - Add additional filters:
    - **Tags**: If using environment tags, filter for "Environment:Development"
    - **Service**: Amazon SageMaker

**Production Environment Budget:**
1. Create another budget with:
  - Budget name: "ML-Production-Environment"
  - Amount: $5,000/month
  - Filters focused on production resources

**2. Budget Monitoring Setup**
1. Navigate back to the main Budgets dashboard
2. Review all created budgets in the list view
3. Click on each budget name to verify configuration
4. Test email delivery by temporarily setting a very low threshold (like 1%)
5. Document the budget monitoring process

---

## Lab 1.1 Deliverables Checklist
- [ ] AWS cost analysis report with detailed SageMaker breakdown
- [ ] Configured AWS budgets with appropriate alert thresholds
- [ ] Optimization recommendations document with specific actions
- [ ] Ongoing monitoring process documentation
- [ ] Baseline cost data for GCP migration comparison

---

## ☁️ Lab 1.2: Google Cloud Console Cost Management and Billing Tools Deep Dive

### **Lab Information**
- **Duration:** 4 hours
- **Tools Required:** Google Cloud Console only, web browser, spreadsheet application
- **Difficulty:** Intermediate

### **Lab Objectives**
- Master Google Cloud billing and cost management tools using console interface only
- Understand GCP pricing models for Vertex AI and supporting services
- Implement cost controls and monitoring for GCP ML workloads through console
- Create comprehensive cost comparison framework between AWS and GCP

---

## Section 1: Google Cloud Billing Console Deep Dive (60 minutes)

### Step 1.1: Billing Account Setup and Navigation (20 minutes)

**1. Access Google Cloud Billing Console**
1. Open your web browser
2. Navigate to: [Google Cloud Console](https://console.cloud.google.com)
3. Sign in with your Google Cloud credentials
4. Click the billing menu icon (💳) in the top navigation bar
5. Select your billing account from the dropdown

**2. Billing Account Configuration Review**
1. In the left sidebar, click "Account management"
2. **Verify permissions**:
  - Click "Account permissions"
  - Confirm you have appropriate billing roles
  - Document your access level (Administrator, User, or Viewer)
3. **Review account hierarchy**:
  - Note any linked projects
  - Understand the billing account structure
4. **Check payment settings**:
  - Click "Payment settings" in the left sidebar
  - Review payment methods
  - Check automatic payment settings and billing alerts

**3. Initial Billing Dashboard Overview**
1. Click "Overview" in the left sidebar
2. **Review current month spending**:
  - Note total month-to-date spending
  - Identify top spending services
  - Check spending trends chart
3. **Analyze service-level breakdown**:
  - Review the services cost chart
  - Click on chart segments for detailed views
4. **Check project-level allocation**:
  - Review costs by project
  - Note any existing ML-related projects

### Step 1.2: Cloud Billing Reports Analysis (25 minutes)

**1. Navigate to Billing Reports**
1. In the billing console left sidebar, click "Reports"
2. Familiarize yourself with the Reports interface

**2. Configure Analysis View**
1. **Set time range**: Click the date picker and select "Last 6 months"
2. **Group by options**: Experiment with different grouping:
  - Group by "Service" (default)
  - Group by "Project"
  - Group by "SKU" for detailed analysis
3. **Apply filters**:
  - Click "Filters" to explore available options
  - Note filter categories: Projects, Services, SKUs, Locations, Labels

**3. Analyze Current GCP Usage for ML Services**
1. **Filter for AI/ML related services**:
  - Click "Filters" → "Services"
  - Look for any existing usage of:
    - Vertex AI (if any current usage)
    - Compute Engine
    - Cloud Storage
    - Container Registry
2. **Document current baseline**:
  - Create a baseline cost matrix for existing services
  - Note any patterns in usage
  - Identify current storage and compute patterns

**4. Create GCP Cost Projection Matrix**

Create a table in your spreadsheet for future ML workload planning:

| Service Category | Current Monthly Cost | Projected ML Cost | Migration Notes |
|------------------|---------------------|-------------------|-----------------|
| Vertex AI Training | $0 | $X,XXX | Based on AWS SageMaker analysis |
| Vertex AI Prediction | $0 | $XXX | Endpoint hosting equivalent |
| Compute Engine | $XXX | $X,XXX | Custom training VMs |
| Cloud Storage | $XXX | $XXX | Data storage migration |
| Networking | $XXX | $XXX | Data transfer and egress |
| Other Services | $XXX | $XXX | Supporting infrastructure |

### Step 1.3: Advanced Billing Analysis Features (15 minutes)

**1. Custom Time Ranges and Detailed Views**
1. **Experiment with time ranges**:
  - Use date picker to set custom periods
  - Try "Last 30 days" for recent patterns
  - Switch to "Last 12 months" for trends
2. **Granularity options**:
  - Change view from Monthly to Daily
  - Observe usage patterns and variations

**2. Export and Save Capabilities**
1. **Export data**:
  - Click "Export" button
  - Choose "Download CSV" for offline analysis
  - Save for comparison with AWS data
2. **Create saved reports**:
  - Click "Save" to create a custom report view
  - Name it "ML Migration Baseline"
  - Set as a regular monitoring view

---

## Section 2: Google Cloud Budgets and Alerts Configuration (45 minutes)

### Step 2.1: Create ML Workload Budget (20 minutes)

**1. Navigate to Budget Creation**
1. In the billing console left sidebar, click "Budgets & alerts"
2. Click "Create budget" button

**2. Budget Scope and Configuration**
1. **Budget details**:
  - Name: "Vertex-AI-ML-Workloads"
  - Time range: "Monthly"
  - Start date: Select current month
2. **Budget scope**:
  - **Projects**: Select "All projects" or specific ML projects
  - **Services**: Click "Add filter" → "Services"
    - Select relevant services for ML workloads:
      - Vertex AI
      - Compute Engine
      - Cloud Storage
  - **Other filters**: Leave as "All" for comprehensive monitoring

**3. Set Budget Amount**
1. **Budget amount**:
  - Type: "Specified amount"
  - Amount: $[Enter estimated monthly ML spend based on AWS analysis]
  - Currency: Verify correct currency

**4. Configure Alert Thresholds**
1. Click "Next" to proceed to alert configuration
2. **Set up multiple alert rules**:

  **Alert 1 - Early Warning (50%)**:
  - Threshold: 50%
  - Trigger on: "Actual spend"
  - Email notifications: Check "Email alerts to billing admins and users"

  **Alert 2 - Planning Alert (75%)**:
  - Click "Add threshold"
  - Threshold: 75%
  - Trigger on: "Actual spend"

  **Alert 3 - Critical Alert (90%)**:
  - Click "Add threshold"
  - Threshold: 90%
  - Trigger on: "Actual spend"

  **Alert 4 - Forecasted Overage (100%)**:
  - Click "Add threshold"
  - Threshold: 100%
  - Trigger on: "Forecasted spend"

3. Click "Finish" to create the budget

### Step 2.2: Environment-Specific Budget Setup (25 minutes)

**1. Create Development Environment Budget**
1. Click "Create budget" again
2. **Configuration**:
  - Name: "ML-Development-Environment"
  - Amount: $500/month
  - **Scope filtering**:
    - Projects: Select development/testing projects only
    - Services: Focus on Vertex AI and Compute Engine
  - **Alert thresholds**: 50%, 75%, 90%

**2. Create Production Environment Budget**
1. Create a third budget:
  - Name: "ML-Production-Environment"
  - Amount: $5,000/month
  - **Scope**: Production projects and prediction services
  - **Alert thresholds**: More conservative (25%, 50%, 75%, 90%)

**3. Budget Dashboard Review**
1. **Navigate back to Budgets & alerts main page**
2. **Review all created budgets**:
  - Verify budget names and amounts
  - Check alert configuration
  - Note budget status and current spend against limits
3. **Test alert functionality**:
  - Temporarily edit one budget to set a very low threshold
  - Monitor for alert email delivery
  - Reset to appropriate threshold

---

## Section 3: Google Cloud Pricing Calculator Analysis (60 minutes)

### Step 3.1: Access and Setup Pricing Calculator (15 minutes)

**1. Access Google Cloud Pricing Calculator**
1. Open a new browser tab
2. Navigate to: [Google Cloud Pricing Calculator](https://cloud.google.com/products/calculator)
3. **Familiarize yourself with the interface**:
  - Review available product categories
  - Understand the estimate building process
  - Note the save and share functionality

**2. Prepare for ML Workload Estimation**
1. **Reference your AWS analysis**: Have your SageMaker cost breakdown available
2. **Set region**: Choose "us-central1" (Iowa) to match typical AWS usage
3. **Plan estimation approach**: Break down by major service categories

### Step 3.2: Vertex AI Training Cost Estimation (20 minutes)

**1. Add Vertex AI Custom Training**
1. In the calculator, find and click "Vertex AI"
2. Select "Custom training"
3. **Configure training parameters based on AWS analysis**:

  **Training Configuration:**
  - **Region**: us-central1
  - **Machine type**: n1-standard-8 (closest to ml.m5.2xlarge)
  - **Training hours per month**: [Based on your AWS SageMaker analysis]
  - **Number of training jobs**: [Estimate based on current frequency]

4. **Add GPU configuration if needed**:
  - GPU type: NVIDIA V100 (if currently using GPU instances in AWS)
  - Number of GPUs: Match current AWS configuration
  - GPU hours: [Based on current usage patterns]

5. **Add storage for training**:
  - Persistent disk: 100GB SSD
  - Adjust based on current storage needs

**2. Configure Multiple Training Scenarios**
1. **Development training**:
  - Add another Vertex AI training estimate
  - Smaller instance types for development
  - Fewer hours per month
2. **Production training**:
  - Larger instances for production workloads
  - Include batch training scenarios

### Step 3.3: Vertex AI Prediction and Supporting Services (25 minutes)

**1. Add Vertex AI Prediction Endpoints**
1. In the calculator, add "Vertex AI" again
2. Select "Online prediction"
3. **Configuration**:
  - **Machine type**: n1-standard-4
  - **Number of nodes**: Start with 2, autoscale to 5
  - **Prediction requests per month**: [Based on current AWS endpoint usage]
  - **Average request size**: [Estimate in KB based on current models]
  - **Average response size**: [Estimate based on current output]

**2. Add Cloud Storage Estimation**
1. Click "Cloud Storage" in the calculator
2. **Configure storage needs**:
  - **Standard storage**: [GB] for active training data
  - **Nearline storage**: [GB] for infrequently accessed data
  - **Archive storage**: [GB] for long-term retention
  - **Operations**:
    - Class A operations: [Number for uploads/writes]
    - Class B operations: [Number for downloads/reads]

**3. Add Compute Engine for Custom ML Workloads**
1. Click "Compute Engine" in the calculator
2. **Configure for custom ML VMs**:
  - **Instance type**: Custom or predefined based on needs
  - **Operating hours**: [Hours per month for custom training]
  - **Persistent disk**: [GB] for VM storage
  - **GPUs**: Add if needed for custom training

**4. Add Networking Costs**
1. Click "Network" in the calculator
2. **Configure data transfer**:
  - **Egress to internet**: [GB] based on current AWS data transfer
  - **Inter-region traffic**: [GB] if using multiple regions

### Step 3.4: Generate and Analyze Estimate (10 minutes)

**1. Review Total Estimate**
1. **Scroll to the estimate summary**
2. **Review monthly totals by service**
3. **Check annual projections**
4. **Note any cost optimizations suggested**

**2. Save and Export Estimate**
1. **Save estimate**:
  - Click "Save estimate"
  - Name: "Sysco ML Migration Estimate"
  - Add description: "Initial migration cost projection"
2. **Share estimate**:
  - Click "Share estimate" to get permanent URL
  - Save URL for future reference
3. **Export data**:
  - Click "Export" and download CSV
  - Save for detailed analysis

---

## Section 4: Cost Comparison Framework Development (45 minutes)

### Step 4.1: Create Comprehensive AWS vs GCP Comparison (25 minutes)

**1. Compile Detailed Cost Comparison**
Create a comprehensive comparison matrix in your spreadsheet:

| Service Component | AWS SageMaker | GCP Vertex AI | Monthly Difference | Annual Difference | Notes |
|-------------------|---------------|---------------|-------------------|-------------------|--------|
| **Training Compute** | $X,XXX | $X,XXX | ±$XXX | ±$X,XXX | Include GPU costs |
| **Prediction Endpoints** | $X,XXX | $X,XXX | ±$XXX | ±$X,XXX | Auto-scaling comparison |
| **Development Environment** | $XXX | $XXX | ±$XX | ±$XXX | Notebook instances vs Workbench |
| **Storage Costs** | $XXX | $XXX | ±$XX | ±$XXX | S3 vs Cloud Storage |
| **Data Transfer** | $XXX | $XXX | ±$XX | ±$XXX | Egress and inter-region |
| **Management Overhead** | $XXX | $XXX | ±$XX | ±$XXX | Operational costs |
| **Support and SLA** | $XXX | $XXX | ±$XX | ±$XXX | Enterprise support levels |
| **Total Monthly** | **$X,XXX** | **$X,XXX** | **±$XXX** | **±$X,XXX** | **Net difference** |

**2. Document Key Assumptions**
1. **List all assumptions made**:
  - Usage patterns remain constant
  - Similar performance requirements
  - Equivalent SLA requirements
2. **Identify cost variables**:
  - Factors that could increase costs
  - Potential for additional savings
  - Regional pricing differences
3. **Note service capability differences**:
  - Features available in one platform but not the other
  - Performance differences that might affect costs

### Step 4.2: Total Cost of Ownership (TCO) Analysis (20 minutes)

**1. Expand Analysis Beyond Direct Cloud Costs**
Create a comprehensive TCO analysis:

| Cost Category | One-Time Costs | Ongoing Monthly Costs | Notes |
|---------------|----------------|--------------------|--------|
| **Direct Cloud Costs** | - | $X,XXX | From comparison above |
| **Migration Costs** | $X,XXX | - | One-time migration effort |
| - Data Transfer | $XXX | - | Moving data from AWS to GCP |
| - Application Modification | $X,XXX | - | Code changes and testing |
| - Training and Certification | $X,XXX | - | Team upskilling |
| **Operational Changes** | $X,XXX | $XXX | New tools and processes |
| **Risk Mitigation** | $XXX | $XXX | Security and compliance |
| **Opportunity Costs** | $X,XXX | - | Development delays |
| **Total TCO** | **$X,XXX** | **$X,XXX** | **Complete picture** |

**2. Calculate Break-Even Analysis**
1. **Determine monthly savings**: GCP monthly cost - AWS monthly cost
2. **Calculate break-even period**: Total one-time costs ÷ Monthly savings
3. **Create scenarios**:
  - Best case (maximum savings)
  - Realistic case (expected savings)
  - Worst case (minimal savings)

---

## Section 5: Cost Monitoring and Governance Setup (30 minutes)

### Step 5.1: Cloud Monitoring Integration for Cost Alerts (15 minutes)

**1. Access Cloud Monitoring from Google Cloud Console**
1. In the Google Cloud Console, ensure you're in the correct project
2. Navigate to "Monitoring" from the main menu
3. If first time setup, follow the workspace creation prompts

**2. Create Custom Dashboards for Cost Monitoring**
1. **In Cloud Monitoring, click "Dashboards"**
2. **Click "Create Dashboard"**
3. **Configure dashboard**:
  - Name: "ML Workload Cost Monitoring"
  - Description: "Cost tracking for ML migration project"
4. **Add charts for cost monitoring**:
  - Click "Add Chart"
  - Select appropriate billing metrics
  - Configure time ranges and aggregation
5. **Save dashboard** for regular monitoring

**3. Set Up Additional Alert Policies**
1. **In Cloud Monitoring, click "Alerting"**
2. **Click "Create Policy"**
3. **Configure cost-based alerts**:
  - Alert name: "High Daily ML Spend"
  - Condition: Based on billing metrics
  - Threshold: Daily spend exceeding normal patterns
  - Notification: Email to team leads

### Step 5.2: Establish Cost Governance Framework (15 minutes)

**1. Create Cost Review Process Documentation**
Document a comprehensive cost governance process:

Daily Monitoring (Console-Based - 10 minutes):

Check billing overview at console.cloud.google.com/billing
Review budget status in budgets dashboard
Quick scan of any cost alerts in Cloud Monitoring

Weekly Review (Console Analysis - 30 minutes):

Deep dive into billing reports
Analyze spending trends and patterns
Compare actual vs budgeted spend
Review any budget threshold alerts

Monthly Review (Comprehensive Analysis - 2 hours):

Full cost breakdown analysis using Reports
Budget reconciliation and adjustment
Cost optimization opportunity identification
Stakeholder reporting and communication

Quarterly Review (Strategic Planning - 4 hours):

TCO analysis update using pricing calculator
Service optimization review
Long-term budget planning and forecasting
Migration ROI assessment

**2. Create Cost Management Runbook**
Document standard operating procedures:

```markdown
# Google Cloud ML Cost Management Runbook

## Daily Tasks (Console-Based)
- [ ] Check billing overview dashboard
- [ ] Review any budget alerts in Budgets & alerts
- [ ] Monitor Cloud Monitoring dashboards for anomalies
- [ ] Validate no unexpected resource creation

## Weekly Tasks (Analysis and Planning)
- [ ] Generate and review cost reports
- [ ] Analyze spending trends using Reports interface
- [ ] Update cost forecasts based on current usage
- [ ] Review and adjust budgets if necessary

## Monthly Tasks (Governance and Reporting)
- [ ] Complete budget reconciliation
- [ ] Implement identified cost optimizations
- [ ] Prepare stakeholder cost summary reports
- [ ] Update pricing calculator estimates based on actual usage
- [ ] Review and validate cost allocation across projects

## Quarterly Tasks (Strategic Review)
- [ ] Comprehensive TCO analysis update
- [ ] Service optimization and rightsizing review
- [ ] Long-term budget planning and forecasting
- [ ] Migration ROI assessment and validation

## Emergency Procedures
### Budget Overage Response
1. Immediately access billing console to identify cost drivers
2. Review recent resource creation and usage spikes
3. Implement temporary cost controls if necessary
4. Escalate to finance and management team
5. Document incident and update monitoring thresholds

### Unexpected Cost Spike Investigation
1. Use Reports interface to identify service causing spike
2. Filter by time period to pinpoint exact timing
3. Check Cloud Monitoring for corresponding resource usage
4. Investigate recent changes or deployments
5. Implement immediate mitigation if required

## Contact Information
- Finance Team: [Contact information]
- Cloud Operations: [Contact information]
- ML Team Leads: [Contact information]
- Escalation Manager: [Contact information]

## Key Console URLs for Quick Access
- Billing Overview: https://console.cloud.google.com/billing
- Budgets & Alerts: https://console.cloud.google.com/billing/budgets
- Cost Reports: https://console.cloud.google.com/billing/reports
- Pricing Calculator: https://cloud.google.com/products/calculator
- Cloud Monitoring: https://console.cloud.google.com/monitoring