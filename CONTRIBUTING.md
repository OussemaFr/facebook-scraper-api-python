# Path: facebook-scraper-python/CONTRIBUTING.md

# Contributing to Facebook Scraper SDK

Thank you for your interest in contributing!

## 📋 Development Setup
```bash
git clone https://github.com/yourusername/facebook-scraper-python.git
cd facebook-scraper-python
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

## 🧪 Running Tests
```bash
pytest tests/ -v
pytest --cov
```

## 🎨 Code Style
```bash
# Format code
black facebook_scraper_sdk/
isort facebook_scraper_sdk/

# Lint
flake8 facebook_scraper_sdk/

# Type check
mypy facebook_scraper_sdk/
```

## 📝 Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):
```
feat: add new endpoint support
fix: resolve timeout issue
docs: update API reference
test: add error handling tests
```

## 🔄 Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Update documentation
6. Submit PR

Thank you! 🎉