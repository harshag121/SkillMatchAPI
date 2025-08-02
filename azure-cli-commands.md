# Azure CLI Quick Commands for SkillMatchAPI

## Login and Setup
```bash
# Login to Azure
az login

# List subscriptions
az account list --output table

# Set default subscription
az account set --subscription "Your Subscription Name"

# Create resource group
az group create --name skillmatch-rg --location "East US"
```

## App Service Deployment
```bash
# Create App Service Plan
az appservice plan create --name skillmatch-plan --resource-group skillmatch-rg --sku B1 --is-linux

# Create Web App
az webapp create --resource-group skillmatch-rg --plan skillmatch-plan --name skillmatch-api-unique --runtime "PYTHON|3.11"

# Configure app settings
az webapp config appsettings set --resource-group skillmatch-rg --name skillmatch-api-unique --settings GEMINI_API_KEY="your_api_key_here" HOST="0.0.0.0" PORT="8000" DEBUG="false" WEBSITES_PORT="8000" SCM_DO_BUILD_DURING_DEPLOYMENT="true"

# Set startup command
az webapp config set --resource-group skillmatch-rg --name skillmatch-api-unique --startup-file "python -m uvicorn main:app --host 0.0.0.0 --port 8000"

# Deploy from local git
az webapp deployment source config-local-git --name skillmatch-api-unique --resource-group skillmatch-rg
```

## Container Instance Deployment
```bash
# Deploy container using ARM template
az deployment group create --resource-group skillmatch-rg --template-file azure-container-template.json --parameters geminiApiKey="your_api_key_here"

# Or create container instance directly
az container create --resource-group skillmatch-rg --name skillmatch-container --image skillmatch-api:latest --dns-name-label skillmatch-unique --ports 8001 --environment-variables GEMINI_API_KEY="your_api_key_here" HOST="0.0.0.0" PORT="8001"
```

## Monitoring and Management
```bash
# View logs
az webapp log tail --name skillmatch-api-unique --resource-group skillmatch-rg

# Restart app
az webapp restart --name skillmatch-api-unique --resource-group skillmatch-rg

# Show app details
az webapp show --name skillmatch-api-unique --resource-group skillmatch-rg --output table

# List all resources in group
az resource list --resource-group skillmatch-rg --output table

# Delete resource group (cleanup)
az group delete --name skillmatch-rg --yes --no-wait
```

## Scaling
```bash
# Scale up (increase instance size)
az appservice plan update --name skillmatch-plan --resource-group skillmatch-rg --sku S1

# Scale out (increase instance count)
az webapp scale --name skillmatch-api-unique --resource-group skillmatch-rg --instance-count 2

# Enable autoscale
az monitor autoscale create --resource-group skillmatch-rg --resource skillmatch-api-unique --resource-type Microsoft.Web/sites --name skillmatch-autoscale --min-count 1 --max-count 5 --count 1
```

## Security
```bash
# Enable HTTPS only
az webapp update --resource-group skillmatch-rg --name skillmatch-api-unique --https-only true

# Add custom domain (optional)
az webapp config hostname add --webapp-name skillmatch-api-unique --resource-group skillmatch-rg --hostname www.yourdomain.com
```
