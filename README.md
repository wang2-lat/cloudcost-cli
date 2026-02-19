# cloudcost-cli

Analyze cloud bills, find savings, and predict costs.

## Features

- Parse cloud billing CSV files
- Generate visual cost reports
- Identify cost optimization opportunities (idle resources, cost spikes)
- Predict next month's costs based on historical data

## Installation


## Usage

### Analyze full bill and generate report


Save report to HTML file:


### Predict next month's cost


## CSV Format

Your cloud bill CSV should contain these columns:

- `date` - Date of the charge (YYYY-MM-DD)
- `service` - Service name (e.g., "EC2", "S3", "Lambda")
- `cost` - Cost amount (numeric)
- `resource_id` - (Optional) Resource identifier

Example:


## Example


## Cost Optimization Tips

The tool identifies:

- **Idle Resources**: Resources with minimal cost that may be unused
- **Cost Spikes**: Unusual daily cost increases (>2 standard deviations)
- **Top Services**: Services consuming the most budget
- **Trend Analysis**: Whether costs are increasing or stable