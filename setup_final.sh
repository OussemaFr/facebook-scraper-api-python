#!/bin/bash

echo "🔧 Setting up final improvements..."

# Format code
echo "📝 Formatting code..."
black facebook_scraper_sdk/ tests/ examples/
isort facebook_scraper_sdk/ tests/ examples/

# Run tests
echo "🧪 Running tests..."
pytest tests/ -v -m "not integration"

# Check coverage
echo "📊 Checking coverage..."
pytest tests/ --cov --cov-report=term-missing -m "not integration"

# Lint
echo "🔍 Linting..."
flake8 facebook_scraper_sdk/ --max-line-length=110

# Build package
echo "📦 Building package..."
python -m build

# Check package
echo "✅ Checking package..."
twine check dist/*

echo "✨ All done! Ready to publish!"
echo ""
echo "Next steps:"
echo "1. git add ."
echo "2. git commit -m 'feat: add retry logic, rate limiting, and logging'"
echo "3. git push"
echo "4. twine upload dist/*"