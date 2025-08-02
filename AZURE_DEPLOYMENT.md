# Azure Deployment Guide for SkillMatchAPI

This guide provides multiple options for deploying your SkillMatchAPI to Microsoft Azure.

## 🚀 Quick Deployment Options

### Option 1: Automated Script Deployment (Recommended)
```bash
# Make sure you have your Gemini API key
export GEMINI_API_KEY=your_api_key_here

# Run the automated deployment script
./deploy-azure.sh
```

### Option 2: Manual Azure App Service
Use the Azure Portal or Azure CLI commands below.

### Option 3: GitHub Actions CI/CD
Automatic deployment on every push to main branch.

### Option 4: Docker Container Instances
Deploy using Azure Container Instances for containerized deployment.

## 📋 Prerequisites

### Required Software
- **Azure CLI**: [Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- **Git**: For code deployment
- **Google Gemini API Key**: [Get API Key](https://aistudio.google.com/app/apikey)

### Azure Account Setup
1. Create an Azure account at [portal.azure.com](https://portal.azure.com)
2. Install Azure CLI
3. Login to Azure:
   ```bash
   az login
   ```

## 🎯 Deployment Methods

### Method 1: Automated Script (Easiest)

**Step 1**: Set your API key
```bash
export GEMINI_API_KEY=your_actual_api_key_here
```

**Step 2**: Run deployment script
```bash
./deploy-azure.sh
```

**What it does:**
- Creates Azure Resource Group
- Deploys App Service with ARM template
- Configures environment variables
- Sets up Git deployment
- Deploys your code
- Provides access URLs

### Method 2: Manual Azure Portal Deployment

**Step 1**: Create App Service
1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Create a resource" → "Web App"
3. Configure:
   - **Subscription**: Your subscription
   - **Resource Group**: Create new "skillmatch-rg"
   - **Name**: "skillmatch-api-[unique]"
   - **Runtime**: Python 3.11
   - **Operating System**: Linux
   - **Region**: East US (or preferred)
   - **Pricing**: Basic B1 (or Free F1 for testing)

**Step 2**: Configure Environment Variables
1. Go to your App Service → Configuration → Application settings
2. Add these settings:
   ```
   GEMINI_API_KEY = your_api_key_here
   HOST = 0.0.0.0
   PORT = 8000
   DEBUG = false
   WEBSITES_PORT = 8000
   SCM_DO_BUILD_DURING_DEPLOYMENT = true
   ```

**Step 3**: Configure Startup Command
1. Go to Configuration → General settings
2. Set **Startup Command**: 
   ```
   python -m uvicorn main:app --host 0.0.0.0 --port 8000
   ```

**Step 4**: Deploy Code
1. Go to Deployment Center
2. Choose "Local Git" or "GitHub"
3. Follow deployment instructions

### Method 3: GitHub Actions CI/CD

**Step 1**: Get Publish Profile
1. In Azure Portal, go to your App Service
2. Click "Get publish profile" and download the file
3. Copy the entire contents

**Step 2**: Add GitHub Secrets
1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Add secrets:
   - `AZURE_WEBAPP_PUBLISH_PROFILE`: Paste publish profile content
   - `GEMINI_API_KEY`: Your Gemini API key

**Step 3**: Push to Main Branch
The workflow file `.github/workflows/azure-deploy.yml` will automatically deploy on push to main.

### Method 4: Azure Container Instances

**Step 1**: Build and Push Docker Image
```bash
# Build Docker image
docker build -t skillmatch-api .

# Tag for Azure Container Registry (optional)
docker tag skillmatch-api your-registry.azurecr.io/skillmatch-api:latest

# Push to registry
docker push your-registry.azurecr.io/skillmatch-api:latest
```

**Step 2**: Deploy with ARM Template
```bash
az deployment group create \
  --resource-group skillmatch-rg \
  --template-file azure-container-template.json \
  --parameters geminiApiKey="your_api_key"
```

## 🌐 Access Your Deployed Application

After successful deployment, your application will be available at:

### Azure App Service URLs
- **Main App**: `https://your-app-name.azurewebsites.net/`
- **API Docs**: `https://your-app-name.azurewebsites.net/docs`
- **Test Interface**: `https://your-app-name.azurewebsites.net/test`
- **Frontend**: `https://your-app-name.azurewebsites.net/frontend/`

### Individual Frontend Pages
- **Landing**: `/frontend/index.html`
- **Upload Resume**: `/frontend/upload.html`
- **Skill Extraction**: `/frontend/skills.html`
- **Job Search**: `/frontend/jobs.html`
- **Results**: `/frontend/results.html`
- **About**: `/frontend/about.html`
- **Contact**: `/frontend/contact.html`

## 🔧 Configuration & Monitoring

### Environment Variables
Required settings in Azure App Service:
```
GEMINI_API_KEY=your_api_key_here
HOST=0.0.0.0
PORT=8000
DEBUG=false
WEBSITES_PORT=8000
SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

### Monitoring & Logs
1. **Application Insights**: Enable for detailed monitoring
2. **Log Stream**: View real-time logs in Azure Portal
3. **Metrics**: Monitor CPU, memory, and requests
4. **Alerts**: Set up alerts for errors or high usage

### Scaling Options
1. **Scale Up**: Increase instance size (CPU/RAM)
2. **Scale Out**: Add more instances for high traffic
3. **Auto-scaling**: Automatic scaling based on metrics

## 🛠️ Troubleshooting

### Common Issues

**1. "Application Error" on startup**
- Check Application Settings for correct environment variables
- Verify startup command: `python -m uvicorn main:app --host 0.0.0.0 --port 8000`
- Check logs in Log Stream

**2. "Module not found" errors**
- Ensure `SCM_DO_BUILD_DURING_DEPLOYMENT=true` is set
- Check that `requirements.txt` is in root directory
- Verify Python version is 3.11

**3. API key not working**
- Verify `GEMINI_API_KEY` is correctly set in Application Settings
- Check that the API key is valid and has quota
- Ensure no extra spaces or characters in the key

**4. Frontend not loading**
- Check that `frontend/` directory is deployed
- Verify static file serving is configured
- Check CORS settings in main.py

### Debug Mode
To enable detailed logging, set:
```
DEBUG=true
```

### Viewing Logs
1. Azure Portal → Your App Service → Monitoring → Log stream
2. Or use Azure CLI:
   ```bash
   az webapp log tail --name your-app-name --resource-group skillmatch-rg
   ```

## 💰 Cost Optimization

### Pricing Tiers
- **Free F1**: Good for testing (limited to 60 minutes/day)
- **Basic B1**: ~$13/month, good for development
- **Standard S1**: ~$56/month, production ready
- **Premium P1V2**: ~$73/month, best performance

### Cost-Saving Tips
1. Use **Free F1** tier for development/testing
2. Enable **auto-shutdown** for development environments
3. Monitor **Gemini API usage** (main cost driver)
4. Use **Application Insights** sampling to reduce logs cost

## 🔐 Security Best Practices

### Production Security
1. **HTTPS Only**: Enable HTTPS redirection
2. **API Key Security**: Use Azure Key Vault for secrets
3. **CORS Configuration**: Restrict origins to your domain
4. **Authentication**: Add Azure AD authentication if needed
5. **Network Security**: Use Virtual Networks for enhanced security

### Example Secure CORS Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],  # Replace with your domain
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## 📊 Performance Optimization

### App Service Optimization
1. **Always On**: Enable to prevent cold starts
2. **Application Initialization**: Configure warm-up requests
3. **Connection Strings**: Use for database connections
4. **Caching**: Implement Redis cache for job search results

### Code Optimization
1. **Async Operations**: Use async/await for I/O operations
2. **Connection Pooling**: Reuse HTTP connections
3. **Caching**: Cache Gemini API responses
4. **Compression**: Enable gzip compression

## 🚀 Advanced Deployment

### Blue-Green Deployment
1. Create deployment slots in Azure App Service
2. Deploy to staging slot first
3. Test staging environment
4. Swap slots for zero-downtime deployment

### Multiple Environments
Create separate App Services for:
- **Development**: `skillmatch-dev`
- **Staging**: `skillmatch-staging`  
- **Production**: `skillmatch-prod`

### Infrastructure as Code
Use the provided ARM templates for consistent deployments:
```bash
# Deploy infrastructure
az deployment group create \
  --resource-group skillmatch-rg \
  --template-file azure-deploy-template.json \
  --parameters @parameters.json
```

## 📞 Support & Resources

### Azure Documentation
- [Azure App Service Python](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python)
- [Azure Container Instances](https://docs.microsoft.com/en-us/azure/container-instances/)
- [Azure DevOps](https://docs.microsoft.com/en-us/azure/devops/)

### Monitoring & Debugging
- [Application Insights](https://docs.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview)
- [Azure Monitor](https://docs.microsoft.com/en-us/azure/azure-monitor/)

### Community Support
- [Azure Community](https://techcommunity.microsoft.com/t5/azure/ct-p/Azure)
- [Stack Overflow - Azure](https://stackoverflow.com/questions/tagged/azure)

---

🎉 **Congratulations!** Your SkillMatchAPI is now running on Microsoft Azure with enterprise-grade scalability and reliability!
