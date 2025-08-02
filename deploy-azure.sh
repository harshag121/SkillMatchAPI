#!/bin/bash

# Azure Deployment Script for SkillMatchAPI
# This script automates the deployment process to Azure App Service

set -e  # Exit on any error

echo "🚀 Azure Deployment Script for SkillMatchAPI"
echo "============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Configuration
RESOURCE_GROUP="skillmatch-rg"
APP_NAME="skillmatch-api"
LOCATION="East US"
SKU="B1"

print_step "Checking Azure CLI installation..."
if ! command -v az &> /dev/null; then
    print_error "Azure CLI is not installed. Please install it first:"
    echo "https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

print_status "Azure CLI found"

print_step "Checking Azure login status..."
if ! az account show &> /dev/null; then
    print_warning "Not logged into Azure. Please login..."
    az login
fi

SUBSCRIPTION=$(az account show --query name -o tsv)
print_status "Logged into Azure subscription: $SUBSCRIPTION"

print_step "Creating resource group (if it doesn't exist)..."
az group create --name $RESOURCE_GROUP --location "$LOCATION" --output table

print_step "Checking for Gemini API Key..."
if [ -z "$GEMINI_API_KEY" ]; then
    if [ -f ".env" ] && grep -q "GEMINI_API_KEY=" .env; then
        GEMINI_API_KEY=$(grep "GEMINI_API_KEY=" .env | cut -d'=' -f2)
        print_status "Found Gemini API key in .env file"
    else
        print_error "GEMINI_API_KEY not found in environment or .env file"
        echo "Please set your Gemini API key:"
        echo "export GEMINI_API_KEY=your_api_key_here"
        echo "Or add it to your .env file"
        exit 1
    fi
fi

# Unique app name with timestamp
UNIQUE_APP_NAME="${APP_NAME}-$(date +%s)"

print_step "Deploying ARM template..."
DEPLOYMENT_RESULT=$(az deployment group create \
    --resource-group $RESOURCE_GROUP \
    --template-file azure-deploy-template.json \
    --parameters appName=$APP_NAME sku=$SKU geminiApiKey="$GEMINI_API_KEY" \
    --query properties.outputs \
    --output json)

if [ $? -eq 0 ]; then
    WEB_APP_URL=$(echo $DEPLOYMENT_RESULT | jq -r '.webAppUrl.value')
    WEB_APP_NAME=$(echo $DEPLOYMENT_RESULT | jq -r '.webAppName.value')
    
    print_status "ARM template deployed successfully"
    print_status "Web App Name: $WEB_APP_NAME"
    print_status "Web App URL: $WEB_APP_URL"
else
    print_error "ARM template deployment failed"
    exit 1
fi

print_step "Configuring deployment source..."
az webapp deployment source config-local-git \
    --name $WEB_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --output table

print_step "Getting deployment credentials..."
DEPLOY_URL=$(az webapp deployment list-publishing-credentials \
    --name $WEB_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --query scmUri \
    --output tsv)

print_status "Deployment URL: $DEPLOY_URL"

print_step "Setting up Git remote (if not exists)..."
if ! git remote get-url azure &> /dev/null; then
    git remote add azure $DEPLOY_URL
    print_status "Added Azure remote"
else
    git remote set-url azure $DEPLOY_URL
    print_status "Updated Azure remote URL"
fi

print_step "Deploying code to Azure..."
print_warning "You may be prompted for deployment credentials"
git add .
git commit -m "Deploy to Azure" || print_warning "No changes to commit"
git push azure main

print_step "Waiting for deployment to complete..."
sleep 30

print_step "Testing deployment..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$WEB_APP_URL/docs" || echo "000")

if [ "$HTTP_STATUS" = "200" ]; then
    print_status "✅ Deployment successful!"
else
    print_warning "⚠️  Deployment may still be in progress. Status: $HTTP_STATUS"
fi

echo ""
echo "🎉 Azure Deployment Complete!"
echo "================================="
echo "🌐 Application URL: $WEB_APP_URL"
echo "📚 API Documentation: $WEB_APP_URL/docs"
echo "🧪 Test Interface: $WEB_APP_URL/test"
echo "📱 Frontend: $WEB_APP_URL/frontend/"
echo ""
echo "Azure Resources:"
echo "📦 Resource Group: $RESOURCE_GROUP"
echo "🖥️  App Service: $WEB_APP_NAME"
echo ""
echo "Management URLs:"
echo "🔧 Azure Portal: https://portal.azure.com"
echo "📊 App Service: https://portal.azure.com/#resource/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.Web/sites/$WEB_APP_NAME"
echo ""

print_status "Deployment script completed successfully!"
