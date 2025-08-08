# Docker Setup Test Script

# Check Docker installation
echo "Checking Docker installation..."
docker --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Check Docker Desktop status
echo "Checking Docker Desktop status..."
docker info 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker Desktop is not running. Please start Docker Desktop and try again." -ForegroundColor Red
    Write-Host "💡 Open Docker Desktop application and wait for it to fully start" -ForegroundColor Yellow
    exit 1
}

echo "✅ Docker is installed and running!" -ForegroundColor Green

# Test build (optional - only if Docker is running)
echo "Testing Docker build..."
docker-compose build --no-cache meme-app
if ($LASTEXITCODE -eq 0) {
    echo "✅ Docker build successful!" -ForegroundColor Green
} else {
    echo "❌ Docker build failed. Check the logs above." -ForegroundColor Red
}

echo ""
echo "🚀 To start the full application stack:"
echo "   docker-compose up --build"
echo ""
echo "🌐 Then visit: http://localhost:3000"
