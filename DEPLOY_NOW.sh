#!/bin/bash

# Quick Azure Deployment Commands for SkillMatchAPI
# Run these commands in your local terminal

echo "🚀 Azure Deployment Commands for SkillMatchAPI"
echo "================================================"

# Step 1: Login to Azure
echo "1. Login to Azure:"
echo "az login"
echo ""

# Step 2: Create Resource Group
echo "2. Create Resource Group:"
echo "az group create --name skillmatch-rg --location 'East US'"
echo ""

# Step 3: Create App Service Plan
echo "3. Create App Service Plan:"
echo "az appservice plan create --name skillmatch-plan --resource-group skillmatch-rg --sku B1 --is-linux"
echo ""

# Step 4: Create Web App
echo "4. Create Web App:"
echo "az webapp create --resource-group skillmatch-rg --plan skillmatch-plan --name skillmatch-api-\$(date +%s) --runtime 'PYTHON|3.11'"
echo ""

# Step 5: Configure App Settings (Replace YOUR_API_KEY with actual key)
echo "5. Configure App Settings:"
echo "az webapp config appsettings set --resource-group skillmatch-rg --name skillmatch-api-TIMESTAMP --settings \\"
echo "  GEMINI_API_KEY='AIzaSyC_7uMvzi1N4ekH51QeTSevFCHpb6zGguQ' \\"
echo "  HOST='0.0.0.0' \\"
echo "  PORT='8000' \\"
echo "  DEBUG='false' \\"
echo "  WEBSITES_PORT='8000' \\"
echo "  SCM_DO_BUILD_DURING_DEPLOYMENT='true'"
echo ""

# Step 6: Set Startup Command
echo "6. Set Startup Command:"
echo "az webapp config set --resource-group skillmatch-rg --name skillmatch-api-TIMESTAMP --startup-file 'python -m uvicorn main:app --host 0.0.0.0 --port 8000'"
echo ""

# Step 7: Deploy Code
echo "7. Deploy Code:"
echo "az webapp deployment source config-local-git --name skillmatch-api-TIMESTAMP --resource-group skillmatch-rg"
echo ""

# Step 8: Get Deployment URL and Deploy
echo "8. Get Deployment URL and Deploy:"
echo "DEPLOY_URL=\$(az webapp deployment list-publishing-credentials --name skillmatch-api-TIMESTAMP --resource-group skillmatch-rg --query scmUri --output tsv)"
echo "git remote add azure \$DEPLOY_URL"
echo "git add ."
echo "git commit -m 'Deploy to Azure'"
echo "git push azure main"
echo ""

echo "📝 Notes:"
echo "- Replace 'skillmatch-api-TIMESTAMP' with your actual app name from step 4"
echo "- Your API key is already configured in the commands above"
echo "- After deployment, your app will be available at: https://skillmatch-api-TIMESTAMP.azurewebsites.net"
echo ""

echo "💡 Alternative: Use the automated script:"
echo "./deploy-azure.sh"
