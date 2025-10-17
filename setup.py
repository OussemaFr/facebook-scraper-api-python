# Path: facebook-scraper-python/setup.py

"""Setup configuration for Facebook Scraper SDK."""

from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="facebook-scraper-sdk",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Official Python SDK for Facebook Scraper API via RapidAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/facebook-scraper-python",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/facebook-scraper-python/issues",
        "Documentation": "https://github.com/yourusername/facebook-scraper-python#readme",
        "Source Code": "https://github.com/yourusername/facebook-scraper-python",
        "Changelog": "https://github.com/yourusername/facebook-scraper-python/blob/main/CHANGELOG.md",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0,<3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "isort>=5.11.0",
            "mypy>=0.990",
            "twine>=4.0.0",
            "build>=0.10.0",
        ],
    },
    keywords=[
        "facebook",
        "scraper",
        "api",
        "sdk",
        "social-media",
        "data-extraction",
        "rapidapi",
        "facebook-api",
    ],
)